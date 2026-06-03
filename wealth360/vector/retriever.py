from wealth360.config.settings import get_settings
from wealth360.vector.client import get_pinecone_index


class Retriever:
    def __init__(self):
        self.settings = get_settings()
        self.index = get_pinecone_index()

    def query(self, query: str, namespace: str = "research", top_k: int = 5) -> list[dict]:
        if self.settings.use_stub_data or self.index is None:
            return self._stub_results(top_k)
        from wealth360.vector.embedder import get_embedder
        embedding = get_embedder().embed_query(query)
        results = self.index.query(
            vector=embedding,
            top_k=top_k,
            namespace=namespace,
            include_metadata=True,
        )
        return [
            {
                "id": m.id,
                "score": m.score,
                "text": m.metadata.get("text", ""),
                "source": m.metadata.get("source", ""),
                "doc_type": m.metadata.get("doc_type", ""),
            }
            for m in results.matches
        ]

    def _stub_results(self, top_k: int) -> list[dict]:
        from wealth360.data.stub_research import STUB_RESEARCH_DOCS
        return STUB_RESEARCH_DOCS[:top_k]
