from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from .models import ChatModelPayload, ChatModel, ChatModelListItem
from api.db import get_session
from typing import List
from api.ai.agents import get_supervisor
from api.ai.services import generate_email_message
from api.ai.schemas import EmailMessageSchema, SupervisorMessageSchema
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
# curl -X POST -d '{"message":"Give me the summary of why is it better to go outside"}' -H "Content-Type: application/json" http://localhost:8000/api/chat/
# curl -X POST -d '{"message":"Give me the summary of why is it better to go outside"}' -H "Content-Type: application/json" https://ai-agent-docker-python.onrender.com/api/chat

# curl -X POST -d '{"message": "Research why it is good to go outside and email me the results"}' -H "Content-Type: application/json" http://localhost:8080/api/chat/
# curl -X POST -d '{"message": "Research what is the best type of food in different parts of the world and email me the results"}' -H "Content-Type: application/json" https://ai-agent-docker-python.onrender.com/api/chat/


@router.post("/", response_model=SupervisorMessageSchema)
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
    supe = get_supervisor()
    msg_data = {
        "messages" : [
           { 
            "role" : "user",
            "content" : f"{payload.message}"
            },
        ]
    }
    results = supe.invoke(msg_data)
    if not results:
        raise HTTPException(status_code=400,detail="Error with Supervisor")
    
    messages = results.get("messages")
    if not messages:
        raise HTTPException(status_code=400,detail="Error with Supervisor")
    # session.refresh(obj)   # ensures id/primary key added to the object instance

    return messages[-1]