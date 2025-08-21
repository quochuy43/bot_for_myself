from langchain_core.messages import SystemMessage
from utils.config import model
from langgraph.graph import MessagesState

PLANNER_PROMPT = """
You are the Planner. Your only job is to classify the user query into one of two routes.

RULES:
- Output must be exactly one word: either SUPERVISOR or FALLBACK. Do not add explanation.
- SUPERVISOR = factual or computational tasks (math problems like "3+4", or research questions like "headcount of FAANG").
- FALLBACK = casual conversation ("How are you?") or unclear/ambiguous queries.

Think carefully. If any part of the query looks like math or research, choose SUPERVISOR.
Answer format: SUPERVISOR or FALLBACK (uppercase).
"""

PLANNER_PROMPT = """
You are the Planner. Your only job is to classify the user query into one of two routes.

RULES:
- Output must be exactly one word: either SUPERVISOR or FALLBACK. Do not add explanation.
- SUPERVISOR = any query that belongs to one of:
  • Math: numerical/symbolic calculations (e.g., "3+4", "solve x^2+3x+2=0").
  • Research: external facts/web knowledge (e.g., "FAANG headcount 2024", "who is the CEO of Google").
  • Rag: questions about the user's personal knowledge base (about Huy) including: personal information, interests, idols/inspiration, skills, projects, career goals/direction, memorable moments, life philosophy, or contact details.
- FALLBACK = small talk/casual conversation ("How are you?"), chit-chat, opinions not tied to the user’s KB, or unclear/ambiguous queries.

Guidance:
- If any part of the query indicates MATH, RESEARCH or RAG, choose SUPERVISOR.
- Language can be Vietnamese or English; the rules remain the same.

Answer format: SUPERVISOR or FALLBACK (uppercase).
"""

async def planner_node(state: MessagesState):
    messages = state["messages"]
    response = await model.ainvoke([SystemMessage(content=PLANNER_PROMPT)] + messages)
    decision = response.content.strip().lower()  # "supervisor" or "fallback"
    return {"messages": messages + [response], "decision": decision}