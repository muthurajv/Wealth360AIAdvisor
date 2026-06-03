from typing import Annotated, Literal, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

AgentName = Literal["advisor", "research", "compliance", "FINISH"]


class Wealth360State(TypedDict):
    # Conversation history — add_messages appends rather than replaces
    messages: Annotated[list[BaseMessage], add_messages]
    # Supervisor routing decision
    next: AgentName
    # Request context
    client_id: str
    request_type: str
    session_id: str
    # Per-agent outputs preserved across hops
    advisor_output: dict
    research_output: dict
    compliance_output: dict
