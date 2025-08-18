from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState
from utils.config import model

def finalizer_node(state: MessagesState):
    messages = state["messages"]
    system_prompt = SystemMessage(
        content=(
            "As the Final Answer Composer, you will synthesize information from the conversation and outputs from "
            "specialist agents (e.g., math_expert, research_expert) to produce a definitive response. "
            "Follow these rules for your final answer: "
            "1. **Consolidate:** Combine all relevant information into a single, cohesive answer. "
            "2. **Calculate:** If specialist outputs contain numbers that require a final calculation, perform it and provide the result. "
            "3. **Clarify:** If crucial information is missing, state a single, specific question to get the needed details. "
            "Do not provide incomplete answers or conversational filler."
        )
    )
    resp = model.invoke([system_prompt] + messages)
    return {"messages": messages + [resp]}
