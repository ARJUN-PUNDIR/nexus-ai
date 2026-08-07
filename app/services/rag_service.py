"""
LangChain Document RAG Service for Nexus AI
Handles document loading (PDF, Word, CSV, TXT), text splitting, HuggingFace embeddings, and FAISS vector index storage.
"""

import os
from pathlib import Path
from typing import Any

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from app.models.schemas import SearchResultItem


RAG_STORAGE_DIR = "rag_storage"
DATA_DIR = "data"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_vectorstore = None


def get_embeddings():
    """Initializes local HuggingFace embeddings."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)


def load_single_document(file_path: str) -> list[Any]:
    """
    Uses LangChain Document Loaders to parse PDF, CSV, TXT, MD files.
    """
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".csv":
        loader = CSVLoader(file_path)
    elif ext in [".txt", ".md"]:
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        # Fallback to TextLoader
        loader = TextLoader(file_path, encoding="utf-8")

    return loader.load()


def ingest_documents_from_directory(directory_path: str = DATA_DIR) -> int:
    """
    Ingests all files from data/ directory, chunks them, creates HuggingFace embeddings,
    and saves the FAISS index to disk.
    """
    global _vectorstore

    dir_path = Path(directory_path)
    if not dir_path.exists():
        dir_path.mkdir(parents=True, exist_ok=True)
        return 0

    all_docs = []
    supported_exts = {".pdf", ".csv", ".txt", ".md"}

    for file_path in dir_path.iterdir():
        if file_path.suffix.lower() in supported_exts:
            try:
                docs = load_single_document(str(file_path))
                all_docs.extend(docs)
            except Exception as e:
                print(f"⚠️ Error loading {file_path.name}: {e}")

    if not all_docs:
        return 0

    # LangChain text splitting strategy
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(all_docs)

    embeddings = get_embeddings()

    # Build FAISS vector store using LangChain
    _vectorstore = FAISS.from_documents(chunks, embeddings)

    # Save local vector store
    os.makedirs(RAG_STORAGE_DIR, exist_ok=True)
    _vectorstore.save_local(RAG_STORAGE_DIR)

    return len(chunks)


def query_rag_index(query: str, top_k: int = 4) -> list[SearchResultItem]:
    """
    Queries local FAISS index and returns SearchResultItem list with source_type="document".
    """
    global _vectorstore

    index_file = Path(RAG_STORAGE_DIR) / "index.faiss"
    if not index_file.exists():
        ingest_documents_from_directory(DATA_DIR)

    index_file = Path(RAG_STORAGE_DIR) / "index.faiss"
    if not index_file.exists():
        return []

    if _vectorstore is None:
        embeddings = get_embeddings()
        _vectorstore = FAISS.load_local(
            RAG_STORAGE_DIR, embeddings, allow_dangerous_deserialization=True
        )

    retrieved_docs = _vectorstore.similarity_search(query, k=top_k)

    results = []
    for doc in retrieved_docs:
        source_name = doc.metadata.get("source", "Local Document")
        results.append(
            SearchResultItem(
                title=f"Document: {Path(source_name).name}",
                url="",
                content=doc.page_content,
                source_type="document",
                metadata=doc.metadata,
            )
        )

    return results
