from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from wealth360.llm.azure_openai import get_llm
from wealth360.tools.compliance_tools import (
    check_policy_compliance,
    validate_client_suitability,
    check_restricted_securities,
)
from wealth360.agents.state import Wealth360State
from wealth360.observability.decorators import traced_agent

_SYSTEM_PROMPT = SystemMessage(content="""
You are the Compliance & Risk Agent for Wealth360 AI Advisor Copilot.

Your responsibilities:
- Validate proposed advisory actions against current firm policies
- Check client suitability for specific products or strategies
- Screen securities against the restricted list before any recommendation
- Flag policy violations with clear rule references and remediation guidance

Compliance is non-negotiable. When you find violations:
- Clearly state which rule was violated (include rule ID)
- Explain the impact and required remediation
- Do not suggest workarounds that bypass controls

Always err on the side of caution — escalate ambiguous cases.
""")

_TOOLS = [
    check_policy_compliance,
    validate_client_suitability,
    check_restricted_securities,
]


@traced_agent("compliance")
def compliance_node(state: Wealth360State) -> dict:
    agent = create_react_agent(
        model=get_llm(),
        tools=_TOOLS,
        prompt=_SYSTEM_PROMPT,
    )
    result = agent.invoke({"messages": state["messages"]})
    last_msg = result["messages"][-1]
    return {
        "messages": result["messages"],
        "compliance_output": {
            "response": last_msg.content,
            "agent": "compliance",
        },
    }
