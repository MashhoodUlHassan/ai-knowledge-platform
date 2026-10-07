from typing import TypedDict


class AgentState(TypedDict):
    query: str
    retrieved_context: list[dict]
    answer: str