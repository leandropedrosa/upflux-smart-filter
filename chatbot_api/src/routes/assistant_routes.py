from fastapi import HTTPException
from fastapi import APIRouter

from src.assistants.assistant_create import AssistantCreateManager
from src.assistants.assistant_exists import AssistantExistManager
from src.assistants.assistant_scope import AssistantScopeManager
from src.models.o2c_rag_query import O2CQueryOutput, O2CQueryInput
from src.utils.async_utils import async_retry

router = APIRouter(
    prefix="/assistant",
    tags=["ASSISTANT"],
    responses={404: {"description": "Not found"}}
)

@async_retry(max_retries=1, delay=1)
async def invoke_assistant_create_with_retry(query: str):
    manager = AssistantCreateManager()
    return await manager.execute(query)


@async_retry(max_retries=10, delay=1)
async def invoke_assistant_exists_with_retry(query: str):
    assistant_id = "asst_s17OzuRpmIuXgAvgxoKjZ0P0"
    manager = AssistantExistManager(assistant_id=assistant_id)
    return await manager.execute(query)


@async_retry(max_retries=10, delay=1)
async def invoke_assistant_scope_with_retry(query: str):
    manager = AssistantScopeManager()
    return await manager.execute(query)


@async_retry(max_retries=10, delay=1)
async def invoke_assistant_response_with_retry(query: str):
    raise HTTPException(status_code=501, detail="Este endpoint ainda não foi implementado.")

@router.post("/assistant-scope")
async def assistant_scope(
    query: O2CQueryInput,
) -> O2CQueryOutput:
    query_response = await invoke_assistant_scope_with_retry(query.text)
    return O2CQueryOutput(
        input=query.text,
        output=query_response.get("output"),
        intermediate_steps=query_response.get("intermediate_steps", [])
    )

@router.post("/assistant-request")
async def assistant_request(
    query: O2CQueryInput,
) -> O2CQueryOutput:
    raise HTTPException(status_code=501, detail="Este endpoint ainda não foi implementado.")

@router.post("/assistant-response")
async def assistant_response(
    query: O2CQueryInput,
) -> O2CQueryOutput:
    raise HTTPException(status_code=501, detail="Este endpoint ainda não foi implementado.")

@router.post("/assistant-created")
async def assistant_created(
    query: O2CQueryInput,
) -> O2CQueryOutput:
    query_response = await invoke_assistant_create_with_retry(query.text)

    human_input = query.text
    chat_history = [human_input]
    text = query_response

    chat_history_strings = [message for message in chat_history]

    return O2CQueryOutput(
        input=human_input,
        output=text,
        intermediate_steps=chat_history_strings
    )

@router.post("/assistant-existed")
async def assistant_existed(
    query: O2CQueryInput,
) -> O2CQueryOutput:
    query_response = await invoke_assistant_exists_with_retry(query.text)
    return O2CQueryOutput(
        input=query.text,
        output=query_response.get("output"),
        intermediate_steps=query_response.get("intermediate_steps", [])
    )