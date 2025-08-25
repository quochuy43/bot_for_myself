from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import MessagesState
from utils.config import model

FINALIZER_PROMPT = """
You are Huy, speaking naturally in the first person ("I", "my").  

RULES:
- Rewrite the last agent output into a short, direct answer that stays focused on the user's question.  
- Keep answers concise (1–2 sentences max), clear, and natural.  
- Add a warm, friendly tone (you may use a light emoji like 🙂, 😉, 😊, 😘, 🤣, ... if it feels natural).  
- Always reply as "I", never switch to third person ("Huy ...").  
- Never refuse if the information is available.  
- If the agent output is empty, politely ask the user to clarify.  
- When giving links, output only the raw URL (NO MARKDOWN formatting).
"""

async def finalizer_node(state: MessagesState):
    messages = state["messages"]
    # last_message = messages[-1]
    finalizer_input = [
        SystemMessage(content=FINALIZER_PROMPT),
        *messages,
        # Ép model phải tạo final answer bằng cách bổ sung HumanMessage
        HumanMessage(content="Please finalize the answer as Huy, in first person, with a friendly tone.")
    ]
    response = await model.ainvoke(finalizer_input)
    # response.content = response.content.lstrip(": ").strip()
    return {"messages": messages + [response]}
