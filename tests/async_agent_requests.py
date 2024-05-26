import asyncio
import time

import httpx

CHATBOT_URL = "http://chatbot_api:8000/o2c-rag-agent"


async def make_async_post(url, data):
    timeout = httpx.Timeout(timeout=120)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, timeout=timeout)
        return response


async def make_bulk_requests(url, data):
    tasks = [make_async_post(url, payload) for payload in data]
    responses = await asyncio.gather(*tasks)
    outputs = [r.json()["output"] for r in responses]
    return outputs


questions_stock_financialdocument = [
    "O que a chave STOCK representa?",
    "Qual é o valor disponível para a chave STOCK?",
    "Forneça um exemplo de resposta para a chave STOCK.",
    "O que a chave FINANCIALDOCUMENT descreve?",
    "Quais são os possíveis valores para a chave FINANCIALDOCUMENT?",
    "Forneça um exemplo de resposta para a chave FINANCIALDOCUMENT.",
    "O que a chave PAYMENTSTATUS indica?",
    "Liste os valores disponíveis para a chave PAYMENTSTATUS.",
    "Forneça um exemplo de resposta para a chave PAYMENTSTATUS.",
    "O que são LOGISTICSEVENT e quais são seus possíveis valores?",
    "Qual é a função da chave TIMEUNIT?",
    "Liste um valor e forneça um exemplo de resposta para a chave TIMEUNIT.",
    "Qual é a descrição da chave FINANCIALMETRIC?",
    "Forneça um exemplo de valor para a chave FINANCIALMETRIC.",
    "Qual é a descrição da chave KPI?",
]

request_bodies = [{"text": q} for q in questions_stock_financialdocument]

start_time = time.perf_counter()
outputs = asyncio.run(make_bulk_requests(CHATBOT_URL, request_bodies))
end_time = time.perf_counter()

print(f"Run time: {end_time - start_time} seconds")
