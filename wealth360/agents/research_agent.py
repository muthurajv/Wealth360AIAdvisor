from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from wealth360.llm.azure_openai import get_llm
from wealth360.tools.research_tools import (
    summarize_pdf,
    analyze_market_trends,
    compare_analyst_opinions,
    search_knowledge_base,
)
from wealth360.tools.vector_tools import retrieve_documents
from wealth360.agents.state import Wealth360State
from wealth360.observability.decorators import traced_agent

_SYSTEM_PROMPT = SystemMessage(content="""
You are the Research Intelligence Agent for Wealth360 AI Advisor Copilot.

Your responsibilities:
- Analyze and summarize market research documents and PDFs
- Identify sector trends and macro themes relevant to client portfolios
- Compare analyst opinions and consensus ratings for specific tickers
- Search the knowledge base for relevant research on any topic

When answering research queries:
- Cite sources (analyst firm, report date) when available
- Note consensus vs. outlier opinions
- Highlight key risks alongside opportunities
- Keep summaries concise — bullet points preferred
""")

_TOOLS = [
    summarize_pdf,
    analyze_market_trends,
    compare_analyst_opinions,
    search_knowledge_base,
    retrieve_documents,
]


@traced_agent("research")
def research_node(state: Wealth360State) -> dict:
    agent = create_react_agent(
        model=get_llm(),
        tools=_TOOLS,
        prompt=_SYSTEM_PROMPT,
    )
    result = agent.invoke({"messages": state["messages"]})
    last_msg = result["messages"][-1]
    return {
        "messages": result["messages"],
        "research_output": {
            "response": last_msg.content,
            "agent": "research",
        },
    }
