# Construa um chatbot LLM RAG com LangChain

Este repositório contém o código-fonte para [Construir um LLM RAG Chatbot com LangChain](https://realpython.com/build-llm-rag-chatbot-with-langchain/)

Para executar o aplicativo final que você construirá neste tutorial, você pode usar o código fornecido em `source_code_final/`.

## Configurar

Crie um arquivo `.env` no diretório raiz e adicione as seguintes variáveis de ambiente:

```.env
OPENAI_API_KEY=<>

DEFINITIONS_JSON_PATH=https://github.com/leandropedrosa/arquivos/blob/main/datatype_definitions.json

O2C_AGENT_MODEL=gpt-3.5-turbo-1106
O2C_CYPHER_MODEL=gpt-3.5-turbo-1106
O2C_QA_MODEL=gpt-3.5-turbo-0125

CHATBOT_URL=http://chatbot_api:8000/o2c-rag-agent
```
Depois de preencher todas as variáveis de ambiente e instalar o Docker Compose, abra um terminal e execute:

```console
docker-compose up --build
```
Após cada container finalizar a construção, você poderá acessar a API do chatbot em http://localhost:8000/docs e o aplicativo Streamlit em http://localhost:8501/.




Comandos básicos Docker:

Gerenciamento de Contêineres
```console
docker ps
```
Lista contêineres em execução.

```console
docker ps -a
```
Lista todos os contêineres (incluindo os parados).

```console
docker start <container_id>
```
Inicia um contêiner parado.

```console
docker stop <container_id>
```
Para um contêiner em execução.

```console
docker restart <container_id>
```
Reinicia um contêiner.

```console
docker rm <container_id>
```
Remove um contêiner parado.

```console
docker container prune
```
Remove todos os contêineres parados.

Gerenciamento de Imagens:

```console
docker images
```
Lista todas as imagens.

```console
docker pull <image_name>
```
Baixa uma imagem.

```console
docker rmi <image_id>
```
Remove uma imagem.

```console
docker image prune
```
Remove todas as imagens não utilizadas.

Gerenciamento de Volumes:

```console
docker volume ls
```
Lista volumes.

```console
docker volume create <volume_name>
```
Cria um volume.

```console
docker volume rm <volume_name>
```
Remove um volume.

```console
docker volume prune
```
Remove todos os volumes não utilizados.

Gerenciamento de Redes:

```console
docker network ls
```
Lista redes.

```console
docker network create <network_name>
```
Cria uma rede.

```console
docker network rm <network_name>
```
Remove uma rede.

```console
docker network prune
```
Remove todas as redes não utilizadas.

Comandos Utilitários:

```console
docker logs <container_id>
```
Ver logs de um contêiner.

```console
docker exec -it <container_id> <command>
```
Executa um comando em um contêiner em execução.

```console
docker attach <container_id>
```
Anexa-se a um contêiner em execução.

```console
docker info
```
Obter informações detalhadas sobre o sistema Docker.

```console
docker system df
```
Ver o uso de disco por contêineres, imagens e volumes.

```console
docker-compose down -v
```
Derruba todos os serviços e remove os volumes criados com Docker Compose.
