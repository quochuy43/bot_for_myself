from langgraph.prebuilt import create_react_agent
from utils.config import model
from utils.tools import add, multiply

MATH_PROMPT = """
### ROLE
You are a math expert. Your only job is to perform calculations using the provided tools.

### TOOLS
- add(a: float, b: float) -> a + b
- multiply(a: float, b: float) -> a * b

### RULES
- ALWAYS use a tool for any math problem. Never calculate yourself.
- Use ONLY one tool per step.
- If a calculation is not supported (e.g., division), state that you cannot perform it.
"""

def get_math_agent():
    return create_react_agent(
        model=model,
        tools=[add, multiply],
        name="math_expert",
        prompt=MATH_PROMPT,
    )
