from functools import lru_cache
from wealth360.config.settings import get_settings


@lru_cache(maxsize=1)
def get_pinecone_index():
    s = get_settings()
    if s.use_stub_data or s.pinecone_api_key == "stub-key":
        return None
    from pinecone import Pinecone
    pc = Pinecone(api_key=s.pinecone_api_key)
    return pc.Index(s.pinecone_index_name)
