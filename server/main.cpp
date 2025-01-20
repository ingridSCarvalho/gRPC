#include <grpcpp/grpcpp.h>
#include "dictionary.grpc.pb.h"
#include <string>
#include <unordered_map>
#include <iostream>
#include <iomanip>

static std::unordered_map<std::string, int> word_dictionary;

void printSeparator()
{
    std::cout << "\n"
              << std::string(50, '-') << "\n";
}

class DictionaryServiceImpl final : public dictionary::DictionaryService::Service
{
    grpc::Status AddWord(grpc::ServerContext *context,
                         const dictionary::WordRequest *request,
                         dictionary::WordResponse *response) override
    {
        printSeparator();
        std::cout << "Recebida requisição AddWord\n";
        std::cout << "Palavra recebida: '" << request->word() << "'\n";

        std::string word = request->word();

        if (word.empty())
        {
            std::cout << "ERRO: Palavra vazia recebida!\n";
            printSeparator();
            return grpc::Status(grpc::StatusCode::INVALID_ARGUMENT,
                                "Palavra não pode ser vazia.");
        }

        bool exists = word_dictionary.find(word) != word_dictionary.end();
        int old_count = exists ? word_dictionary[word] : 0;

        word_dictionary[word]++;
        response->set_count(word_dictionary[word]);

        std::cout << "Operação realizada:\n"
                  << "- Palavra: '" << word << "'\n"
                  << "- Contagem anterior: " << old_count << "\n"
                  << "- Nova contagem: " << word_dictionary[word] << "\n";

        std::cout << "\nEstado atual do dicionário:\n";
        for (const auto &entry : word_dictionary)
        {
            std::cout << std::setw(20) << std::left << entry.first
                      << " : " << entry.second << "\n";
        }

        printSeparator();
        return grpc::Status::OK;
    }

    grpc::Status PrintDictionary(grpc::ServerContext *context,
                                 const dictionary::EmptyRequest *request,
                                 dictionary::DictionaryResponse *response) override
    {
        printSeparator();
        std::cout << "Recebida requisição PrintDictionary\n";

        if (word_dictionary.empty())
        {
            std::cout << "Dicionário está vazio!\n";
        }
        else
        {
            std::cout << "Enviando " << word_dictionary.size() << " palavras:\n";
        }

        for (const auto &entry : word_dictionary)
        {
            auto word_count = response->add_words();
            word_count->set_word(entry.first);
            word_count->set_count(entry.second);

            std::cout << std::setw(20) << std::left << entry.first
                      << " : " << entry.second << "\n";
        }

        printSeparator();
        return grpc::Status::OK;
    }
};

int main()
{
    std::string server_address("0.0.0.0:50051");
    DictionaryServiceImpl service;

    grpc::ServerBuilder builder;
    builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);

    printSeparator();
    std::cout << "Iniciando servidor...\n";

    std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
    std::cout << "Servidor rodando em " << server_address << "\n";
    printSeparator();

    server->Wait();

    return 0;
}
