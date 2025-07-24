from langgraph.prebuilt import create_react_agent
from api.ai.llms import get_gemini_llm
from api.ai.tools import send_me_email, get_unread_emails, research_email
from langgraph_supervisor import create_supervisor, create_handoff_tool

EMAIL_TOOLS_LIST = [send_me_email, get_unread_emails]


def get_email_assistant():
    model = get_gemini_llm()
    email_agent = create_react_agent(
    model=model,
    tools=[send_me_email, get_unread_emails],
    name="email_agent",
    prompt="""
    You are an email assistant.

    - To send an email, use the `send_me_email` tool.
    - You will be given a "subject" and "body" from the supervisor.
    - Do not just reply with confirmation. Instead, invoke the `send_me_email` tool with the provided subject and body.
    - You can also use `get_unread_emails` to check recent messages.
    """
)

    return email_agent

def get_research_assistant():
    model = get_gemini_llm()
    research_agent = create_react_agent(
    model=model,
    tools=[research_email],
    name="research_agent",
    prompt="""
    You are a research agent. Use only the `research_email` tool to look up information. 
    Once you have the result, return it as-is (do not modify or rephrase it). 
    Make sure the returned result is a structured dictionary with "subject" and "body" fields.

    DO NOT try to send the email yourself.
    """
)

    return research_agent 



# supe = get_supervisor()
# supe.invoke({"messages":[{"role":"user","content":"Find how to create a latte and then email me the result"}]})
# 3. Supervisor: handles coordination logic
def get_supervisor():
    model = get_gemini_llm()
    
    email_agent = get_email_assistant()
    research_agent = get_research_assistant()

    supervisor_prompt = """
    You are a supervisor agent who can delegate tasks to sub-agents.

    - If the user asks to "check" or "read" emails, or asks for unread or recent emails, delegate the task to the email_agent.
    - If the user asks to research a topic, extract the topic and delegate it to the research_agent.
    - Wait for the research_agent’s response, then extract "subject" and "body" fields from the result.
    - Finally, send the email using the email_agent with that subject and body.

    Only call one sub-agent at a time. Wait for a sub-agent’s result before proceeding to the next step.
    """

    supe = create_supervisor(
        agents=[email_agent, research_agent],
        model=model,
        prompt=supervisor_prompt,
    ).compile()

    return supe

