import pytest
from wealth360.tools.advisor_tools import (
    get_portfolio_summary,
    prepare_meeting_briefing,
    generate_action_recommendations,
    get_risk_overview,
)


def test_portfolio_summary_known_client():
    result = get_portfolio_summary.invoke({"client_id": "CLIENT001"})
    assert result["client_id"] == "CLIENT001"
    assert result["name"] == "Jane Smith"
    assert isinstance(result["aum"], (int, float))
    assert len(result["holdings"]) > 0


def test_portfolio_summary_unknown_client():
    result = get_portfolio_summary.invoke({"client_id": "UNKNOWN"})
    assert "error" in result


def test_meeting_briefing_returns_structure():
    result = prepare_meeting_briefing.invoke({"client_id": "CLIENT001", "meeting_type": "quarterly_review"})
    assert "talking_points" in result
    assert "portfolio_snapshot" in result
    assert "risk_flags" in result
    assert isinstance(result["talking_points"], list)
    assert len(result["talking_points"]) > 0


def test_meeting_briefing_unknown_client():
    result = prepare_meeting_briefing.invoke({"client_id": "GHOST", "meeting_type": "annual"})
    assert "error" in result


def test_action_recommendations_returns_list():
    result = generate_action_recommendations.invoke({"client_id": "CLIENT001", "context": ""})
    assert isinstance(result, list)
    assert len(result) > 0
    for rec in result:
        assert "action" in rec
        assert "priority" in rec


def test_risk_overview_known_client():
    result = get_risk_overview.invoke({"client_id": "CLIENT001"})
    assert result["client_id"] == "CLIENT001"
    assert "var_95" in result
    assert "beta" in result
    assert "sharpe_ratio" in result
    assert "interpretation" in result


def test_risk_overview_unknown_client():
    result = get_risk_overview.invoke({"client_id": "MISSING"})
    assert "error" in result
