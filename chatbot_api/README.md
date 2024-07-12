# Projeto API

Este projeto é destinado para disponibilizar os endpoints.

## Pré-requisitos

- Python 3.9.7
- Pip (gerenciador de pacotes do Python)

## Passo a passo para executar o projeto localmente

1. **Clone o repositório:**

   ```bash
   git clone git@github.com:CEIA-UpFlux/symphony.git
   cd symphony/chatbot_api
   ```
   
Crie e ative um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # Para sistemas Unix
```

Para usuários Windows, o comando de ativação é:

```bash
.\venv\Scripts\activate
```
Instale as dependências:

```bash
pip install -r requirements.txt
```
Execute a aplicação:

```bash
python src/main.py
```
Reinstalar dependências (se necessário):

Caso precise reinstalar todas as dependências, use o comando abaixo:

```bash
pip install --force-reinstall -r requirements.txt
```

Quando a aplicação subir os endpoins para teste estão na url:

http://localhost:8000/docs

se caso quiser rodar algum teste unitário específico: (exemplo test_assistant_create)

```bash
python tests/test_assistant_create.py
```

Estrutura do Projeto
- src/ - Contém o código fonte do projeto
- requirements.txt - Lista de dependências necessárias para o projeto
