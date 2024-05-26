from fastapi import FastAPI
from agents.o2c_agente import o2c_rag_agent_executor
from models.o2c_rag_query import O2CQueryInput, O2CQueryOutput
from utils.async_utils import async_retry

app = FastAPI(
    title="Agent O2C Chatbot",
    description="Endpoints for Agent O2C RAG chatbot",
)


@async_retry(max_retries=10, delay=1)
async def invoke_agent_with_retry(query: str):
    """
    Retry the agent if a tool fails to run. This can help when there
    are intermittent connection issues to external APIs.
    """

    return await o2c_rag_agent_executor.ainvoke({"input": query})


@app.get("/")
async def get_status():
    return {"status": "running"}

@app.get("/healthcheck")
async def get_status():
    return {"status": "ok"}

@app.post("/o2c-rag-agent")
async def query_o2c_agent(
    query: O2CQueryInput,
) -> O2CQueryOutput:
    query_response = await invoke_agent_with_retry(query.text)
    query_response["intermediate_steps"] = [
        str(s) for s in query_response["intermediate_steps"]
    ]

    return query_response
