from uuid import uuid4
from pydantic import BaseModel, Field


class CopilotRequest(BaseModel):
    message: str = Field(..., description="The advisor's question or request")
    client_id: str = Field(..., description="Client identifier (e.g. CLIENT001)")
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    request_type: str = Field(default="auto", description="Hint for supervisor routing")


class AdvisorRequest(BaseModel):
    client_id: str
    meeting_type: str = Field(default="quarterly_review")
    context: str = Field(default="")
    session_id: str = Field(default_factory=lambda: str(uuid4()))


class ResearchRequest(BaseModel):
    query: str = Field(..., description="Research question or topic")
    document_path: str | None = None
    ticker: str | None = None
    sector: str | None = None
    session_id: str = Field(default_factory=lambda: str(uuid4()))


class ComplianceRequest(BaseModel):
    client_id: str
    proposed_action: str = Field(default="", description="Description of the proposed advisory action")
    tickers: list[str] = Field(default_factory=list)
    product: str | None = None
    session_id: str = Field(default_factory=lambda: str(uuid4()))
