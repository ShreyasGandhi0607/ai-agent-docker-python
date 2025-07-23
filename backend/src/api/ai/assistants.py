from api.ai.llms import get_gemini_llm
from api.ai.tools import (
    send_me_email,
    get_unread_emails
)
from langchain_core.messages import AIMessage

EMAIL_TOOLS = {
    "send_me_email" : send_me_email,
    "get_unread_emails" : get_unread_emails
}

def email_assistant(query:str):
    # llm = llm_base.bind_tools([send_me_email, get_unread_emails])
    llm = get_gemini_llm().bind_tools(list(EMAIL_TOOLS.values()))

    messages = [
        ("system", "You are an helpful assistant for managing my email inbox."),
        ("human", query)
    ]

    response = llm.invoke(messages)
    messages.append(response)

    # Manually handle tool calls if present
    if isinstance(response, AIMessage) and getattr(response, "tool_calls", None):
        results = []
        for tool_call in response.tool_calls:
            name = tool_call.get("name")
            args = tool_call.get("args", {})
            func = EMAIL_TOOLS.get(name)
            if not func:
                continue
            try:
                out = func.invoke(args)
            except Exception as e:
                out = f"Error in {name}: {e}"
            results.append({"tool": name, "result": out})

        # return the tool outputs directly
        return results[0] if len(results) == 1 else results

    # No tools invoked: just return the model’s text reply
    return response.content if hasattr(response, "content") else str(response)