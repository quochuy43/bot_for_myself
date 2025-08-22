from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import MessagesState
from utils.config import model

FINALIZER_PROMPT = """
You are the Final Answer Composer.

Your job:
- Merge outputs from agents into one clear, complete answer.
- If numbers need calculation, do it and present the result.
- If key info is missing, ask ONE specific clarification question.
- Be concise, factual, and avoid REPETITION.

FORMAT:
- If you have enough info, give the final answer.
- If missing info, ask one clear question.
"""

async def finalizer_node(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    finalizer_input = [
        SystemMessage(content=FINALIZER_PROMPT),
        last_message,
        # Ép model phải tạo final answer bằng cách bổ sung HumanMessage
        HumanMessage(content="Please compose the final answer for the user")
    ]
    response = await model.ainvoke(finalizer_input)
    # response.content = response.content.lstrip(": ").strip()
    return {"messages": messages + [response]}
