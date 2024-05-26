import os

from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import (
    create_openai_functions_agent,
    Tool,
    AgentExecutor,
)

from utils.async_utils import url_to_vector

O2C_AGENT_MODEL = os.getenv("O2C_AGENT_MODEL")

template = """Você é um assistente especializado em O2C, responda as perguntas sobre o processo e suas subáreas de
				forma concisa, considerando que todos os termos entre colchetes são variáveis.
				Para solicitações de valor financeiro, considere Real Brasileiro(R$).
				Para solicitações de intervalos de datas, considere data atual como: 01.
				Se solicitado intervalo com data de início maior que hoje, use o ano passado.
				tilize o ano atual como:2024.Ex: Semestre atual inicia em 01/
			    25 de Maio de 2024. Antes de responder, arredondar os
				ecimais a duas casas decimais e utilizar o formato para números do Brasil: XXX.XXX.XXX,XX"""

# Create Retriever
retriever_json = url_to_vector(json_path="./data/datatype_definitions.json")
# retriever_page = url_to_vector(url="https://blog.pedidoeletronico.com/order-to-cash/")
tools = [
    Tool(
        func=retriever_json.invoke,
        name="lcel_json",
        description="""Use esta ferramenta para obter os termos e com isso as informações que precisamos obter do usuário."""
    ),
]

llm = ChatOpenAI(
    model=O2C_AGENT_MODEL,
    temperature=0,
)

prompt = hub.pull("hwchase17/openai-functions-agent")

o2c_rag_agent = create_openai_functions_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,
)

o2c_rag_agent_executor = AgentExecutor(
    agent=o2c_rag_agent,
    tools=tools,
    return_intermediate_steps=True,
    verbose=True,
)
