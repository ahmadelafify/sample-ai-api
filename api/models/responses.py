from pydantic import BaseModel


class BaseAIPayload(BaseModel):
    email: str


class GetAIHistoryPayload(BaseAIPayload):
    pass


class AskAIPayload(BaseAIPayload):
    prompt: str
