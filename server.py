from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.mongodb import AsyncMongoDBSaver
from pymongo import MongoClient
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import os
from graph import graph_builder 

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

# Input schema
class ChatRequest(BaseModel):
    user_id: str   # = thread_id
    message: str   

# Global vars
checkpointer: AsyncMongoDBSaver = None
graph = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global checkpointer, graph
    # 👉 mở context bằng async with
    async with AsyncMongoDBSaver.from_conn_string(DB_URI) as saver:
        checkpointer = saver
        graph = graph_builder.compile(checkpointer=checkpointer)
        print("🚀 Chatbot graph ready")
        yield
        print("🛑 Closed MongoDB saver")

app = FastAPI(title="Chatbot API", lifespan=lifespan)

@app.post("/chat")
async def chat(request: ChatRequest):
    config = {"configurable": {"thread_id": request.user_id}}
    input_message = HumanMessage(content=request.message)

    try:
        result = await graph.ainvoke({"messages": [input_message]}, config=config)
        final_answer = result["messages"][-1].content
        return {"answer": final_answer}
    except Exception as e:
        return {"error": str(e)}
