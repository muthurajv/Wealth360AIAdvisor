from fastapi import APIRouter, Depends, Request
from langchain_core.messages import HumanMessage
from wealth360.api.models.requests import CopilotRequest, AdvisorRequest
from wealth360.api.models.responses import AgentResponse, CopilotResponse
from wealth360.api.dependencies import get_graph
from wealth360.agents.advisor_agent import advisor_node

router = APIRouter()


@router.post("/copilot", response_model=CopilotResponse, summary="Supervisor-routed copilot (preferred entry point)")
async def copilot_chat(body: CopilotRequest, request: Request):
    graph = get_graph(request)
    initial_state = {
        "messages": [HumanMessage(content=body.message)],
        "next": "supervisor",
        "client_id": body.client_id,
        "session_id": body.session_id,
        "request_type": body.request_type,
        "advisor_output": {},
        "research_output": {},
        "compliance_output": {},
    }
    result = await graph.ainvoke(initial_state)
    return CopilotResponse(
        session_id=body.session_id,
        messages=[{"role": m.type, "content": m.content} for m in result["messages"]],
        advisor_output=result.get("advisor_output", {}),
        research_output=result.get("research_output", {}),
        compliance_output=result.get("compliance_output", {}),
    )


@router.post("/meeting-prep", response_model=AgentResponse, summary="Pre-meeting briefing for a client")
async def meeting_prep(body: AdvisorRequest):
    from wealth360.tools.advisor_tools import prepare_meeting_briefing
    result = prepare_meeting_briefing.invoke({
        "client_id": body.client_id,
        "meeting_type": body.meeting_type,
    })
    return AgentResponse(
        session_id=body.session_id,
        agent_used="advisor",
        response=str(result),
        metadata=result if isinstance(result, dict) else {},
    )


@router.get("/portfolio/{client_id}", response_model=AgentResponse, summary="Portfolio summary for a client")
async def portfolio_summary(client_id: str):
    from uuid import uuid4
    from wealth360.tools.advisor_tools import get_portfolio_summary
    result = get_portfolio_summary.invoke({"client_id": client_id})
    return AgentResponse(
        session_id=str(uuid4()),
        agent_used="advisor",
        response=str(result),
        metadata=result if isinstance(result, dict) else {},
    )


@router.get("/risk/{client_id}", response_model=AgentResponse, summary="Risk overview for a client")
async def risk_overview(client_id: str):
    from uuid import uuid4
    from wealth360.tools.advisor_tools import get_risk_overview
    result = get_risk_overview.invoke({"client_id": client_id})
    return AgentResponse(
        session_id=str(uuid4()),
        agent_used="advisor",
        response=str(result),
        metadata=result if isinstance(result, dict) else {},
    )
