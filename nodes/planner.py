from langchain_core.messages import SystemMessage
from utils.config import model
from langgraph.graph import MessagesState

PLANNER_PROMPT = """You are the Planner. Your only job is to classify the user query into one of two routes.

    RULES:
    - Output must be exactly one word: either SUPERVISOR or FALLBACK. Do not add explanation.
    - SUPERVISOR = factual or computational tasks (math problems like "3+4", or research questions like "headcount of FAANG").
    - FALLBACK = casual conversation ("How are you?") or unclear/ambiguous queries.

    Think carefully. If any part of the query looks like math or research, choose SUPERVISOR.
    Answer format: SUPERVISOR or FALLBACK (uppercase).
"""

def planner_node(state: MessagesState):
    messages = state["messages"]
    response = model.invoke([SystemMessage(content=PLANNER_PROMPT)] + messages)
    decision = response.content.strip().lower()  # "supervisor" or "fallback"
    return {"messages": messages + [response], "decision": decision}