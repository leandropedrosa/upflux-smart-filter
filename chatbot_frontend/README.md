# Projeto front de teste

Este projeto é destinado uma interface grafica de teste.

## Pré-requisitos

- Python 3.9.7
- Pip (gerenciador de pacotes do Python)

## Passo a passo para executar o projeto localmente

1. **Clone o repositório:**

   ```bash
   git clone git@github.com:CEIA-UpFlux/symphony.git
   cd symphony/chatbot_frontend
   ```
   
Crie e ative um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```
Para usuários Windows, o comando de ativação é:
```
```bash
.\venv\Scripts\activate
```
Instale as dependências:

```bash
pip install -r requirements.txt
```
Execute a aplicação:

```bash
python streamlit run src/main.py
```
Reinstalar dependências (se necessário):

Caso precise reinstalar todas as dependências, use o comando abaixo:

```bash
pip install --force-reinstall -r requirements.txt
```
Estrutura do Projeto
- src/ - Contém o código fonte do projeto
- requirements.txt - Lista de dependências necessárias para o projeto
