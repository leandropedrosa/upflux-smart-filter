import os
from langchain.agents import (
    AgentExecutor,
    create_openai_functions_agent
)
from langchain.chat_models import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from src.tools import ToolDefinition
from langchain import hub

llm = ChatOpenAI(
            model=os.getenv("O2C_AGENT_MODEL", "gpt-3.5-turbo"),
            temperature=0,
            openai_api_key= os.getenv('OPENAI_API_KEY')
        )
tools = [ToolDefinition().create_json_retriever("rag_assistant_scope.json", name="rag_scopo",
                                                   description="Utilize quando for fazer sugestões")]

PREFIX = '''You are an assistant specialized in O2C. Respond to questions about the process and its subareas concisely, 
considering that all terms within brackets are variables. For financial value requests, consider the Brazilian Real (R$). 
Your sole mission is to create a JSON structure based on the interaction with the user, filling in each field of the example below:
[
   {
      "type":"agci",
      "context_name":"O2C",
      "dashboard":"Análise do Ciclo da Ordem de Venda",
      "main_keywords":[
         "taxa",
         "envios atrasados",
         "itens de vendas",
         "Grupo de cliente"
      ],
      "user_requested_unit":"porcentagem"
   },
   {
      "type":"tempo",
      "mode":"casos interligados",
      "DATE":"01/01/2023-30/06/2023",
      "start_date":"2023-01-01",
      "end_date":"2023-06-30"
   }
]
'''

FORMAT_INSTRUCTIONS = """To use a tool, please use the following format:
'''
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: Fill in each field of the example JSON below:
[
   {
      "type":"agci",
      "context_name":"O2C",
      "dashboard":"Análise do Ciclo da Ordem de Venda",
      "main_keywords":[
         "taxa",
         "envios atrasados",
         "itens de vendas",
         "Grupo de cliente"
      ],
      "user_requested_unit":"porcentagem"
   },
   {
      "type":"tempo",
      "mode":"casos interligados",
      "DATE":"01/01/2023-30/06/2023",
      "start_date":"2023-01-01",
      "end_date":"2023-06-30"
   }
]

This is the structure of each field:

{
  "properties": {
    "type": {
      "type": "string",
      "description": "Tipo de filtro"
    },
    "context_name": {
      "type": "string",
      "enum": [
        "O2C"
      ],
      "description": "Nome do contexto"
    },
    "dashboard": {
      "type": "string",
      "description": "Nome do dashboard"
    },
    "main_keywords": {
      "type": "string",
      "description": "Palavras-chave principais da pergunta do usuário"
    },
    "user_requested_unit": {
      "type": "string",
      "description": "Unidade solicitada pelo usuário"
    },
    "mode": {
      "type": "string",
      "description": "Modo de operação"
    },
    "DATE": {
      "type": "string",
      "description": "Data"
    },
    "start_date": {
      "type": "string",
      "description": "Data de início"
    },
    "end_date": {
      "type": "string",
      "description": "Data de término"
    }
  }
}
'''

Use your knowledge base to make suggestions in Portuguese if the user's question does not provide all the information 
needed to complete the JSON. Make a suggestion by offering short options with the sole purpose of completing the structure. 
Guide a conversation just to fill in the JSON fields. Ask in a friendly manner one field at a time.
"""

SUFFIX = '''

Begin!

Previous conversation history:
{chat_history}

Instructions: {input}
{agent_scratchpad}

Use your knowledge base to make suggestions in Portuguese if the user's question does not provide all the information 
needed to complete the JSON. Make a suggestion by offering short options with the sole purpose of completing the structure. 
Guide a conversation just to fill in the JSON fields. Ask in a friendly manner one field at a time.
'''

prompt = hub.pull("hwchase17/openai-functions-agent")

o2c_rag_agent = create_openai_functions_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,
)

agent = AgentExecutor(
    tools=tools,
    llm=llm,
    agent=o2c_rag_agent,
    verbose=True,
    return_intermediate_steps=True,
    agent_kwargs={
        'prefix': PREFIX,
        'format_instructions': FORMAT_INSTRUCTIONS,
        'suffix': SUFFIX
    }
)


async def execute(query: str):
    # return await agent.ainvoke({"input": query})
    memory = ChatMessageHistory(session_id="test-session")
    agent_with_chat_history = RunnableWithMessageHistory(
        agent,
        lambda session_id: memory,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    return await agent_with_chat_history.ainvoke(
        {"input": query},
        config={"configurable": {"session_id": "<foo>"}},
    )