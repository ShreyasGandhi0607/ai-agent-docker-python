from api.ai.llms import get_gemini_llm
from langchain_core.messages import AIMessage
from api.ai.tools import (
    send_me_email,
    get_unread_emails
)
from api.ai.services import generate_email_message  # assume this exists

EMAIL_TOOLS = {
    "send_me_email" : send_me_email,
    "get_unread_emails" : get_unread_emails
}

def email_assistant(query: str):
    llm_base = get_gemini_llm()
    llm = llm_base.bind_tools(list(EMAIL_TOOLS.values()))

    messages = [
        (
            "system",
            "You are an AI assistant that helps manage a user's inbox. "
            "You can send emails using the `send_me_email` tool, and check unread emails with `get_unread_emails`. "
            "Use tools when appropriate. If needed, ask for more details or create them."
        ),
        ("human", query)
    ]

    response = llm.invoke(messages)
    messages.append(response)

        # Existing tool call handling...
    if hasattr(response, "tool_calls") and response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call.get("name")
            tool_func = EMAIL_TOOLS.get(tool_name)

            if not tool_func:
                continue

            if tool_name == "send_me_email":
                generated = generate_email_message(query)
                subject = generated.subject or "No Subject"
                content = generated.content or "No content"
                tool_result = tool_func.invoke({"subject": subject, "content": content})
            else:
                tool_result = tool_func.invoke()

            messages.append(AIMessage(content=str(tool_result)))

        final_response = llm.invoke(messages)
        return final_response

    # ✅ NEW: If LLM doesn't call tools, do it manually
    else:
        generated = generate_email_message(query)
        subject = generated.subject or "No Subject"
        content = generated.content or "No content"
        tool_result = send_me_email.invoke({"subject": subject, "content": content})
        return AIMessage(content=f"Email sent with subject: {subject}")