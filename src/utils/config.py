# src/utils/config.py
# Pydantic v2 settings + python-dotenv + YAML config loading
# Implemented in Phase 0
"""
Application configuration using Pydantic v2 settings.
Loads from environment variables and .env file.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # --- LLM API Keys ---
    gemini_api_key: str = Field(default="", description="Gemini API key")

    # --- Database ---
    postgres_url: str = Field(
        default="postgresql://manda_user:password@localhost:5432/manda_rag",
        description="PostgreSQL connection string",
    )

    # --- Qdrant ---
    qdrant_url: str = Field(
        default="http://localhost:6333",
        description="Qdrant server URL",
    )
    qdrant_grpc_port: int = Field(
        default=6334,
        description="Qdrant gRPC port",
    )

    # --- Ollama ---
    ollama_url: str = Field(
        default="http://localhost:11434",
        description="Ollama server URL",
    )

    # --- Application ---
    log_level: str = Field(default="INFO", description="Logging level")
    environment: str = Field(default="development", description="Environment name")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Returns cached application settings singleton."""
    return Settings()
