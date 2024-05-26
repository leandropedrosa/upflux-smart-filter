import os

import requests
import streamlit as st

CHATBOT_URL = os.getenv(
    "CHATBOT_URL", "http://chatbot_api:8000/o2c-rag-agent"
)

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
    st.markdown("- Mostre a taxa de impacto de itens de ordens de vendas Indústria na Cancelados")
    st.markdown(
        """- Qual é a taxa de impacto de itens de ordens de vendas Distr. Industrial no canal de distribuição Cancelados em abril de 2023?"""
    )
    st.markdown(
        """- Informe qual é o impacto gerado pelo total de itens de ordens de vendas por organização de venda."""
    )
    st.markdown(
        "- Diga quanto é a porcentagem de itens de ordens de vendas afetada por organização de venda."
    )


st.title("Chatbot Especialista em O2C")
st.info(
    """Pergunte-me sobre a taxa de impacto de itens de ordens de vendas por organização de venda?"""
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            with st.status("Como isso foi gerado", state="complete"):
                st.info(message["explanation"])

if prompt := st.chat_input("O que você quer saber?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"text": prompt}

    with st.spinner("Procurando por uma resposta..."):
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            output_text = response.json()["output"]
            explanation = response.json()["intermediate_steps"]

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
