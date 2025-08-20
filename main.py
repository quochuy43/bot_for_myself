from langgraph.graph import StateGraph, MessagesState, START, END
from nodes.supervisor import supervisor_node
from nodes.fallback import fallback_node
from nodes.planner import planner_node
from nodes.finalizer import finalizer_node
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

class ExtendedState(MessagesState):
    decision: str = ""  # save decision of supervisor

# Build graph
graph_builder = StateGraph(ExtendedState)
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

# DB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/history_chatbot")
# try:
#     client = MongoClient(DB_URI)
#     client.admin.command('ping')
#     print("Connect mongo successfully!")
# except Exception as e:
#     print(f"Errors in MongoDB: {e}")
#     exit(1)


# with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
graph = graph_builder.compile()

if __name__ == "__main__":

    config = {"configurable": {"thread_id": "lvqh-43"}}

    while True:
        user_input = input("You: ")

        # what's the combined headcount of the FAANG companies in 2024?

        if user_input.lower() == 'exit':
            print("exit...")
            break
        
        input_message = HumanMessage(content=user_input)
        
        try:
            result = graph.invoke({"messages": [input_message]})
            print("Final answer:", result["messages"][-1].content)
            
        except Exception as e:
            print(f"Errors: {e}")