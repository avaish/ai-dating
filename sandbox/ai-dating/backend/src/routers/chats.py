from enum import Enum

from fastapi import APIRouter
from langchain_core.prompts import ChatPromptTemplate

from src.lib.chat_session import ChatSession
from src.lib.image_utils import create_image_message
from src.lib.message_utils import create_system_message
from src.lib.open_api_client import get_open_api_client
from src.lib.prompts import BANTER_GURU_PROMPT, PROFILE_GURU_PROMPT

class ChatMode(Enum):
    BANTER = "banter"
    PROFILE_CREATION = "profile-creation"

CHAT_MODE_TO_PROMPT = {
    ChatMode.BANTER: BANTER_GURU_PROMPT,
    ChatMode.PROFILE_CREATION: PROFILE_GURU_PROMPT
}


router = APIRouter(
    prefix="/chats",
    tags=["chats"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{session_id}:image")
async def do_chat(session_id: str, chat_mode: ChatMode = ChatMode.PROFILE_CREATION):
    open_api_client = get_open_api_client()
    chat = open_api_client.chat_model

    system_message = create_system_message(CHAT_MODE_TO_PROMPT[chat_mode])
    human_message = create_image_message()

    prompt = ChatPromptTemplate.from_messages([system_message, human_message])
    chain = prompt | chat
    ai_message = chain.invoke({})

    chat_session = ChatSession(session_id, system_message)
    chat_session.add_ai_message(ai_message)
    print(ai_message)


@router.get("/{session_id}")
async def do_chat(session_id: str, text: str, chat_mode: ChatMode = ChatMode.PROFILE_CREATION):
    system_message = create_system_message(CHAT_MODE_TO_PROMPT[chat_mode])
    chat_session = ChatSession(session_id, system_message)
    ai_message = chat_session.invoke(text)

    print(ai_message)

    print(chat_session.chat_history)
