from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "enterprise-agentic-ai"
    environment: str = "development"
    log_level: str = "INFO"

    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_api_version: str = "2025-01-01-preview"
    azure_openai_chat_deployment: str = ""
    azure_openai_embedding_deployment: str = ""

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/agentdb"
    redis_url: str = "redis://localhost:6379/0"

    top_k: int = 5
    chunk_size: int = 800
    chunk_overlap: int = 120

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
