from fastapi import FastAPI
import sys
import os
from dotenv import load_dotenv

import uvicorn

app = FastAPI()
def init_app():

    @app.get("/")
    async def root():
        return {"message": "Ok!"}

    from src.routes import assistant_routes, agent_routes

    app.include_router(agent_routes.router)
    app.include_router(assistant_routes.router)
    return app

@app.get("/healthcheck")
async def root():
    return {"message": "Ok!"}


if __name__ == '__main__':
    # Adiciona o diretório atual ao sys.path
    sys.path.append(os.getcwd())

    # Imprime todos os caminhos no sys.path para verificação
    print(sys.path)

    # Define o caminho para o arquivo .env
    dotenv_path = os.path.join(os.getcwd(), '.env')
    print(f"Loading .env from: {dotenv_path}")

    # Carrega o arquivo .env
    load_dotenv(dotenv_path)

    # Verifica se a variável de ambiente foi carregada corretamente
    if not os.getenv("OPENAI_API_KEY"):
        raise TypeError("'env' variable not found in .env file")

    app = init_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)