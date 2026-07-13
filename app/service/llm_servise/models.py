"""Lazy creation of the configured LLM client."""

from functools import lru_cache

from app.core.config import settings


@lru_cache(maxsize=1)
def get_llm():
    """Create the Mistral client only when the first chat request arrives."""
    if not settings.MISTRAL_API_KEY:
        raise RuntimeError("MISTRAL_API_KEY is not configured.")

    from langchain_mistralai import ChatMistralAI

    return ChatMistralAI(
        model=settings.MISTRAL_MODEL,
        api_key=settings.MISTRAL_API_KEY,
        temperature=0.7,
    )
