from fastapi import APIRouter

from langchain_core.prompts import ChatPromptTemplate


from src.lib.chat_session import ChatSession
from src.lib.image_utils import create_image_message
from src.lib.message_utils import create_system_message
from src.lib.open_api_client import get_open_api_client
from src.lib.prompts import PROFILE_GURU_PROMPT

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{session_id}")
async def do_chat(session_id: str, text: str, image: bool):
    system_message = create_system_message(PROFILE_GURU_PROMPT)
    chat_session = ChatSession(session_id, system_message)
    if image:
        open_api_client = get_open_api_client()
        chat = open_api_client.chat_model

        system_message = create_system_message(PROFILE_GURU_PROMPT)
        human_message = create_image_message()

        PROFILE_GURU_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([system_message, human_message])
        chain = PROFILE_GURU_PROMPT_TEMPLATE | chat
        ai_message = chain.invoke({})
        chat_session.add_ai_message(ai_message)

        print(chat_session.chat_history)
    else:
        ai_message = chat_session.invoke(text)
        print(ai_message)

        print(chat_session.chat_history)
