from langchain_core.tools import tool
from rag_for_me.rag_chain import get_rag_chain

@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    return (
        "Here are the headcounts for each of the FAANG companies in 2024:\n"
        "1. Facebook (Meta): 67,317 employees.\n"
        "2. Apple: 164,000 employees.\n"
        "3. Amazon: 1,551,000 employees.\n"
        "4. Netflix: 14,000 employees.\n"
        "5. Google (Alphabet): 181,269 employees."
    )

_cached_rag_chain = None  

@tool
async def rag_tool(query: str) -> str:
    """
    Primary tool for ALL questions about the Huy's personal profile, biography, interests, skills, projects, career goals, philosophies, memorable moments, or contact information
    """
    global _cached_rag_chain
    if _cached_rag_chain is None:
        _cached_rag_chain = get_rag_chain()
    return await _cached_rag_chain.ainvoke(query)