from langchain_core.messages import SystemMessage
from utils.config import model
from langgraph.graph import MessagesState
from agents.math_agent import get_math_agent
from agents.research_agent import get_research_agent

SUPERVISOR_PROMPT = """
You are the Supervisor. Your job is to decide which expert should solve the query.

RULES:
- Output must be exactly one word: MATH or RESEARCH. No explanation.
- MATH = numerical or symbolic calculations, arithmetic, algebra, equations.
- RESEARCH = facts, data lookup, real-world knowledge ("FAANG headcount 2024", "who is the CEO of Google").
- If the query has both math and research, choose RESEARCH.

Answer format: MATH or RESEARCH (uppercase).
"""

def supervisor_node(state: MessagesState):
    messages = state["messages"]
    decision_response = model.invoke([SystemMessage(content=SUPERVISOR_PROMPT)] + messages)
    # decision = decision_response.content.lstrip(": ").strip().lower()
    decision = decision_response.content.strip().lower()
    
    if decision == "math":
        agent = get_math_agent()
    else:
        agent = get_research_agent()
    
    result = agent.invoke({"messages": messages})
    return {"messages": messages + result["messages"]}
