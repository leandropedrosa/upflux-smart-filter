import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

template='''
            Você é um assistente especializado em O2C. Sua única missão é criar uma \
            estrutura JSON com base na pergunta do usuário {input}, \
            utilize o histórico da conversa {history} para preencher cada campo do exemplo abaixo: \
            {data_output}
            Esta é a descrição e os valores possíveis para cada campo: \
            {data_structure}
            Utilize a descrição e os valores possíveis para cada campo para fazer sugestões com exemplos em português se a pergunta do usuário não fornecer todas as \
            informações necessárias para completar o JSON. Faça uma sugestão oferecendo opções curtas com o único propósito de \
            completar a estrutura. Conduza a conversa apenas para preencher os campos do JSON. Pergunte de maneira amigável, \
            um campo de cada vez. Quando a pergunta não for relacionada ao seu objetivo, você deve direcionar a conversa para o seu objetivo sem termos técnicos. \
            O campo main_keywords são coletadas no final da conversa utilizando o histórico. 
            
            {key} {type} {agent_scratchpad}
            '''

store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

class AssistantCreateManager:
    def __init__(self):
        self.model = ChatOpenAI(model=os.getenv("O2C_AGENT_MODEL", "gpt-3.5-turbo"), temperature=0,
                           openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.prompt_template = ChatPromptTemplate(
            input_variables=["key", "type", "agent_scratchpad", "history", "input"]
        ).from_messages(
            [
                ("system", template),
                ("human", "Respond to the question: {input}")
            ]
        )

    async def execute(self, query: str, session_id: str = None):
        runnable = self.prompt_template | self.model
        with_message_history = RunnableWithMessageHistory(
            runnable,
            get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        return await with_message_history.ainvoke({"input": query}, config={"configurable": {"session_id": "abc123"}})