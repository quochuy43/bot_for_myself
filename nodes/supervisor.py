from langchain_core.messages import SystemMessage
from utils.config import model
from langgraph.graph import MessagesState
from agents.math_agent import get_math_agent
from agents.research_agent import get_research_agent

def supervisor_node(state: MessagesState):
    messages = state["messages"]
    system_prompt = SystemMessage(
        content=(
            "You are a supervisor managing two experts: math_expert and research_expert. "
            "Decide strictly: 'math' for math problems (e.g., '3 + 4'), "
            "'research' for research questions (e.g., 'headcount of FAANG 2024'). "
            "Respond with a single word: 'math' or 'research'."
        )
    )
    decision_response = model.invoke([system_prompt] + messages)
    decision = decision_response.content.strip().lower()
    
    if decision == "math":
        agent = get_math_agent()
    else:
        agent = get_research_agent()
    
    result = agent.invoke({"messages": messages})
    return {"messages": messages + result["messages"]}
