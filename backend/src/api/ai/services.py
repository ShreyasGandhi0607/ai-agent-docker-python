from api.ai.schemas import EmailMessageSchema
from api.ai.llms import get_gemini_llm

def generate_email_message(query: str):
    llm_base = get_gemini_llm()
    llm = llm_base.with_structured_output(EmailMessageSchema)

    messages = [
        (
            "system",
            "You are a helpful assistant for research and composing plaintext emails. Do not use markdown in your response, only plaintext."
        ),
        (
            "human",
            f"{query}. Do not use markdown in your response only plaintext."
        )
    ]

    response = llm.invoke(messages)


    # If the model returns a list (sometimes happens), extract the first item
    # if isinstance(response, list):
    #     response = response[0]
    return response
    
