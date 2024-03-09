from typing import Optional, Self

from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories.postgres import PostgresChatMessageHistory

from src.lib.open_api_client import get_open_api_client
from src.config import get_config

class ChatSession():
    def __init__(self, session_id: str, system_message: SystemMessage):
        self.open_api_client = get_open_api_client()
        self.chat = self.open_api_client.chat_model
        self.session_id = session_id

        config = get_config()
        self.chat_history = PostgresChatMessageHistory(self.session_id, connection_string=config.SQLALCHEMY_DATABASE_URI)

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
