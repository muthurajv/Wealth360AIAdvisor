from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from wealth360.llm.azure_openai import get_llm
from wealth360.tools.advisor_tools import (
    get_portfolio_summary,
    prepare_meeting_briefing,
    generate_action_recommendations,
    get_risk_overview,
)
from wealth360.agents.state import Wealth360State
from wealth360.observability.decorators import traced_agent

_SYSTEM_PROMPT = SystemMessage(content="""
You are the Advisor Intelligence Agent for Wealth360 AI Advisor Copilot.

Your responsibilities:
- Prepare comprehensive pre-meeting briefings for financial advisors
- Summarize client portfolio performance, allocations, and attribution
- Generate next-best-action recommendations based on portfolio state
- Provide risk overview summaries (VaR, beta, Sharpe, drawdown)

Always respond with structured, actionable information tailored to the advisor's needs.
Use the client_id provided in the conversation to look up client data.
Be concise and highlight the most important insights first.
""")

_TOOLS = [
    get_portfolio_summary,
    prepare_meeting_briefing,
    generate_action_recommendations,
    get_risk_overview,
]


@traced_agent("advisor")
def advisor_node(state: Wealth360State) -> dict:
    agent = create_react_agent(
        model=get_llm(),
        tools=_TOOLS,
        prompt=_SYSTEM_PROMPT,
    )
    result = agent.invoke({"messages": state["messages"]})
    last_msg = result["messages"][-1]
    return {
        "messages": result["messages"],
        "advisor_output": {
            "response": last_msg.content,
            "agent": "advisor",
        },
    }
