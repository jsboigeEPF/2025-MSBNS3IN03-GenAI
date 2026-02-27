"""
Configuration centralisée — toutes les clés API et paramètres
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # ── Serveur ────────────────────────────────────────────────
    PORT: int = 8000
    DEBUG: bool = True



    # ── OpenAI ─────────────────────────────────────────────────
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_MODEL_MINI: str = "gpt-4o-mini"

    # ── OpenRouter (fallback LLM) ───────────────────────────────
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    # ── Qdrant (mémoire vectorielle) ───────────────────────────
    QDRANT_URL: str = "https://students.qdrant.myia.io"
    QDRANT_API_KEY: str = ""
    QDRANT_COLLECTION: str = "rapports"

    # ── SearxNG (recherche web) ────────────────────────────────
    SEARXNG_URL: str = "https://search.myia.io"

    # ── Export ─────────────────────────────────────────────────
    EXPORT_DIR: str = "exports"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
