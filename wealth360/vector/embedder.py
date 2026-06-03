from langchain_openai import AzureOpenAIEmbeddings
from wealth360.config.settings import get_settings


def get_embedder() -> AzureOpenAIEmbeddings:
    s = get_settings()
    return AzureOpenAIEmbeddings(
        azure_deployment=s.azure_openai_embedding_deployment,
        azure_endpoint=s.azure_openai_endpoint,
        api_key=s.azure_openai_api_key,
        api_version=s.azure_openai_api_version,
    )
