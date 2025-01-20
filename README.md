# gRPC
Este repositório é destinado à disciplina de PSPD (Programação de Sistemas Paralelos e Distribuídos), contendo materiais e laboratórios relacionados aos temas gRPC e Virtualização.

## Sobre gRPC
O gRPC (gRPC Remote Procedure Call) é um framework de código aberto desenvolvido pelo Google que facilita a comunicação entre sistemas distribuídos.

- Baseado no protocolo HTTP/2, oferece alta performance e comunicação bidirecional.
- Usa Protocol Buffers (Protobuf) como formato de serialização, tornando a troca de mensagens mais eficiente.
- É amplamente utilizado para conectar serviços em arquiteturas microservices e sistemas distribuídos, garantindo baixo consumo de recursos e alta escalabilidade.

## Sobre Virtualização
A Virtualização é uma tecnologia que permite a execução de várias máquinas virtuais (VMs) em um único hardware físico, otimizando o uso de recursos.

- Máquina Virtual (VM): Uma instância isolada de um sistema operacional, simulada em software, que pode rodar como se fosse um computador físico.
- Benefícios incluem:
    Melhor utilização de hardware.
    Testes em múltiplos sistemas operacionais sem necessidade de várias máquinas físicas.
    Escalabilidade e flexibilidade para ambientes de desenvolvimento e produção.

## PASSO A PASSO p/ executar no linux: 

1. Variaveis de ambiente, tecnologias e build: 
    ```bash
    export MY_INSTALL_DIR=$HOME/.local 
    ```
    ```bash
    mkdir -p $MY_INSTALL_DIR 
    ```
    ```bash
    export PATH="$MY_INSTALL_DIR/bin:$PATH" 
    ```
    ```bash
    sudo apt install -y build-essential autoconf libtool pkg-config 
    ```
     ```bash
    git clone --recurse-submodules -b v1.66.0 --depth 1 --shallow-submodules https://github.com/grpc/grpc 
    ```        
    ```bash
    cd grpc
    mkdir -p cmake/build
    pushd cmake/build
    cmake -DgRPC_INSTALL=ON \
        -DgRPC_BUILD_TESTS=OFF \
        -DCMAKE_CXX_STANDARD=17 \
        -DCMAKE_INSTALL_PREFIX=$MY_INSTALL_DIR \
        ../..
    make -j 4
    make install
    popd
    ```
    ```bash
    protoc -I=proto --grpc_out=server --plugin=protoc-gen-grpc=$(which grpc_cpp_plugin) proto/dictionary.proto protoc -I=proto --cpp_out=server proto/dictionary.proto 
    ``` 
    ```bash
    mkdir build  
    cd build  
    cmake ..  
    make  
    cd .. 
    ```
   
2. Rodar servidor: 
    
    ```bash
    ./build/server 
    ```

3. Rodar cliente:  
 
    ```bash
    cd client 
    python3 main_client.py 
    ```

4. Rodar web_server: 
 
    ```bash
    cd api 
    python3 web_server.py 
    ```

5. Rodar front: 
 
    ```bash
    cd web_client 
    python3 -m http.server
    ```
