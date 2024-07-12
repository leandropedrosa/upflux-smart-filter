from pydantic import BaseModel


class O2CQueryInput(BaseModel):
    text: str
    session_id: str = None


class O2CQueryOutput(BaseModel):
    input: str
    output: str
    intermediate_steps: list[str] = None
