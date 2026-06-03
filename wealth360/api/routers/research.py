from uuid import uuid4
from fastapi import APIRouter
from wealth360.api.models.requests import ResearchRequest
from wealth360.api.models.responses import AgentResponse

router = APIRouter()


@router.post("/analyze", response_model=AgentResponse, summary="Analyze a research query or topic")
async def analyze_research(body: ResearchRequest):
    from wealth360.tools.research_tools import search_knowledge_base
    results = search_knowledge_base.invoke({"query": body.query})
    summary = "\n\n".join(
        f"[{d['source']}] {d['text']}" for d in results
    )
    return AgentResponse(
        session_id=body.session_id,
        agent_used="research",
        response=summary,
        metadata={"documents_found": len(results)},
    )


@router.post("/summarize-pdf", response_model=AgentResponse, summary="Summarize a research PDF")
async def summarize_pdf(body: ResearchRequest):
    from wealth360.tools.research_tools import summarize_pdf as _summarize
    path = body.document_path or "stub_document.pdf"
    result = _summarize.invoke({"document_path": path})
    return AgentResponse(
        session_id=body.session_id,
        agent_used="research",
        response=result.get("summary", ""),
        metadata=result,
    )


@router.get("/analyst/{ticker}", response_model=AgentResponse, summary="Analyst opinion comparison for a ticker")
async def compare_analysts(ticker: str):
    from wealth360.tools.research_tools import compare_analyst_opinions
    result = compare_analyst_opinions.invoke({"ticker": ticker})
    return AgentResponse(
        session_id=str(uuid4()),
        agent_used="research",
        response=str(result),
        metadata=result if isinstance(result, dict) else {},
    )


@router.get("/trends/{sector}", response_model=AgentResponse, summary="Market trend analysis for a sector")
async def market_trends(sector: str, time_horizon: str = "6_months"):
    from wealth360.tools.research_tools import analyze_market_trends
    result = analyze_market_trends.invoke({"sector": sector, "time_horizon": time_horizon})
    return AgentResponse(
        session_id=str(uuid4()),
        agent_used="research",
        response=str(result),
        metadata=result if isinstance(result, dict) else {},
    )
