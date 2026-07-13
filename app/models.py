from langchain_mistralai import ChatMistralAI

from app.core.config import settings

llm = ChatMistralAI(
    model=settings.MISTRAL_MODEL,
    api_key=settings.MISTRAL_API_KEY,
    temperature=0.7,
)