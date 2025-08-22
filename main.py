import os
import asyncio
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.mongodb import AsyncMongoDBSaver

from graph import graph_builder  # import graph đã định nghĩa


load_dotenv()

DB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/history_chatbot")

# Test MongoDB connection
try:
    client = MongoClient(DB_URI)
    client.admin.command("ping")
    print("✅ Connected to MongoDB")
except Exception as e:
    print(f"❌ Errors in MongoDB: {e}")
    exit(1)


async def main():
    async with AsyncMongoDBSaver.from_conn_string(DB_URI) as checkpointer:
        graph = graph_builder.compile(checkpointer=checkpointer)
        config = {"configurable": {"thread_id": "qh-43"}}

        while True:
            user_input = input("You: ")

            if user_input.lower() == "exit":
                print("👋 exit...")
                break

            input_message = HumanMessage(content=user_input)

            try:
                result = await graph.ainvoke({"messages": [input_message]}, config=config)
                print("Final answer:", result["messages"][-1].content)

            except Exception as e:
                print(f"❌ Errors: {e}")


if __name__ == "__main__":
    asyncio.run(main())
