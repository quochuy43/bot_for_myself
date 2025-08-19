from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState
from utils.config import model

FINALIZER_PROMPT = """You are the Final Answer Composer.

    Your job: 
    1. Consolidate all outputs from agents into ONE clear, complete answer for the user.
    2. If numbers from agents require further calculation, do it and present the final result.
    3. If crucial info is missing, ask ONE specific clarification question.
    4. Avoid filler or chit-chat. Be concise, factual, and clear.

    Format:
    - If you have enough info → give the final answer.
    - If missing info → ask one clear question.
"""

def finalizer_node(state: MessagesState):
    messages = state["messages"]
    resp = model.invoke([SystemMessage(content=FINALIZER_PROMPT)] + messages)
    return {"messages": messages + [resp]}
