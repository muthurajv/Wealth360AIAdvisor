from uuid import uuid4
from fastapi import APIRouter
from wealth360.api.models.requests import ComplianceRequest
from wealth360.api.models.responses import AgentResponse

router = APIRouter()


@router.post("/validate", response_model=AgentResponse, summary="Validate a proposed action against firm policies")
async def validate_compliance(body: ComplianceRequest):
    from wealth360.tools.compliance_tools import check_policy_compliance
    result = check_policy_compliance.invoke({
        "client_id": body.client_id,
        "proposed_action": body.proposed_action,
    })
    return AgentResponse(
        session_id=body.session_id,
        agent_used="compliance",
        response="COMPLIANT" if result["compliant"] else f"VIOLATIONS FOUND: {result['violations']}",
        metadata=result,
    )


@router.post("/suitability", response_model=AgentResponse, summary="Check product suitability for a client")
async def suitability_check(body: ComplianceRequest):
    from wealth360.tools.compliance_tools import validate_client_suitability
    product = body.product or ""
    result = validate_client_suitability.invoke({
        "client_id": body.client_id,
        "product": product,
    })
    return AgentResponse(
        session_id=body.session_id,
        agent_used="compliance",
        response=result["reason"],
        metadata=result,
    )


@router.post("/restricted-screen", response_model=AgentResponse, summary="Screen tickers against restricted list")
async def restricted_screen(body: ComplianceRequest):
    from wealth360.tools.compliance_tools import check_restricted_securities
    result = check_restricted_securities.invoke({"tickers": body.tickers})
    return AgentResponse(
        session_id=body.session_id,
        agent_used="compliance",
        response=result["note"],
        metadata=result,
    )
