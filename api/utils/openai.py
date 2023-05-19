from langchain.llms import OpenAI
from openai.error import RateLimitError

from api.models.settings import settings


llm = OpenAI(openai_api_key=settings.OPEN_AI_API_KEY, temperature=0.7)


def get_openai_response(prompt: str) -> str:
    try:
        return llm(prompt=prompt, )
    except RateLimitError:
        return "Sample OpenAI message, api key exceeded your current quota"
