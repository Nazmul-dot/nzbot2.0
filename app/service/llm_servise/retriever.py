"""Vector store retrieval for RAG-augmented chat."""

from pathlib import Path

from langchain_chroma import Chroma
from langchain_mistralai import MistralAIEmbeddings

from app.core.config import settings

# Must match the persist_dir / collection_name used in your ingestion script
PERSIST_DIR = Path(__file__).parent / "document" / "chroma_db"
COLLECTION_NAME = "hole_pdf"

_embedding_model = MistralAIEmbeddings(
    model="mistral-embed",
    api_key=settings.MISTRAL_API_KEY,
)

_vector_store = Chroma(
    persist_directory=str(PERSIST_DIR),
    embedding_function=_embedding_model,
    collection_name=COLLECTION_NAME,
)


def retrieve_context(query: str, k: int = 4) -> str:
    """
    Retrieve the top-k relevant chunks for a query and join them
    into a single context string for the LLM prompt.
    """
    results = _vector_store.similarity_search(query, k=k)
    if not results:
        return ""
    return "\n\n".join(doc.page_content for doc in results)