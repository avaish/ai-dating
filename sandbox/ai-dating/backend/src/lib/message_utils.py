from typing import Any, Type, TypeAlias

from langchain_core.prompt_values import ChatPromptValue
from langchain.schema import HumanMessage, AIMessage, SystemMessage

Message: TypeAlias = AIMessage | HumanMessage | SystemMessage
Invokable: TypeAlias = AIMessage | HumanMessage | ChatPromptValue

def create_message(type: Type[Message], input: str) -> Message:
    return type(content=input)

def create_human_message(content: Any) -> HumanMessage:
    return create_message(HumanMessage, content)

def create_system_message(content: Any) -> SystemMessage:
    return create_message(SystemMessage, content)
