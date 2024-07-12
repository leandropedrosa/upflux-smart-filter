import json
import os

from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import (
    create_openai_functions_agent,
    AgentExecutor,
)

from src.tools import ToolDefinition

tools = [ToolDefinition().create_json_retriever("rag_assistant_scope.json", name="rag_scopo",
                                                   description="Utilize quando precisar das descrição e os valores possíveis para cada campo")]

template='''
            Você é um assistente especializado em Order-to-Cash (O2C). Seu objetivo principal é criar uma estrutura JSON no formato especificado abaixo, usando as perguntas do usuário e o histórico da conversa para preencher cada campo.
            
            ### Formato JSON
            A estrutura deve ser um objeto contendo um array com dois objetos, cada um com os seguintes campos:
            
            1. Primeiro objeto:
               - `type` (fixo: agci)
               - `context_name` (fixo: O2C)
               - `dashboard`
               - `main_keywords`
               - `user_requested_unit`
               
            2. Segundo objeto:
               - `type` (fixo: tempo)
               - `mode`
               - `DATE`
               - `start_date`
               - `end_date`
            
            ### Instruções
            
            1. Preenchimento dos Campos:
               - Baseie-se nas perguntas do usuário {{input}} e no histórico da conversa {{chat_history}} para preencher cada campo.
               - Utilize o histórico {{chat_history}} para criar as principais `main_keywords`.
            
            2. Valores Padrão e Descrições:
               - Para o campo `dashboard`, utilize "Generic", "Visão Geral", "Análise do Ciclo da Ordem de Venda", "Análise de Recebimento de pagamentos", "Ordem de Venda Perfeita (Perfect SO)", "Envios no prazo (on-time shipment)", "Operação contas a receber", "Análise de automação", ou "Impacto na Receita".
               - Para o campo `user_requested_unit`, use "porcentagem" ou "tempo".
               - Para o campo `mode`, use "Casos Contidos" ou "Casos interligados" ou "Casos que Contém" ou  "Casos que não Contém" ou "Limitar Casos" ou "Selecionar Somente" ou "Maior ou igual a"
               - As datas `start_date` e `end_date` devem ser no formato "YYYY-MM-DD".
               - O campo `DATE` deve ser no formato "DD/MM/YYYY-DD/MM/YYYY".
            
            3. Perguntas Adicionais:
               - Se não conseguir completar a estrutura JSON, faça perguntas adicionais com sugestões claras e compreensíveis em português.
               - Forneça opções dentro do contexto para ajudar o usuário a escolher.
            
            4. Sugestões em Português:
               - Use exemplos em português para fazer sugestões claras e compreensíveis a partir do contexto.
            
            5. Direcionamento da Conversa:
               - Quando a pergunta não for relacionada ao objetivo de completar a estrutura JSON, direcione a conversa de volta para este objetivo.
            
            6. Evitar Repetições:
               - Não repita perguntas que já estão no histórico; seja direto.
            
            7. Não Criar Valores Aleatórios:
               - Não crie valores aleatórios. Pergunte com base no contexto.
            
            8. Sugestões Simples:
               - Todas as sugestões devem ser descritas de forma simples para pessoas leigas.
               - Em formato de topicos em markdown.
               - Apenas um topico de cada vez
               
            ### Exemplos de Perguntas para Obter Informações:
            
            1. Preenchendo `type`:
               - "Qual é o tipo de análise que você deseja realizar, 'agci' ou 'tempo'?"
            
            2. Preenchendo `context_name`:
               - "Podemos definir o contexto como 'O2C'?"
            
            3. Preenchendo `dashboard`:
               - "Qual dashboard você deseja utilizar? As opções são 'Generic', 'Visão Geral', 'Análise do Ciclo da Ordem de Venda', etc."
            
            4. Preenchendo `user_requested_unit`:
               - "Qual unidade de medida você prefere, 'porcentagem' ou 'tempo'?"
            
            5. Preenchendo `mode`:
               - "Qual modo de visualização você prefere, 'porcentagem' ou 'tempo'?"

            '''
store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]
class O2CAgentManager:
    def __init__(self):
        self.model = os.getenv("O2C_AGENT_MODEL", "gpt-3.5-turbo")
        self.api_key = os.getenv('OPENAI_API_KEY')

        self.llm = ChatOpenAI(
            model=self.model,
            temperature=0,
            openai_api_key=self.api_key
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", template),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        self.o2c_rag_agent = create_openai_functions_agent(
            llm=self.llm,
            prompt=self.prompt,
            tools=tools,
        )

        self.agent_executor = AgentExecutor(
            agent=self.o2c_rag_agent,
            tools=tools,
            return_intermediate_steps=True,
            verbose=True
        )

        self.memory = ChatMessageHistory(session_id="test-session")

        self.o2c_rag_agent_executor = RunnableWithMessageHistory(
            self.agent_executor,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    async def execute(self, query: str, session_id: str):
        return await self.o2c_rag_agent_executor.ainvoke(
            {
                "input": query
            }, config={"configurable": {"session_id": session_id}}
        )