from abc import ABC

from pydantic import Field
from pymongo.collection import Collection

from api.schemas.base import BaseDBModel
from api.utils.mongo import database


class PromptResponse(BaseDBModel, ABC):
    email: str = Field(None, description="Email of prompt author")
    prompt: str = Field(None, description="Prompt message")
    openai_response: str = Field(None, description="OpenAI prompt response")

    @classmethod
    def _get_collection(cls) -> Collection:
        return database['prompt_responses']
