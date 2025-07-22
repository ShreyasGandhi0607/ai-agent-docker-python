from sqlmodel import SQLModel, Field, DateTime
from datetime import datetime, timezone

def get_utc_now():
    return datetime.now().replace(tzinfo=timezone.utc)

class ChatModelPayload(SQLModel):
    # kind of pydantic model for validation
    message : str

class ChatModel(SQLModel, table = True):
    # this is for saving into the table , and the CRUD operations to perform on 
    id : int | None = Field(default=None, primary_key=True)
    message : str
    created_at : datetime = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),# sqlalchemy
        primary_key=False, # if using timescaledb u can keep primary key true
        nullable=False 
    )

class ChatModelListItem(SQLModel):
    id : int | None = Field(default=None)
    message : str
    created_at : datetime = Field(
        default=None
    )