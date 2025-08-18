from langgraph.prebuilt import create_react_agent
from utils.config import model
from utils.tools import add, multiply

def get_math_agent():
    return create_react_agent(
        model=model,
        tools=[add, multiply],
        name="math_expert",
        prompt="You are a math expert. Always use one tool at a time."
    )