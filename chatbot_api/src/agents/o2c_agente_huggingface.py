import os
from langchain.agents.format_scratchpad import format_log_to_str
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain import hub
from langchain.agents import (
    AgentExecutor,
)
from langchain.agents.output_parsers import (
    ReActJsonSingleInputOutputParser,
)
from src.tools import ToolDefinition
from langchain.tools.render import render_text_description

class O2CAgentHuggingFaceManager:
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
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

        self.tools = [ToolDefinition().create_json_retriever("rag_assistant_scope.json", name="rag_scopo",
                                                   description="Utilize quando precisar das descrição e os valores possíveis para cada campo")]
        self.llm = HuggingFaceEndpoint(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1")

        self.chat_model = ChatHuggingFace(llm=self.llm)
        self.prompt = hub.pull("hwchase17/react")
        self.prompt = self.prompt.partial(
            tools=render_text_description(self.tools),
            tool_names=", ".join([t.name for t in self.tools]),
        )
        self.chat_model_with_stop = self.chat_model.bind(stop=["\nObservation"])
        self.agent = (
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
                }
                | self.prompt
                | self.chat_model_with_stop
                | ReActJsonSingleInputOutputParser()
        )

        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            return_intermediate_steps=True,
            verbose=True
        )

    async def execute(self, query: str):
        return await self.agent_executor.ainvoke({"input": query}, config={"configurable": {"session_id": "<foo>"}})
