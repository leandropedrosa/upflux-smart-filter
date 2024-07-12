# Chatbot SYMPHONY

## Configurar

Crie um arquivo `.env` no diretório raiz e adicione as seguintes variáveis de ambiente:

```.env
OPENAI_API_KEY=<>

DEFINITIONS_JSON_PATH=https://github.com/leandropedrosa/arquivos/blob/main/datatype_definitions.json

O2C_AGENT_MODEL=gpt-3.5-turbo-1106
O2C_CYPHER_MODEL=gpt-3.5-turbo-1106
O2C_QA_MODEL=gpt-3.5-turbo-0125

CHATBOT_URL=http://chatbot_api:8000/agent/agent-local
ATLAS_CONNECTION_STRING=<url gerada de conexão do mongo atlas>
ATLAS_DB_NAME=<
ATLAS_COLLECTION_NAME=
ATLAS_INDEX_NAME=
```
Depois de preencher todas as variáveis de ambiente e instalar o Docker Compose, abra um terminal e execute:

```console
docker-compose up --build
```
Se precisar derrubar todos os serviços e remove os volumes criados com Docker Compose.
```console
docker-compose down -v
```
Se precisar listar todos contêineres em execução.
```console
docker ps -a
```
Após cada container finalizar a construção, você poderá acessar a API do chatbot em http://localhost:8000/docs e o aplicativo Streamlit em http://localhost:8501/.

Estrutura do proejeto

```console
./
│
├── chatbot_api/
│   │
│   ├── src/
│   │   │
│   │   ├── agents/
│   │   ├── assistants/
│   │   ├── client
│   │   ├── chroma_data/
│   │   ├── data/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── service/
│   │   ├── tools/
│   │   ├── utils/
│   │   ├── entrypoint.sh
│   │   └── main.py
│   ├── tests/
│   ├── .env
│   ├── Dockerfile
│   └── requirements.txt
│
├── chatbot_frontend/
│   │
│   ├── src/
│   │   ├── entrypoint.sh
│   │   └── main.py
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── tests_integration/
├── .env
└── docker-compose.yml
└── requirements.txt
```

## Debugging

Rode primeiro o composer up no arquivo docker-compose.debug.yml

```console
docker compose up
````

Depois, basta abrir com F5 o menu de depuração e acessar normalmente as rotas padrão.
Note que apenas a api será depurada com esse comando.