from langgraph.graph import StateGraph, MessagesState, START, END
from nodes.supervisor import supervisor_node
from nodes.fallback import fallback_node
from nodes.planner import planner_node
from nodes.finalizer import finalizer_node


class ExtendedState(MessagesState):
    decision: str = ""  # save decision of supervisor


# Build graph
graph_builder = StateGraph(ExtendedState)

# Add nodes
graph_builder.add_node("planner", planner_node)
graph_builder.add_node("supervisor", supervisor_node)
graph_builder.add_node("fallback", fallback_node)
graph_builder.add_node("finalizer", finalizer_node)

# Edges
graph_builder.add_edge(START, "planner")

# Conditional edges from Planner
def route_from_planner(state: ExtendedState):
    return state["decision"]  # "supervisor" or "fallback"

graph_builder.add_conditional_edges(
    "planner",
    route_from_planner,
    {"supervisor": "supervisor", "fallback": "fallback"}
)

graph_builder.add_edge("supervisor", "finalizer")
graph_builder.add_edge("finalizer", END)
graph_builder.add_edge("fallback", END)
