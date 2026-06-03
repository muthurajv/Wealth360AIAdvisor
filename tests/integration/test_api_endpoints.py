import pytest
from fastapi.testclient import TestClient
from wealth360.api.app import create_app


@pytest.fixture(scope="module")
def client():
    app = create_app()
    with TestClient(app) as c:
        yield c


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_portfolio_endpoint(client):
    resp = client.get("/api/v1/advisor/portfolio/CLIENT001")
    assert resp.status_code == 200
    body = resp.json()
    assert body["agent_used"] == "advisor"
    assert "CLIENT001" in body["response"]


def test_portfolio_unknown_client(client):
    resp = client.get("/api/v1/advisor/portfolio/UNKNOWN_XYZ")
    assert resp.status_code == 200
    body = resp.json()
    assert "error" in body["response"].lower() or "not found" in body["response"].lower()


def test_risk_endpoint(client):
    resp = client.get("/api/v1/advisor/risk/CLIENT001")
    assert resp.status_code == 200
    body = resp.json()
    assert body["agent_used"] == "advisor"


def test_meeting_prep_endpoint(client):
    resp = client.post("/api/v1/advisor/meeting-prep", json={
        "client_id": "CLIENT001",
        "meeting_type": "quarterly_review",
    })
    assert resp.status_code == 200
    body = resp.json()
    assert body["agent_used"] == "advisor"


def test_research_analyze_endpoint(client):
    resp = client.post("/api/v1/research/analyze", json={"query": "AI sector outlook"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["agent_used"] == "research"
    assert len(body["response"]) > 0


def test_research_analyst_endpoint(client):
    resp = client.get("/api/v1/research/analyst/AAPL")
    assert resp.status_code == 200
    body = resp.json()
    assert body["agent_used"] == "research"


def test_research_trends_endpoint(client):
    resp = client.get("/api/v1/research/trends/Technology")
    assert resp.status_code == 200
    body = resp.json()
    assert body["agent_used"] == "research"


def test_compliance_restricted_screen(client):
    resp = client.post("/api/v1/compliance/restricted-screen", json={
        "client_id": "CLIENT001",
        "tickers": ["AAPL", "TICKER_X"],
    })
    assert resp.status_code == 200
    body = resp.json()
    assert "TICKER_X" in body["response"] or "restricted" in body["response"].lower()


def test_compliance_suitability(client):
    resp = client.post("/api/v1/compliance/suitability", json={
        "client_id": "CLIENT001",
        "product": "AAPL",
    })
    assert resp.status_code == 200
    body = resp.json()
    assert body["agent_used"] == "compliance"


def test_compliance_validate(client):
    resp = client.post("/api/v1/compliance/validate", json={
        "client_id": "CLIENT001",
        "proposed_action": "Add more technology equity",
    })
    assert resp.status_code == 200
    body = resp.json()
    assert body["agent_used"] == "compliance"
