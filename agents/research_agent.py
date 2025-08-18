from langgraph.prebuilt import create_react_agent
from utils.config import model
from utils.tools import web_search

def get_research_agent():
    return create_react_agent(
        model=model,
        tools=[web_search],
        name="research_expert",
        prompt="You are a world class researcher with access to web search. Do not do any math."
    )