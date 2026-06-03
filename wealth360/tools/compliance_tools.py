from langchain_core.tools import tool
from wealth360.data.stub_compliance import RESTRICTED_SECURITIES, POLICY_RULES, SUITABILITY_MATRIX
from wealth360.data.stub_portfolios import STUB_PORTFOLIOS


@tool
def check_policy_compliance(client_id: str, proposed_action: str) -> dict:
    """Validate a proposed advisory action against current firm policies for a client."""
    portfolio = STUB_PORTFOLIOS.get(client_id)
    if not portfolio:
        return {"compliant": False, "violations": [f"Client {client_id} not found"], "warnings": []}

    violations = []
    warnings = []
    risk_profile = portfolio["risk_profile"]

    for rule in POLICY_RULES:
        applies = "all" in rule["applies_to"] or risk_profile in rule["applies_to"]
        if not applies:
            continue

        if rule["rule_id"] == "POL-001":
            for holding in portfolio["holdings"]:
                if holding["weight"] > rule["threshold"]:
                    violations.append({
                        "rule_id": rule["rule_id"],
                        "description": rule["description"],
                        "detail": f"{holding['ticker']} is at {holding['weight']:.0%} — exceeds {rule['threshold']:.0%} limit",
                    })

        elif rule["rule_id"] in ("POL-002", "POL-003"):
            fi_weight = sum(h["weight"] for h in portfolio["holdings"] if h["sector"] == "Fixed Income")
            if fi_weight < rule["threshold"]:
                violations.append({
                    "rule_id": rule["rule_id"],
                    "description": rule["description"],
                    "detail": f"Fixed income at {fi_weight:.0%} — below {rule['threshold']:.0%} minimum for {risk_profile} profile",
                })

    return {
        "client_id": client_id,
        "proposed_action": proposed_action,
        "compliant": len(violations) == 0,
        "violations": violations,
        "warnings": warnings,
    }


@tool
def validate_client_suitability(client_id: str, product: str) -> dict:
    """Check if a product or security is suitable for a client's risk profile and investment objective."""
    portfolio = STUB_PORTFOLIOS.get(client_id)
    if not portfolio:
        return {"suitable": False, "reason": f"Client {client_id} not found"}

    risk_profile = portfolio["risk_profile"]
    allowed = SUITABILITY_MATRIX.get(risk_profile, [])
    suitable = product.upper() in [p.upper() for p in allowed]

    return {
        "client_id": client_id,
        "client_name": portfolio["name"],
        "product": product,
        "risk_profile": risk_profile,
        "investment_objective": portfolio["investment_objective"],
        "suitable": suitable,
        "reason": (
            f"{product} is approved for {risk_profile} risk profile"
            if suitable
            else f"{product} is NOT on the approved product list for {risk_profile} risk profile"
        ),
        "approved_products": allowed,
    }


@tool
def check_restricted_securities(tickers: list[str]) -> dict:
    """Screen a list of tickers against the firm's current restricted securities list."""
    tickers_upper = [t.upper() for t in tickers]
    flagged = [t for t in tickers_upper if t in RESTRICTED_SECURITIES]
    passed = [t for t in tickers_upper if t not in RESTRICTED_SECURITIES]
    return {
        "screened": tickers_upper,
        "flagged": flagged,
        "passed": passed,
        "compliant": len(flagged) == 0,
        "note": (
            f"{len(flagged)} restricted security/securities found — trading blocked"
            if flagged
            else "All securities cleared — no restrictions found"
        ),
    }
