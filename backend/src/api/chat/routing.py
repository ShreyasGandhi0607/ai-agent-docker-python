from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from .models import ChatModelPayload, ChatModel, ChatModelListItem
from api.db import get_session
from typing import List

router = APIRouter()

# /api/chat
@router.get("/")
def heath_check():
    return {
        "Status" : "OK"
    }

# /api/chat/recents
# curl http://localhost:8000/api/chat/recent
@router.get("/recent/", response_model=List[ChatModelListItem])
def chat_list_messages(session:Session = Depends(get_session)):
    query = select(ChatModel) # sql -> query
    results = session.exec(query).fetchall()[:10]
    return results

# HTTP post -> payload ={"message":"Hello world"}
# curl -X POST -d '{"message":"Hello world"}' -H "Content-Type: application/json" http://localhost:8000/api/chat/
# curl -X POST -d '{"message":"Hello world"}' -H "Content-Type: application/json" https://ai-agent-docker-python.onrender.com/api/chat

@router.post("/", response_model=ChatModelListItem)
def chat_create_message(
    payload : ChatModelPayload,
    session : Session = Depends(get_session)
    ):
    data = payload.model_dump() # pydantic -> dict
    print(data)

    obj = ChatModel.model_validate(data)

    # ready to store in the database
    session.add(obj)
    session.commit()
    session.refresh(obj)   # ensures id/primary key added to the object instance

    return obj