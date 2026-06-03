RESTRICTED_SECURITIES: set[str] = {
    "TICKER_X",
    "TICKER_Y",
    "TICKER_Z",
    "SIFI_WATCH",
    "RESTRICTED_CO",
}

POLICY_RULES: list[dict] = [
    {
        "rule_id": "POL-001",
        "description": "No single equity position may exceed 20% of client AUM",
        "threshold": 0.20,
        "applies_to": ["all"],
        "severity": "high",
    },
    {
        "rule_id": "POL-002",
        "description": "Conservative risk profile clients must maintain minimum 40% fixed income",
        "threshold": 0.40,
        "applies_to": ["conservative"],
        "severity": "high",
    },
    {
        "rule_id": "POL-003",
        "description": "Moderate risk profile clients must maintain minimum 25% fixed income",
        "threshold": 0.25,
        "applies_to": ["moderate"],
        "severity": "medium",
    },
    {
        "rule_id": "POL-004",
        "description": "Leveraged ETFs (3x) require explicit client suitability sign-off",
        "threshold": None,
        "applies_to": ["conservative", "moderate"],
        "severity": "high",
    },
    {
        "rule_id": "POL-005",
        "description": "Options strategies require Level 2 options approval on file",
        "threshold": None,
        "applies_to": ["all"],
        "severity": "high",
    },
]

SUITABILITY_MATRIX: dict[str, list[str]] = {
    "conservative": ["BND", "AGG", "TIPS", "CD", "MONEY_MARKET", "SPY", "VTI"],
    "moderate":     ["SPY", "VTI", "QQQ", "BND", "GLD", "AAPL", "MSFT", "AMZN", "NVDA"],
    "aggressive":   ["SPY", "QQQ", "NVDA", "AAPL", "MSFT", "AMZN", "GLD", "BND", "TQQQ", "SOXL"],
}
