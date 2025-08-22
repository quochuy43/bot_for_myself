from langchain_core.messages import SystemMessage
from utils.config import model
from langgraph.graph import MessagesState

PLANNER_PROMPT = """
You are the Planner. Your only job is to classify the user query into one of two routes.

RULES:
- Output must be exactly ONE WORD ONLY: either SUPERVISOR or FALLBACK.
- SUPERVISOR: any question about Huy's personal profile, biography, interests, skills, projects, career goals, philosophies, memorable moments, or contact information
- FALLBACK: small talk, chit-chat, casual conversation, opinions not tied to Huy, or unclear/ambiguous queries.

Answer format: SUPERVISOR or FALLBACK (uppercase)
"""

async def planner_node(state: MessagesState):
    messages = state["messages"]
    response = await model.ainvoke([SystemMessage(content=PLANNER_PROMPT)] + messages)
    decision = response.content.strip().lower()  # "supervisor" or "fallback"
    return {"messages": messages + [response], "decision": decision}