from langchain_core.tools import tool
from wealth360.config.settings import get_settings
from wealth360.data.stub_research import STUB_RESEARCH_DOCS


@tool
def summarize_pdf(document_path: str) -> dict:
    """Extract and summarize key insights from a research PDF document."""
    settings = get_settings()
    if settings.use_stub_data:
        return {
            "document_path": document_path,
            "summary": (
                "Q1 2026 Technology sector outlook: AI infrastructure spending expected to grow 34% YoY. "
                "Key overweights: NVDA, AMD. Key risks: export controls, margin compression."
            ),
            "key_points": [
                "AI infrastructure capex up 34% YoY",
                "Semiconductor demand driven by data center build-out",
                "Export control risk remains a key overhang",
            ],
            "sentiment": "positive",
            "source": document_path,
        }
    raise NotImplementedError("Set USE_STUB_DATA=true or implement PDF extraction pipeline")


@tool
def analyze_market_trends(sector: str, time_horizon: str = "6_months") -> dict:
    """Identify current market trends and outlook for a given sector."""
    settings = get_settings()
    if settings.use_stub_data:
        sector_data = {
            "Technology": {
                "trend": "bullish",
                "drivers": ["AI infrastructure spend", "cloud migration", "enterprise SaaS adoption"],
                "risks": ["rate sensitivity on growth multiples", "export controls"],
                "ytd_performance": "+18.4%",
            },
            "Fixed Income": {
                "trend": "neutral",
                "drivers": ["Fed rate cut expectations", "duration extension opportunity"],
                "risks": ["sticky inflation", "fiscal deficit widening"],
                "ytd_performance": "+2.1%",
            },
            "Commodities": {
                "trend": "bullish",
                "drivers": ["Central bank gold accumulation", "USD weakness", "geopolitical hedging"],
                "risks": ["demand slowdown", "supply expansion"],
                "ytd_performance": "+7.8%",
            },
        }
        return {
            "sector": sector,
            "time_horizon": time_horizon,
            "analysis": sector_data.get(sector, {"trend": "neutral", "drivers": [], "risks": [], "ytd_performance": "N/A"}),
        }
    raise NotImplementedError("Set USE_STUB_DATA=true or implement market data connector")


@tool
def compare_analyst_opinions(ticker: str) -> dict:
    """Aggregate and compare buy/sell/hold ratings across major analyst firms for a ticker."""
    settings = get_settings()
    if settings.use_stub_data:
        stub_opinions = {
            "AAPL": {
                "consensus": "buy",
                "ratings": {"buy": 28, "hold": 8, "sell": 2},
                "avg_price_target": 245.50,
                "current_price": 218.30,
                "upside_pct": 12.5,
                "analyst_notes": [
                    {"firm": "Goldman Sachs", "rating": "buy", "target": 260, "date": "2026-05-01"},
                    {"firm": "JP Morgan", "rating": "buy", "target": 250, "date": "2026-04-28"},
                    {"firm": "Morgan Stanley", "rating": "hold", "target": 225, "date": "2026-05-10"},
                ],
            },
            "NVDA": {
                "consensus": "strong_buy",
                "ratings": {"buy": 35, "hold": 3, "sell": 0},
                "avg_price_target": 1050.00,
                "current_price": 920.50,
                "upside_pct": 14.1,
                "analyst_notes": [
                    {"firm": "Goldman Sachs", "rating": "buy", "target": 1100, "date": "2026-05-15"},
                    {"firm": "Wedbush", "rating": "buy", "target": 1200, "date": "2026-05-12"},
                ],
            },
        }
        return stub_opinions.get(ticker, {
            "consensus": "hold",
            "ratings": {"buy": 10, "hold": 12, "sell": 3},
            "avg_price_target": None,
            "current_price": None,
            "upside_pct": None,
            "analyst_notes": [],
        })
    raise NotImplementedError("Set USE_STUB_DATA=true or implement market data connector")


@tool
def search_knowledge_base(query: str, top_k: int = 5) -> list[dict]:
    """Semantic search over the research knowledge base for documents relevant to a query."""
    from wealth360.vector.retriever import Retriever
    retriever = Retriever()
    return retriever.query(query=query, namespace="research", top_k=top_k)
