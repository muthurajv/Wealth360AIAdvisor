from typing import Literal
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage
from wealth360.agents.state import Wealth360State, AgentName
from wealth360.agents.advisor_agent import advisor_node
from wealth360.agents.research_agent import research_node
from wealth360.agents.compliance_agent import compliance_node
from wealth360.llm.azure_openai import get_llm

_SUPERVISOR_PROMPT = """You are the Wealth360 AI Advisor Copilot supervisor.

Your job is to route user requests to the correct specialist agent.

Available agents:
- advisor: Meeting prep, portfolio summaries, action recommendations, risk overviews
- research: Market research analysis, PDF summaries, analyst opinions, sector trends, knowledge base search
- compliance: Policy compliance checks, product suitability validation, restricted securities screening
- FINISH: Use when all necessary agents have responded and the conversation is complete

Rules:
1. Analyze the conversation history to determine what has already been done
2. Route to the most appropriate next agent, or FINISH if the request is fully addressed
3. You may route to multiple agents sequentially (e.g., research then compliance)
4. Default to FINISH if the last message already contains a complete answer
"""


class RoutingDecision(BaseModel):
    next: Literal["advisor", "research", "compliance", "FINISH"]
    reasoning: str


def _make_supervisor_node():
    router_llm = get_llm().with_structured_output(RoutingDecision)
    system_msg = SystemMessage(content=_SUPERVISOR_PROMPT)

    def supervisor(state: Wealth360State) -> dict:
        messages = [system_msg] + list(state["messages"])
        decision: RoutingDecision = router_llm.invoke(messages)
        return {"next": decision.next}

    return supervisor


def build_graph() -> "CompiledGraph":
    graph = StateGraph(Wealth360State)

    graph.add_node("supervisor", _make_supervisor_node())
    graph.add_node("advisor", advisor_node)
    graph.add_node("research", research_node)
    graph.add_node("compliance", compliance_node)

    graph.add_edge(START, "supervisor")

    graph.add_conditional_edges(
        "supervisor",
        lambda state: state["next"],
        {
            "advisor": "advisor",
            "research": "research",
            "compliance": "compliance",
            "FINISH": END,
        },
    )

    graph.add_edge("advisor", "supervisor")
    graph.add_edge("research", "supervisor")
    graph.add_edge("compliance", "supervisor")

    return graph.compile()
