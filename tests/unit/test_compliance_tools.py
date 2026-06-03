import pytest
from wealth360.tools.compliance_tools import (
    check_restricted_securities,
    validate_client_suitability,
    check_policy_compliance,
)


def test_restricted_screen_flags_restricted():
    result = check_restricted_securities.invoke({"tickers": ["AAPL", "TICKER_X", "MSFT"]})
    assert result["flagged"] == ["TICKER_X"]
    assert set(result["passed"]) == {"AAPL", "MSFT"}
    assert result["compliant"] is False


def test_restricted_screen_all_clear():
    result = check_restricted_securities.invoke({"tickers": ["AAPL", "MSFT", "BND"]})
    assert result["flagged"] == []
    assert result["compliant"] is True


def test_restricted_screen_all_flagged():
    result = check_restricted_securities.invoke({"tickers": ["TICKER_X", "TICKER_Y"]})
    assert len(result["flagged"]) == 2
    assert result["compliant"] is False


def test_suitability_approved_product():
    result = validate_client_suitability.invoke({"client_id": "CLIENT001", "product": "AAPL"})
    assert result["suitable"] is True
    assert result["risk_profile"] == "moderate"


def test_suitability_unapproved_product():
    result = validate_client_suitability.invoke({"client_id": "CLIENT001", "product": "TQQQ"})
    assert result["suitable"] is False


def test_suitability_unknown_client():
    result = validate_client_suitability.invoke({"client_id": "GHOST", "product": "SPY"})
    assert result["suitable"] is False
    assert "not found" in result["reason"]


def test_policy_compliance_concentration_violation():
    # CLIENT001 has BND at 40% and SPY at 35% — both exceed 20% limit
    result = check_policy_compliance.invoke({
        "client_id": "CLIENT001",
        "proposed_action": "add more equity",
    })
    assert result["compliant"] is False
    violation_rule_ids = [v["rule_id"] for v in result["violations"]]
    assert "POL-001" in violation_rule_ids


def test_policy_compliance_unknown_client():
    result = check_policy_compliance.invoke({"client_id": "GHOST", "proposed_action": "buy AAPL"})
    assert result["compliant"] is False
