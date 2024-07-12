import os
import requests
import streamlit as st

CHATBOT_URL = "http://chatbot_api:8000/agent/agent-local"
#CHATBOT_URL = "http://localhost:8000/assistant/assistant-created"
#CHATBOT_URL = "http://localhost:8000/assistant/assistant-existed"

with st.sidebar:
    st.header("Sobre")
    st.markdown(
        """
        Este chatbot interage com
        [LangChain](https://python.langchain.com/docs/get_started/introduction)
        agente projetado para responder perguntas sobre O2C.
        O agente usa geração aumentada por recuperação (RAG) sobre dados
        estruturados e não estruturados que foram gerados sinteticamente.
        """
    )

    st.header("Perguntas de Exemplo")
    st.markdown("- Informe a quantidade total de ordens de vendas nos 60 últimos dias?")
    st.markdown(
        """- Mostre o montante total financeiro das Ordens de Vendas."""
    )
    st.markdown(
        """- Qual é o montante total financeiro das Ordens de Vendas. """
    )
    st.markdown(
        "- Qual é o valor total das Ordens de Vendas em abril de 2023?"
    )

st.title("<<-- _SYMPHONY_ -->>")
st.title(':sunglasses: :blue[Chatbot Especialista em O2C] :sunglasses:')
st.info(
    """Pergunte-me sobre o conteúdo do arquivo data/datatype_definitions.json"""
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            with st.status("Como isso foi gerado?", state="complete"):
                st.info(message["explanation"])

if prompt := st.chat_input("O que você quer saber?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"text": prompt}

    with st.spinner("Procurando por uma resposta..."):
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            output_text = response.json().get("output", "Nenhuma resposta disponível.")
            explanation = response.json().get("explanation", "Nenhuma explicação disponível.")
        else:
            output_text = """Ocorreu um erro ao processar sua mensagem.
            Por favor, tente novamente ou reformule sua mensagem."""
            explanation = output_text

    st.chat_message("assistant").markdown(output_text)
    st.status("Como isso foi gerado?", state="complete").info(explanation)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            "explanation": explanation,
        }
    )