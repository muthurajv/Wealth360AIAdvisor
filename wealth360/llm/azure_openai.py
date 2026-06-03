from functools import lru_cache
from langchain_openai import AzureChatOpenAI
from wealth360.config.settings import get_settings


@lru_cache(maxsize=1)
def get_llm() -> AzureChatOpenAI:
    s = get_settings()
    return AzureChatOpenAI(
        azure_deployment=s.azure_openai_deployment,
        azure_endpoint=s.azure_openai_endpoint,
        api_key=s.azure_openai_api_key,
        api_version=s.azure_openai_api_version,
        temperature=0,
        max_retries=3,
    )
