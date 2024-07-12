from langchain_community.agents.openai_assistant import OpenAIAssistantV2Runnable
from langchain.agents import AgentExecutor
from langchain.tools import DuckDuckGoSearchRun

class AssistantExistManager:
    """
        Uma classe para gerenciar um assistente OpenAI usando OpenAIAssistantV2Runnable e AgentExecutor.

        Atributos:
        ----------
        tools : list
            Uma lista de ferramentas a serem usadas pelo assistente.
        assistant_id : str
            O ID do assistente.
        agent : OpenAIAssistantV2Runnable
            O assistente inicializado.
        exists_assistant_executor : AgentExecutor
            O executor para rodar o assistente com as ferramentas e configurações definidas.

        Métodos:
        -------
        async execute(query: str)
            Executa uma consulta usando o executor do assistente e retorna o resultado.
    """
    def __init__(self, assistant_id: str):
        self.tools = [DuckDuckGoSearchRun()]
        self.assistant_id = assistant_id
        self.agent = OpenAIAssistantV2Runnable(assistant_id=self.assistant_id, as_agent=True)
        self.exists_assistant_executor = AgentExecutor(
            agent=self.agent,
            tools=[],
            return_intermediate_steps=True,
            verbose=True
        )

    async def execute(self, query: str):
        return await self.exists_assistant_executor.ainvoke({"content": query})