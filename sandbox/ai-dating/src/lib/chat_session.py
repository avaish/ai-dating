from typing import Optional, Self

from langchain.memory import ChatMessageHistory
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from src.lib.open_api_client import get_open_api_client

class ChatSession():
    @staticmethod
    def get_or_create(session_id: str, system_message: SystemMessage) -> Self:
        if session_id in CHAT_SESSIONS:
            return CHAT_SESSIONS[session_id]
        chat_session = ChatSession(session_id, system_message)
        CHAT_SESSIONS[session_id] = chat_session
        return chat_session

    def __init__(self, session_id: str, system_message: SystemMessage):
        self.open_api_client = get_open_api_client()
        self.chat = self.open_api_client.chat_model
        self.session_id = session_id
        self.chat_history = ChatMessageHistory()

        prompt = ChatPromptTemplate.from_messages(
            [
                system_message,
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )
        chain = prompt | self.chat
        self.chain_with_message_history = RunnableWithMessageHistory(
            chain,
            lambda session_id: self.chat_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    def add_ai_message(self, ai_message: AIMessage):
        self.chat_history.add_ai_message(ai_message)

    def invoke(self, input_: str) -> AIMessage:
        return self.chain_with_message_history.invoke(
            {"input": input_},
            {"configurable": {"session_id": self.session_id}}
        )

CHAT_SESSIONS = {}
