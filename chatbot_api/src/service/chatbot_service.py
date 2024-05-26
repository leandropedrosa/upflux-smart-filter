
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_community.chat_message_histories.upstash_redis import (
    UpstashRedisChatMessageHistory,
)
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

model = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.6
)

template = """Você é um assistente especializado em O2C, responda as perguntas sobre o processo e suas subáreas de
				forma concisa, considerando que todos os termos entre colchetes são variáveis.
				Para solicitações de valor financeiro, considere Real Brasileiro(R$).
				Para solicitações de intervalos de datas, considere data atual como: 01.
				Se solicitado intervalo com data de início maior que hoje, use o ano passado.
				tilize o ano atual como:2024.Ex: Semestre atual inicia em 01/
			    25 de Maio de 2024. Antes de responder, arredondar os
				ecimais a duas casas decimais e utilizar o formato para números do Brasil: XXX.XXX.XXX,XX"""

prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])


URL = "https://flowing-bonefish-50764.upstash.io"
TOKEN ="AcZMAAIncDE2MmQ3MjI2ZGVhYjE0MDJiOTAwMjIzMGExZGRkN2YxNnAxNTA3NjQ"
history = UpstashRedisChatMessageHistory(
    url=URL, token=TOKEN, ttl=500, session_id="chat1"
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    chat_memory=history,
)

# chain = prompt | model
chain = LLMChain(
    llm=model,
    prompt=prompt,
    verbose=True,
    memory=memory
)