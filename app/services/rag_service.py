"""
LangChain Document RAG Service for Nexus AI with 2-Stage FlashRank Re-Ranking
Handles document loading (PDF, Word, CSV, TXT), text splitting, Embeddings, FAISS vector search, and FlashRank Re-Ranking.
"""

import os
import sys
from pathlib import Path
from typing import Any

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from app.models.schemas import SearchResultItem
from app.config import get_embedding_model


RAG_STORAGE_DIR = "rag_storage"
DATA_DIR = "data"

_vectorstore = None
_reranker = None


def get_embeddings():
    """Initializes embeddings model via central Model Factory."""
    return get_embedding_model()


def get_reranker():
    """Initializes local FlashRank ONNX cross-encoder re-ranker."""
    global _reranker
    if _reranker is None:
        try:
            from flashrank import Ranker
        except ImportError:
            sys.path.append("/Users/arjunsinghpundir/Desktop/langchain_mastery/myenv/lib/python3.14/site-packages")
            from flashrank import Ranker
        _reranker = Ranker(model_name="ms-marco-TinyBERT-L-2-v2")
    return _reranker


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
        loader = TextLoader(file_path, encoding="utf-8")

    return loader.load()


def ingest_documents_from_directory(directory_path: str = DATA_DIR) -> int:
    """
    Ingests all files from data/ directory, chunks them, creates vector embeddings,
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
    2-Stage RAG Search Pipeline:
    - Stage 1: FAISS Similarity Search fetches top 12 candidate chunks.
    - Stage 2: FlashRank Cross-Encoder Re-ranks candidates and selects top 4 best chunks.
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

    # Stage 1: Fetch candidate chunks from FAISS (12 items)
    candidate_docs = _vectorstore.similarity_search(query, k=12)

    if not candidate_docs:
        return []

    # Stage 2: FlashRank Re-Ranking
    try:
        try:
            from flashrank import RerankRequest
        except ImportError:
            sys.path.append("/Users/arjunsinghpundir/Desktop/langchain_mastery/myenv/lib/python3.14/site-packages")
            from flashrank import RerankRequest

        ranker = get_reranker()

        passages = [
            {"id": idx, "text": doc.page_content, "meta": doc.metadata}
            for idx, doc in enumerate(candidate_docs)
        ]

        rerank_req = RerankRequest(query=query, passages=passages)
        reranked_results = ranker.rerank(rerank_req)[:top_k]

        results = []
        for item in reranked_results:
            meta = item.get("meta", {})
            source_name = meta.get("source", "Local Document")
            results.append(
                SearchResultItem(
                    title=f"Document (Re-ranked): {Path(source_name).name}",
                    url="",
                    content=item.get("text", ""),
                    source_type="document",
                    metadata=meta,
                )
            )
        return results

    except Exception as err:
        print(f"⚠️ FlashRank fallback to FAISS ({err})")
        results = []
        for doc in candidate_docs[:top_k]:
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
