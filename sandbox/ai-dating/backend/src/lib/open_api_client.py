
from typing import Optional

from langchain_openai.llms import OpenAI
from langchain_openai.chat_models import ChatOpenAI

from src.config import get_config

DEFAULT_MODEL = "gpt-4-vision-preview"
MAX_TOKENS = 1000

class OpenAPIClient:
    def __init__(self, model: str=DEFAULT_MODEL):
        config = get_config()
        self.llm = OpenAI(openai_api_key=config.OPEN_API_KEY)
        self.chat_model = ChatOpenAI(model=model, openai_api_key=config.OPEN_API_KEY, max_tokens=MAX_TOKENS)

OPEN_API_CLIENT: Optional[OpenAPIClient] = None

def get_open_api_client() -> OpenAPIClient:
    global OPEN_API_CLIENT
    if OPEN_API_CLIENT is None:
        OPEN_API_CLIENT = OpenAPIClient()
    return OPEN_API_CLIENT
