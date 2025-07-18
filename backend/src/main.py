import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.db import init_db
from api.chat.routing import router as ChatRouter

@asynccontextmanager
async def lifespan(app:FastAPI):
    # before app startup
    init_db()
    yield
    # after app startup


app = FastAPI(lifespan=lifespan)
app.include_router(ChatRouter, prefix="/api/chat")

MY_PROJECT = os.environ.get("MY_PROJECT") or "This is my project"
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise NotImplementedError("'API_KEY' was not sent")

@app.get("/")
def index():
    return {
        'message':"Hello world from fastapi!",
        'project_name':MY_PROJECT,
        "API_KEY" : API_KEY
        }