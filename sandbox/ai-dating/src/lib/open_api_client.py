
import base64
from typing import Optional, Type, TypeAlias

from langchain_core.prompt_values import ChatPromptValue
from langchain_openai.llms import OpenAI
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage

from src.config import get_config

Message: TypeAlias = AIMessage | HumanMessage | SystemMessage
Invokable: TypeAlias = AIMessage | HumanMessage | ChatPromptValue

def encode_image(name: str) -> bytes:
    image_path = f"/app/images/{name}"
    with open(image_path, mode="rb") as image_file:
        return base64.b64encode(image_file.read()).decode(encoding="utf-8")

def create_message(type: Type[Message], input: str) -> Message:
    return type(content=input)

def create_human_message(inputs: list[str]) -> HumanMessage:
        content = [ {"type": "text", "text": "Here are the images"}]
        for input_ in inputs:
            base64_image = encode_image(input_)
            url_dict = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                },
            }
            content.append(url_dict)
        return create_message(HumanMessage, content)

DEFAULT_MODEL = "gpt-4-vision-preview"
MAX_TOKENS = 1000

class OpenAPIClient:

    def __init__(self, model: str=DEFAULT_MODEL):
        config = get_config()
        self.llm = OpenAI(openai_api_key=config.OPEN_API_KEY)
        self.chat_model = ChatOpenAI(model=model, openai_api_key=config.OPEN_API_KEY, max_tokens=MAX_TOKENS)

    def invoke(self, invokable: Invokable) -> SystemMessage:
        return self.invoke([invokable])

    def invoke(self, invokables: list[Invokable]) -> SystemMessage:
        result = self.chat_model.invoke(invokables)
        return create_message(SystemMessage, result.content)


OPEN_API_CLIENT: Optional[OpenAPIClient] = None

def get_open_api_client() -> OpenAPIClient:
    global OPEN_API_CLIENT
    if OPEN_API_CLIENT is None:
        OPEN_API_CLIENT = OpenAPIClient()
    return OPEN_API_CLIENT
