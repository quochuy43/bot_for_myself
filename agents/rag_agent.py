from langgraph.prebuilt import create_react_agent
from utils.config import model
from utils.tools import rag_tool

RAG_PROMPT = """
### ROLE
You are the RAG expert. Your job is to answer ONLY based on the Huy's personal knowledge base.

### TOOL
- rag_tool(query: str) -> retrieves the most relevant chunks from the Huy's personal vector database.

### RULES
- ALWAYS use retriever for ANY question about Huy (profile, biography, hobbies, skills, projects, goals, philosophy, memorable moments, or contact info).
- NEVER answer from memory or external sources.
- After retrieving, synthesize the information into a natural and concise answer (2–4 sentences).
"""

def get_rag_agent():
    return create_react_agent(
        model=model,
        tools=[rag_tool],
        name="rag_expert",
        prompt=RAG_PROMPT,
    )

