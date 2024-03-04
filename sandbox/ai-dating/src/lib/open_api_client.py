

from typing import Type, TypeAlias

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage

from src.config import get_config

Message: TypeAlias = AIMessage | HumanMessage | SystemMessage 

def create_message(type: Type[Message], input: str) -> Message:
    return type(content=input)

def create_human_message(input: str) -> HumanMessage:
        content = [ {"type": "text", "text": "Here are the images"}]
        url_dict = {
            "type": "image_url",
            "image_url": {
                "url": input,
                "detail": "auto",
            },
        }
        content.append(url_dict)
        return create_message(HumanMessage, content)

DEFAULT_MODEL = "gpt-4-vision-preview"
MAX_TOKENS = 1000

class OpenAPIClient:
   
    def __init__(self, model: str=DEFAULT_MODEL):
        self.llm = OpenAI()
        self.chat_model = ChatOpenAI(model=model,openai_api_key=get_config().OPEN_API_KEY, max_tokens=MAX_TOKENS)

    def invoke(self, message: Message) -> SystemMessage:
        return self.invoke([message])
    
    def invoke(self, messages: list[Message]) -> SystemMessage:
        result = self.chat_model.invoke(messages)
        return create_message(SystemMessage, result.content)



def get_open_api_client() -> OpenAPIClient:
    global OPEN_API_CLIENT
    if OPEN_API_CLIENT is None:
        OPEN_API_CLIENT = OpenAPIClient()
    return OPEN_API_CLIENT