import time
import unittest
import requests

CHATBOT_URL = "http://chatbot_api:8000/o2c-rag-agent"

questions_date_frequency = [
    "O que a chave DATE representa?",
    "Quais são os possíveis valores para a chave DATE?",
    "Forneça um exemplo de resposta para a chave DATE.",
    "O que a chave FREQUENCY descreve?",
    "Qual é o valor disponível para a chave FREQUENCY?",
    "Forneça um exemplo de resposta para a chave FREQUENCY.",
    "Qual é a descrição da chave CATEGORY?",
    "Liste todos os valores possíveis para a chave CATEGORY.",
    "Forneça um exemplo de resposta para a chave CATEGORY.",
    "O que a chave SALESORDER representa?",
    "Quais são os possíveis valores para a chave SALESORDER?",
    "Forneça um exemplo de resposta para a chave SALESORDER.",
    "Qual é a descrição da chave SYSTEM?",
    "Qual é o valor disponível para a chave SYSTEM?",
    "Forneça um exemplo de resposta para a chave SYSTEM.",
]

request_bodies = [{"text": q} for q in questions_date_frequency]

start_time = time.perf_counter()
outputs = [requests.post(CHATBOT_URL, json=data) for data in request_bodies]
end_time = time.perf_counter()

print(f"Run time: {end_time - start_time} seconds")
