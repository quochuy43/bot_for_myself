from langchain_core.messages import SystemMessage
from utils.config import model
from langgraph.graph import MessagesState

def fallback_node(state: MessagesState):
    messages = state["messages"]
    system_prompt = SystemMessage(
        content=(
            "You are a friendly assistant. If the query is unclear, ask for clarification. "
            "Otherwise, chat naturally."
        )
    )
    response = model.invoke([system_prompt] + messages)
    return {"messages": messages + [response]}