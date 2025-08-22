from langchain_core.tools import tool
from rag_for_me.rag_chain import get_rag_chain

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