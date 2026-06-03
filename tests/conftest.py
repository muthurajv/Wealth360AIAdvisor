import pytest
from unittest.mock import MagicMock
from langchain_core.messages import AIMessage, HumanMessage
from fastapi.testclient import TestClient
from wealth360.api.app import create_app


@pytest.fixture(scope="session")
def test_client():
    app = create_app()
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.invoke.return_value = AIMessage(content="stub response")
    structured = MagicMock()
    structured.invoke.return_value = MagicMock(next="FINISH", reasoning="test done")
    llm.with_structured_output.return_value = structured
    return llm


@pytest.fixture
def sample_state():
    return {
        "messages": [HumanMessage(content="Prepare a briefing for CLIENT001")],
        "next": "supervisor",
        "client_id": "CLIENT001",
        "session_id": "test-session-001",
        "request_type": "meeting_prep",
        "advisor_output": {},
        "research_output": {},
        "compliance_output": {},
    }
