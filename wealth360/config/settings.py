from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Azure OpenAI
    azure_openai_api_key: str = "stub-key"
    azure_openai_endpoint: str = "https://stub.openai.azure.com/"
    azure_openai_deployment: str = "gpt-4o"
    azure_openai_api_version: str = "2024-02-01"
    azure_openai_embedding_deployment: str = "text-embedding-3-small"

    # Pinecone
    pinecone_api_key: str = "stub-key"
    pinecone_environment: str = "us-east1-gcp"
    pinecone_index_name: str = "wealth360-poc"
    pinecone_dimension: int = 1536

    # OpenTelemetry / Grafana Cloud
    otel_service_name: str = "wealth360-advisor"
    otel_enabled: bool = False
    grafana_otlp_endpoint: str = "https://otlp-gateway-prod-us-east-0.grafana.net/otlp"
    grafana_otlp_token: str = "stub-token"

    # Grafana Cloud API (for dashboard deployment)
    grafana_cloud_url: str = "https://your-stack.grafana.net"
    grafana_api_token: str = "stub-grafana-api-token"

    # App
    app_env: str = "local"
    use_stub_data: bool = True
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
