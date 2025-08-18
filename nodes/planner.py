from langchain_core.messages import SystemMessage
from utils.config import model
from langgraph.graph import MessagesState

def planner_node(state: MessagesState):
    messages = state["messages"]
    system_prompt = SystemMessage(
        content=(
            "As a planner, your role is to determine the appropriate course of action for a user query. "
            "Analyze the query and classify it into one of the following two categories: "
            "'supervisor' for queries that require a factual or computational response, such as math problems (e.g., '3 + 4') and research questions (e.g., 'headcount of FAANG'). "
            "'fallback' for queries that are conversational (e.g., 'How are you?') or unclear. "
            "Your response must be a single word: either 'supervisor' or 'fallback'."
        )
    )
    response = model.invoke([system_prompt] + messages)
    decision = response.content.strip().lower()  # "supervisor" hoặc "fallback"
    return {"messages": messages + [response], "decision": decision}