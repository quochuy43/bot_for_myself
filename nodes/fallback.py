from langchain_core.messages import SystemMessage
from utils.config import model
from langgraph.graph import MessagesState

FALLBACK_PROMPT = """You are a friendly fallback assistant.

    RULES:
    - If the query is unclear → politely ask the user for clarification.
    - If it is casual conversation → respond naturally and briefly.
    - Do NOT attempt math or research here. That is the job of other agents.
"""

def fallback_node(state: MessagesState):
    messages = state["messages"]
    response = model.invoke([SystemMessage(content=FALLBACK_PROMPT)] + messages)
    return {"messages": messages + [response]}