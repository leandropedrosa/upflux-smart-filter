from fastapi import APIRouter

from src.agents.o2c_agente import O2CAgentManager
from src.agents.o2c_agente_huggingface import O2CAgentHuggingFaceManager
from src.agents.o2c_agente_mongo import O2CAgentManagerMongo
from src.models.o2c_rag_query import O2CQueryInput, O2CQueryOutput
from src.utils.async_utils import async_retry

router = APIRouter(
    prefix="/agent",
    tags=["AGENT"],
    responses={404: {"description": "Not found"}}
)

@async_retry(max_retries=2, delay=1)
async def invoke_agent_with_retry(query: str):
    manager = O2CAgentManager()
    return await manager.execute(query)


@async_retry(max_retries=10, delay=1)
async def invoke_agent_mongo_with_retry(query: str):
    manager = O2CAgentManagerMongo()
    return await manager.execute(query)

@async_retry(max_retries=10, delay=1)
async def invoke_agent_hugging_face(query: str):
    manager = O2CAgentHuggingFaceManager()
    return await manager.execute(query)

@router.post("/agent-local")
async def agent_created(
    query: O2CQueryInput,
) -> O2CQueryOutput:
    agent = O2CAgentManager()
    query_response = await agent.execute(query.text, query.session_id)
    query_response["intermediate_steps"] = [
        str(s) for s in query_response["intermediate_steps"]
    ]

    return query_response


@router.post("/agent-mongo")
async def agent_created(
    query: O2CQueryInput,
) -> O2CQueryOutput:
    query_response = await invoke_agent_mongo_with_retry(query.text)
    query_response["intermediate_steps"] = [
        str(s) for s in query_response["intermediate_steps"]
    ]

    return query_response


@router.post("/agent-huggingface")
async def agent_created(
    query: O2CQueryInput,
) -> O2CQueryOutput:
    query_response = await invoke_agent_hugging_face(query.text)
    query_response["intermediate_steps"] = [
        str(s) for s in query_response["intermediate_steps"]
    ]

    return query_response