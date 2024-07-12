import os

from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain import hub
from langchain.agents import (
    create_openai_functions_agent,
    AgentExecutor,
)

from src.tools import ToolDefinition

class O2CAgentManagerMongo:
    """
        Uma classe para gerenciar um agente O2C (Order-to-Cash) usando OpenAIAssistantV2Runnable e AgentExecutor.

        Atributos:
        ----------
        model : str
            O modelo a ser usado pelo agente.
        api_key : str
            A chave de API do OpenAI para autenticação.
        tools : list
            Uma lista de ferramentas a serem usadas pelo agente.
        llm : ChatOpenAI
            A instância do modelo de linguagem grande.
        prompt : Any
            O template de prompt para o agente.
        o2c_rag_agent : Any
            O agente O2C RAG inicializado.
        agent_executor : AgentExecutor
            O executor para rodar o agente com as ferramentas e configurações definidas.
        memory : ChatMessageHistory
            O histórico de mensagens do chat para a sessão.
        o2c_rag_agent_executor : RunnableWithMessageHistory
            O executor do agente com histórico de mensagens.

        Métodos:
        -------
        execute(query: str)
            Executa uma consulta usando o executor do agente e retorna o resultado.
    """
    def __init__(self):
        self.model = os.getenv("O2C_AGENT_MODEL", "gpt-3.5-turbo")
        self.api_key = os.getenv('OPENAI_API_KEY')

        self.tools = [
            ToolDefinition().create_mongo_retriever()
        ]

        self.llm = ChatOpenAI(
            model=self.model,
            temperature=0,
            openai_api_key=self.api_key
        )

        self.prompt = hub.pull("hwchase17/openai-functions-agent")

        self.o2c_rag_agent = create_openai_functions_agent(
            llm=self.llm,
            prompt=self.prompt,
            tools=self.tools,
        )

        self.agent_executor = AgentExecutor(
            agent=self.o2c_rag_agent,
            tools=self.tools,
            return_intermediate_steps=True,
            verbose=True
        )

        self.memory = ChatMessageHistory(session_id="test-session")

        self.o2c_rag_agent_executor = RunnableWithMessageHistory(
            self.agent_executor,
            lambda session_id: self.memory,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    async def execute(self, query: str):
        return await self.o2c_rag_agent_executor.ainvoke({"input": query}, config={"configurable": {"session_id": "<foo>"}})