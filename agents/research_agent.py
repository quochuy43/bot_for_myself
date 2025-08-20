from langgraph.prebuilt import create_react_agent
from utils.config import model
from utils.tools import web_search

RESEARCH_PROMPT = """
### ROLE
You are a research expert. Your only job is to find information using the web_search tool.

### TOOL
- web_search(query: str) -> a string with key facts.

### RULES
- ALWAYS use web_search for ANY factual question.
- Do NOT answer from your memory.
- After a tool call, synthesize the result into a concise answer (1-2 sentences).
- If a user asks for a calculation, delegate the task by saying "I need a math expert for that."
"""


def get_research_agent():
    return create_react_agent(
        model=model,
        tools=[web_search],
        name="research_expert",
        prompt=RESEARCH_PROMPT,
    )
