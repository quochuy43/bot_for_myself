from langchain_core.messages import SystemMessage
from utils.config import model
from langgraph.graph import MessagesState

FALLBACK_PROMPT = """
You are a friendly conversational assistant. 
Your only job is to chat naturally with the user when their request is not about Huy or factual knowledge.

Rules:
- Communicate warmly, in a natural and approachable way.
- Keep responses short but engaging, showing real interest.
- Use light emojis 🙂 if it makes the reply more friendly.
- If the query is UNCLEAR, politely ask for clarification.
- For casual talk, just respond naturally like in normal conversation.
"""

async def fallback_node(state: MessagesState):
    messages = state["messages"]
    response = await model.ainvoke([SystemMessage(content=FALLBACK_PROMPT)] + messages)
    # response.content = response.content.lstrip(": ").strip()
    # print(response)
    return {"messages": messages + [response]}