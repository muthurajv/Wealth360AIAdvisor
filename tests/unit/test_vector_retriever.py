import pytest
from wealth360.vector.retriever import Retriever


def test_retriever_returns_stub_docs():
    r = Retriever()
    docs = r.query("technology sector")
    assert isinstance(docs, list)
    assert len(docs) > 0


def test_retriever_respects_top_k():
    r = Retriever()
    docs = r.query("any query", top_k=2)
    assert len(docs) <= 2


def test_retriever_doc_structure():
    r = Retriever()
    docs = r.query("market outlook")
    for doc in docs:
        assert "text" in doc
        assert "source" in doc
        assert "id" in doc
