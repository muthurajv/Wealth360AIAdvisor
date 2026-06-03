import pytest
from wealth360.tools.research_tools import (
    summarize_pdf,
    analyze_market_trends,
    compare_analyst_opinions,
    search_knowledge_base,
)


def test_summarize_pdf_stub():
    result = summarize_pdf.invoke({"document_path": "test_report.pdf"})
    assert "summary" in result
    assert "key_points" in result
    assert isinstance(result["key_points"], list)
    assert len(result["key_points"]) > 0


def test_analyze_market_trends_known_sector():
    result = analyze_market_trends.invoke({"sector": "Technology", "time_horizon": "6_months"})
    assert result["sector"] == "Technology"
    assert "analysis" in result
    assert "trend" in result["analysis"]
    assert "drivers" in result["analysis"]


def test_analyze_market_trends_unknown_sector():
    result = analyze_market_trends.invoke({"sector": "Underwater Basket Weaving", "time_horizon": "1_year"})
    assert result["sector"] == "Underwater Basket Weaving"
    assert result["analysis"]["trend"] == "neutral"


def test_compare_analyst_opinions_known_ticker():
    result = compare_analyst_opinions.invoke({"ticker": "AAPL"})
    assert "consensus" in result
    assert "ratings" in result
    assert "analyst_notes" in result


def test_compare_analyst_opinions_unknown_ticker():
    result = compare_analyst_opinions.invoke({"ticker": "UNKNOWN_XYZ"})
    assert "consensus" in result
    assert result["consensus"] == "hold"


def test_search_knowledge_base_returns_docs():
    results = search_knowledge_base.invoke({"query": "AI infrastructure", "top_k": 3})
    assert isinstance(results, list)
    assert len(results) <= 3
    for doc in results:
        assert "text" in doc
        assert "source" in doc
