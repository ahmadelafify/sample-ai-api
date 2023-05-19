from pydantic import BaseModel


class BaseAIPayload(BaseModel):
    email: str


class AskAIPayload(BaseAIPayload):
    prompt: str
