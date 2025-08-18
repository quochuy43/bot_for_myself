from langgraph.graph import StateGraph, MessagesState, START, END
from nodes.supervisor import supervisor_node
from nodes.fallback import fallback_node
from nodes.planner import planner_node
from nodes.finalizer import finalizer_node

# Mở rộng MessagesState để lưu decision từ supervisor
class ExtendedState(MessagesState):
    decision: str = ""  # Lưu quyết định của supervisor

# Build graph
graph_builder = StateGraph(ExtendedState)

# Thêm nodes
graph_builder.add_node("planner", planner_node)
graph_builder.add_node("supervisor", supervisor_node)
graph_builder.add_node("fallback", fallback_node)
graph_builder.add_node("finalizer", finalizer_node)

# Edges 
graph_builder.add_edge(START, "planner")

# Conditional edges từ Planner
def route_from_planner(state: ExtendedState):
    return state["decision"]  # "supervisor" hoặc "fallback"

graph_builder.add_conditional_edges(
    "planner",
    route_from_planner,
    {"supervisor": "supervisor", "fallback": "fallback"}
)

# Từ Fallback, kết thúc
# graph_builder.add_edge("fallback", END)

graph_builder.add_edge("supervisor", "finalizer")
graph_builder.add_edge("finalizer", END)
graph_builder.add_edge("fallback", END)

# Compile graph
graph = graph_builder.compile()

# Chạy ví dụ
if __name__ == "__main__":
    from langchain_core.messages import HumanMessage
    input_message = HumanMessage(content="what's the combined headcount of the FAANG companies in 2024?")
    result = graph.invoke({"messages": [input_message]})
    print(result)
    print(result["messages"][-1].content)