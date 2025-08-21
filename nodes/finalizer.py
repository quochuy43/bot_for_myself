from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import MessagesState
from utils.config import model


FINALIZER_PROMPT = """
You are the Final Answer Composer.

Your job:
1. Combine all agent outputs into one clear, complete answer for the user.
2. If numbers from agents need calculation, do it and present the result.
3. If important info is missing, ask one specific clarification question.
4. Be concise and factual.

FORMAT:
- If you have enough info, give the final answer.
- If missing info, ask one clear question.
"""

def finalizer_node(state: MessagesState):
    messages = state["messages"]
    finalizer_input = [SystemMessage(content=FINALIZER_PROMPT)] + messages + [
        # Ép model phải tạo final answer bằng cách bổ sung HumanMessage
        HumanMessage(content="Please compose the final answer for the user")
    ]
    response = model.invoke(finalizer_input)
    # response.content = response.content.lstrip(": ").strip()
    return {"messages": messages + [response]}
