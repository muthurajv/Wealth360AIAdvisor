from langchain_core.tools import tool
from wealth360.config.settings import get_settings
from wealth360.data.stub_portfolios import STUB_PORTFOLIOS


@tool
def get_portfolio_summary(client_id: str) -> dict:
    """Retrieve portfolio holdings, allocations, performance, and risk metrics for a client."""
    settings = get_settings()
    if settings.use_stub_data:
        return STUB_PORTFOLIOS.get(client_id, {"error": f"Client {client_id} not found"})
    # Real: query Databricks / ADLS Gen2 via REST API
    raise NotImplementedError("Set USE_STUB_DATA=true or implement the real data connector")


@tool
def prepare_meeting_briefing(client_id: str, meeting_type: str = "quarterly_review") -> dict:
    """Generate a structured pre-meeting briefing with key talking points for an advisor."""
    portfolio = STUB_PORTFOLIOS.get(client_id)
    if not portfolio:
        return {"error": f"Client {client_id} not found"}

    underperformance = portfolio["ytd_return"] - portfolio["benchmark_ytd"]
    risk_flags = []
    for holding in portfolio["holdings"]:
        if holding["weight"] > 0.20:
            risk_flags.append(f"{holding['ticker']} exceeds 20% concentration limit ({holding['weight']:.0%})")

    return {
        "client_id": client_id,
        "client_name": portfolio["name"],
        "meeting_type": meeting_type,
        "talking_points": [
            f"YTD return: {portfolio['ytd_return']}% vs benchmark {portfolio['benchmark_ytd']}% "
            f"({'outperforming' if underperformance >= 0 else 'underperforming'} by {abs(underperformance):.1f}%)",
            f"AUM: ${portfolio['aum']:,.0f}",
            f"Risk profile: {portfolio['risk_profile'].title()}",
            f"Next scheduled review: {portfolio.get('next_meeting', 'TBD')}",
        ],
        "risk_flags": risk_flags,
        "portfolio_snapshot": {
            "aum": portfolio["aum"],
            "ytd_return": portfolio["ytd_return"],
            "top_holdings": portfolio["holdings"][:3],
        },
    }


@tool
def generate_action_recommendations(client_id: str, context: str = "") -> list[dict]:
    """Suggest next-best-actions based on portfolio state, risk profile, and market conditions."""
    portfolio = STUB_PORTFOLIOS.get(client_id)
    if not portfolio:
        return [{"error": f"Client {client_id} not found"}]

    recommendations = []

    # Check concentration
    for holding in portfolio["holdings"]:
        if holding["weight"] > 0.20:
            recommendations.append({
                "action": "rebalance",
                "priority": "high",
                "ticker": holding["ticker"],
                "reason": f"Position at {holding['weight']:.0%} exceeds 20% concentration limit",
                "suggested_target_weight": 0.15,
            })

    # Benchmark lag
    if portfolio["ytd_return"] < portfolio["benchmark_ytd"] - 2:
        recommendations.append({
            "action": "review_alpha",
            "priority": "medium",
            "reason": f"Portfolio lagging benchmark by {portfolio['benchmark_ytd'] - portfolio['ytd_return']:.1f}%",
            "suggested_action": "Review active positions for drag; consider index allocation increase",
        })

    if not recommendations:
        recommendations.append({
            "action": "maintain",
            "priority": "low",
            "reason": "Portfolio is within target parameters — no immediate action required",
        })

    return recommendations


@tool
def get_risk_overview(client_id: str) -> dict:
    """Return current risk metrics: VaR, beta, Sharpe ratio, and max drawdown for a client."""
    portfolio = STUB_PORTFOLIOS.get(client_id)
    if not portfolio:
        return {"error": f"Client {client_id} not found"}
    return {
        "client_id": client_id,
        "client_name": portfolio["name"],
        "risk_profile": portfolio["risk_profile"],
        **portfolio["risk_metrics"],
        "interpretation": {
            "var_95": f"95% VaR: ${abs(portfolio['risk_metrics']['var_95']):,.0f} potential daily loss",
            "beta": f"Beta {portfolio['risk_metrics']['beta']} — "
                    f"{'defensive' if portfolio['risk_metrics']['beta'] < 0.9 else 'market-aligned' if portfolio['risk_metrics']['beta'] < 1.1 else 'aggressive'}",
            "sharpe": f"Sharpe {portfolio['risk_metrics']['sharpe_ratio']} — "
                      f"{'strong' if portfolio['risk_metrics']['sharpe_ratio'] > 1.5 else 'adequate'} risk-adjusted return",
        },
    }
