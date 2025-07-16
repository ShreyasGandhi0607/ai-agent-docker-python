from fastapi import FastAPI
import requests
import os

app = FastAPI()

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