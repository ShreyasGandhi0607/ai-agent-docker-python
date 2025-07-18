from sqlmodel import SQLModel, Field

class ChatModelPayload(SQLModel):
    # kind of pydantic model for validation
    message : str

class ChatModel(SQLModel, table = True):
    # this is for saving into the table , and the CRUD operations to perform on 
    id : int | None = Field(default=None, primary_key=True)
    message : str
