from langchain_core.tools import tool


@tool
def retrieve_documents(query: str, namespace: str = "research", top_k: int = 5) -> list[dict]:
    """Perform semantic retrieval from the knowledge base. Returns the most relevant documents for a query."""
    from wealth360.vector.retriever import Retriever
    return Retriever().query(query=query, namespace=namespace, top_k=top_k)
