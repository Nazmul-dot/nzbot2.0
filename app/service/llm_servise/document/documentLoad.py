import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mistralai import MistralAIEmbeddings
from langchain_chroma import Chroma
from app.core.config import settings



# --- 1. Load ---
pdf_path = Path(__file__).parent / "nz.pdf"
loader = PyPDFLoader(str(pdf_path))
documents = loader.load()
print(f"Loaded {len(documents)} page(s)")

# --- 2. Split ---
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". ", " ", ""],
)
chunks = splitter.split_documents(documents)
print(f"Split into {len(chunks)} chunk(s)")

# --- 3. Embed ---
# embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

embedding_model = MistralAIEmbeddings(
    model="mistral-embed",
    api_key=settings.MISTRAL_API_KEY
)

# --- 4. Store in vector DB (Chroma, persisted to disk) ---
persist_dir = Path(__file__).parent / "chroma_db"
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=str(persist_dir),
    collection_name="hole_pdf",
)
print(f"Stored {len(chunks)} vectors in {persist_dir}")

# --- Quick sanity check ---
results = vector_store.similarity_search("explain about The term ‘black hole’ ", k=4)
for r in results:
    print("---")
    print(r.page_content[:200])