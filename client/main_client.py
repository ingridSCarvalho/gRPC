import grpc
import dictionary_pb2
import dictionary_pb2_grpc

def run_client():
    channel = grpc.insecure_channel('localhost:50051')
    
   
    stub = dictionary_pb2_grpc.DictionaryServiceStub(channel)
    
    while True:
        print("Escolha o modo (1: Inclusão, 2: Consulta): ")
        modo = input()
        
        if modo == '1':
            while True:
                word = input("Digite uma palavra para incluir (ou 'sair' para finalizar): ")
                if word.lower() == 'sair':
                    break
                    
                
                request = dictionary_pb2.WordRequest(word=word)
                
                try:
            
                    response = stub.AddWord(request)
                    print(f"Palavra '{word}' adicionada/atualizada. Contagem atual: {response.count}")
                except grpc.RpcError as e:
                    print(f"Erro ao adicionar palavra: {e.details()}")
                    
        elif modo == '2':
            try:
               
                request = dictionary_pb2.EmptyRequest()
                
        
                response = stub.PrintDictionary(request)
                
                print("\nDicionário atual:")
                for word_count in response.words:
                    print(f"Palavra: {word_count.word}, Contagem: {word_count.count}")
                print()
            except grpc.RpcError as e:
                print(f"Erro ao consultar dicionário: {e.details()}")
                
        else:
            print("Opção inválida!")
            
        print("\nDeseja continuar? (s/n): ")
        if input().lower() != 's':
            break
    
    channel.close()

if __name__ == '__main__':
    try:
        run_client()
    except KeyboardInterrupt:
        print("\nEncerrando cliente...")
    except Exception as e:
        print(f"Erro inesperado: {e}")
