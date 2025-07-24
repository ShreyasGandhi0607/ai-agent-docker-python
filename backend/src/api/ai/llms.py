import os
from langchain_google_genai import ChatGoogleGenerativeAI

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise NotImplementedError("`GOOGLE_API_KEY` is required")



def get_gemini_llm():
    gemini_params = {
        "model" : "gemini-2.0-flash",
        "api_key" : GOOGLE_API_KEY,
    }

    return ChatGoogleGenerativeAI(**gemini_params)

