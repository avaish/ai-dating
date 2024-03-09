from fastapi import APIRouter, Depends, HTTPException
from langchain.chains import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.memory import ChatMessageHistory
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables.history import RunnableWithMessageHistory


from src.models.posts import Post, create_post_repository
from src.models.users import User, create_user_repository
from src.lib.open_api_client import get_open_api_client
from src.lib.message_utils import create_human_message, create_system_message
from src.lib.image_utils import create_image_message
from src.lib.prompts import PROFILE_GURU_PROMPT


from src.models.base_model import Repository

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

fake_posts_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

class CustomRetriever(BaseRetriever):
    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> list[Document]:
        return [Document(page_content=query)]

@router.get("/{session_id}")
async def read_posts(session_id: str, post_repository: Repository[Post] = Depends(create_post_repository)):
    open_api_client = get_open_api_client()
    chat = open_api_client.chat_model

    system_message = create_system_message(PROFILE_GURU_PROMPT)
    human_message = create_image_message()

    chat_history = ChatMessageHistory()

    PROFILE_GURU_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([system_message, human_message])
    chain = PROFILE_GURU_PROMPT_TEMPLATE | chat
    ai_message = chain.invoke({})
    print(ai_message)

    chat_history.add_ai_message(ai_message)

    prompt = ChatPromptTemplate.from_messages(
        [
            system_message,
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )
    chain = prompt | chat

    chain_with_message_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: chat_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    ai_message = chain_with_message_history.invoke(
        {"input": "I love programming."},
        {"configurable": {"session_id": session_id}}
    )
    print(ai_message)

    ai_message = chain_with_message_history.invoke(
        {"input": "I volunteer for an animal shelter"},
        {"configurable": {"session_id": session_id}}
    )
    print(ai_message)

    ai_message = chain_with_message_history.invoke(
        {"input": "I own a yacht"},
        {"configurable": {"session_id": session_id}}
    )
    print(ai_message)

    print(chat_history.messages)


    return post_repository.list()

    # return fake_posts_db


@router.get("/{post_id}")
async def read_post(post_id: str):
    if post_id not in fake_posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"name": fake_posts_db[post_id]["name"], "post_id": post_id}


@router.put(
    "/{post_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_post(post_id: str, post_repository: Repository[Post] = Depends(create_post_repository)):
    if post_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": post_id, "name": "The great Plumbus"}
