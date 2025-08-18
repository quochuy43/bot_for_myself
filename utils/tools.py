from langchain_core.tools import tool

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