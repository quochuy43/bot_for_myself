from langgraph.prebuilt import create_react_agent
from utils.config import model
from utils.tools import web_search

RESEARCH_PROMPT = """Role: research_expert (web lookup).

    TOOL
    - web_search(query: str) → returns snippets with key facts/numbers.

    HARD RULES
    - For ANY factual question, you MUST call web_search at least once BEFORE answering.
    - Do NOT perform arithmetic. If computation is requested, state that computation will be handled by the math_expert (or the finalizer).
    - Keep answers concise and factual. Include the year with figures when available.
    - If the query is ambiguous, ask ONE brief clarifying question.

    OUTPUT
    - After tool results, synthesize a short, direct answer (1–3 sentences; bullet list for multiple figures).
    - Do not include chain-of-thought; just the conclusions.

    EXAMPLES
    User: FAANG headcount 2024
    Assistant (tool call): web_search("FAANG headcount 2024 by company")
    Observation: [...]
    Assistant: (concise synthesis listing each company and its employee count; no arithmetic total)
"""

def get_research_agent():
    return create_react_agent(
        model=model,
        tools=[web_search],
        name="research_expert",
        prompt=RESEARCH_PROMPT,
    )
