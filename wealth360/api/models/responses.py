from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    session_id: str
    agent_used: str
    response: str
    metadata: dict = Field(default_factory=dict)


class CopilotResponse(BaseModel):
    session_id: str
    messages: list[dict]
    advisor_output: dict = Field(default_factory=dict)
    research_output: dict = Field(default_factory=dict)
    compliance_output: dict = Field(default_factory=dict)
