# 🤖 NEXUS AI RESEARCH PLATFORM

> **A modular multi-agent research platform built with LangGraph and LangChain. It combines intelligent intent routing, autonomous planning, 2-stage hybrid retrieval (Web + Local Documents), reflection-based validation, and persistent conversational memory.**

[![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Stateful_Workflows-FF6F61?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/langgraph)
[![LangChain](https://img.shields.io/badge/LangChain-RAG_Framework-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![FAISS](https://img.shields.io/badge/FAISS-Vector_Store-0467DF?style=for-the-badge)](https://github.com/facebookresearch/faiss)
[![FlashRank](https://img.shields.io/badge/FlashRank-Re--Ranking-FFD700?style=for-the-badge)](https://github.com/PrithivirajDamodaran/FlashRank)
[![Ollama](https://img.shields.io/badge/Ollama-Local_Inference-000000?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.ai/)
[![Pytest](https://img.shields.io/badge/Pytest-29_Passed-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)

---

## 🌟 Executive Summary

**Nexus AI** is a modular multi-agent research platform designed for information retrieval, local document analysis, and report synthesis. Built using **LangGraph**, **LangChain**, **Ollama**, **FlashRank**, and **FAISS**, it orchestrates stateful multi-agent workflows with human-in-the-loop plan reviews, reflection-based validation, and persistent memory.

---

## 🎯 2-Stage RAG Retrieval Pipeline (FAISS + FlashRank Re-Ranking)

Nexus AI utilizes a **2-Stage Retrieval Architecture** to ensure accurate document context selection:

```text
 ┌─────────────────────────┐
 │       User Query        │
 └────────────┬────────────┘
              │
              ▼
 ┌─────────────────────────┐
 │   Stage 1: FAISS Fetch  │ ──► Bi-Encoder similarity retrieval of candidate chunks
 └────────────┬────────────┘
              │
              ▼
 ┌─────────────────────────┐
 │   Stage 2: FlashRank    │ ──► Cross-Encoder model re-ranks candidate chunks &
 │   (ms-marco-TinyBERT)   │     selects highest precision matches
 └────────────┬────────────┘
              │
              ▼
 ┌─────────────────────────┐
 │     Report Writer       │ ──► Receives relevant document context
 └─────────────────────────┘
```

---

## 🔀 Centralized Model Factory & Switcher (`settings.py`)

Switch LLM models and Embedding providers by configuring settings in [`app/config/settings.py`](file:///Users/arjunsinghpundir/Desktop/nexus-ai/app/config/settings.py). All secret keys are loaded from `.env`.

```python
# app/config/settings.py

# LLM Provider Options: "ollama", "openai", "anthropic"
LLM_PROVIDER = "ollama"
LLM_MODEL_NAME = "qwen3:4b"  # or "gpt-4o", "claude-3-5-sonnet-20241022", "llama3.1:8b"

# Embedding Provider Options: "huggingface", "ollama", "openai"
EMBEDDING_PROVIDER = "huggingface"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
```

---

## 🧠 Master Graph Architecture

```mermaid
graph TD
    START([START]) --> Router{🤔 Smart 4-Way Intent Router}
    
    Router -- "DIRECT (Memory/Chat)" --> DirectResponder[💬 Direct Responder Node]
    Router -- "WEB (Live News)" --> PlannerWeb[🎯 Autonomous Planner Node]
    Router -- "DOC (Local RAG)" --> RAGDoc[📚 2-Stage FlashRank RAG Node]
    Router -- "HYBRID (Web + Docs)" --> PlannerHybrid[🎯 Autonomous Planner Node]
    
    PlannerWeb --> HumanApproval[🛑 Human Plan Approval Node<br/>Approve / Edit / Cancel]
    PlannerHybrid --> HumanApproval
    
    HumanApproval --> RouteApproval{👉 User Choice Edge}
    RouteApproval -- "Approve / Edit [y/e]" --> SearcherWeb[🔍 Parallel Web Searcher Node]
    RouteApproval -- "Cancel [n]" --> Writer[✍️ Writer Node]

    SearcherWeb --> Reflection[🧐 Reflection Audit Node]
    RAGDoc --> Reflection

    Reflection --> RouteReflection{🔄 Re-Search Router Edge}
    RouteReflection -- "INCOMPLETE & loop < 2" --> SearcherWeb
    RouteReflection -- "COMPLETE or max loops" --> Writer

    DirectResponder --> END([END])
    Writer --> END([END])
```

---

## ⚡ 4-Way Smart Intent Router Matrix

Nexus AI routes prompts into 4 specialized execution paths:

| Intent Route | Description | Workflow Path | Tavily Search API Calls | FAISS Vector Store Calls |
|---|---|---|---|---|
| 💡 **`DIRECT`** | Casual greetings, personal memory, coding, math, general knowledge | `direct_responder` $\rightarrow$ `END` | **0** | **0** |
| 🌐 **`WEB`** | Real-time live web news, stock market updates, online research | `planner` $\rightarrow$ `human_review` $\rightarrow$ `searcher` $\rightarrow$ `reflection` $\rightarrow$ `writer` | **Parallel (3)** | **0** |
| 📚 **`DOC`** | Explicit queries regarding local files in `data/` (PDF, CSV, Word, TXT) | `rag_searcher` $\rightarrow$ `reflection` $\rightarrow$ `writer` | **0 (Saved!)** | **Top-4 Re-ranked** |
| 🔀 **`HYBRID`** | Complex queries comparing local document data with live web news | `planner` $\rightarrow$ `human_review` $\rightarrow$ `searcher` $\rightarrow$ `rag_searcher` $\rightarrow$ `reflection` $\rightarrow$ `writer` | **Parallel (3)** | **Top-4 Re-ranked** |

---

## 🔥 Technical Features

- 🎯 **2-Stage FlashRank Re-Ranking**: Combines vector retrieval with an ONNX cross-encoder re-ranker (`ms-marco-TinyBERT-L-2-v2`) for improved retrieval precision.
- 🔀 **Centralized Model Factory**: Instantiates LLMs (Ollama, OpenAI, Claude) and Embeddings dynamically through `get_llm()` and `get_embedding_model()`.
- 🛑 **Human-in-the-Loop Plan Review**: Pauses execution after the Planner Agent decomposes queries, giving the user control to **Approve (`y`)**, **Edit (`e`)**, or **Cancel (`n`)** before search API credits are spent.
- 🔄 **Reflection Audit Loop**: Evaluates context quality using `reflection_node`. If retrieved data is incomplete, triggers a targeted supplementary re-search loop.
- ⚡ **Concurrent Web Search**: Executes multi-query searches concurrently using Python `ThreadPoolExecutor`.
- 📚 **Local Hybrid RAG Engine**: Loads PDFs, CSVs, Word documents, and Markdown files using LangChain loaders, chunks text via `RecursiveCharacterTextSplitter`, embeds locally, and queries local **FAISS** vector store.
- 💾 **Persistent SQLite Memory Checkpointer**: Saves thread checkpoints and running summaries to `nexus_memory.db` via `SqliteSaver`, retaining long-term user context across terminal restarts.

---

## 📁 Domain-Grouped Directory Structure

```text
nexus-ai/
├── app/
│   ├── config/              # Centralized environment settings & Model Factory (Ollama, OpenAI, Claude)
│   ├── graph/
│   │   ├── state.py         # AgentState TypedDict schema
│   │   └── workflow.py      # Clean LangGraph edge wiring & graph compilation
│   ├── manager/             # ResearchManager streaming execution engine
│   ├── models/              # Pydantic data contracts (SearchItem, ResearchReport, ReflectionAudit)
│   ├── nodes/               # 📁 Domain-Grouped Workflow Nodes
│   │   ├── direct_nodes.py  # Router & Direct Responder nodes
│   │   ├── web_search_nodes.py # Planner, Searcher, & Reflection nodes
│   │   ├── human_nodes.py   # Human-in-the-Loop plan approval node
│   │   ├── rag_nodes.py     # Local 2-Stage FlashRank RAG searcher node
│   │   └── writer_node.py   # Markdown Report Writer node
│   ├── services/            # FAISS + FlashRank RAG Service & Report Exporter
│   ├── tools/               # Web search tools & custom wrappers
│   └── utils/               # SQLite memory saver & token summarizer helpers
├── data/                    # 📁 Drop your local PDFs, CSVs, Word docs here
├── rag_storage/             # Persistent local FAISS vector database
├── reports/                 # Output generated Markdown research reports
├── tests/                   # 🧪 Comprehensive 29-test Pytest suite
├── main.py                  # Terminal Interactive CLI entry point
└── requirements.txt         # Project dependencies
```

---

## 🚀 Quickstart & Installation Guide

### 1. Configure `.env` File
Create a `.env` file in the root directory:
```env
# Required for Web Search
TAVILY_API_KEY=tvly-your-actual-api-key-here

# Optional Model Provider API Keys
OPENAI_API_KEY=sk-proj-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Local Ollama Server URL
OLLAMA_BASE_URL=http://localhost:11434
```

### 2. Configure Model Selection in `app/config/settings.py`
```python
# Choose provider: "ollama", "openai", or "anthropic"
LLM_PROVIDER = "ollama"
LLM_MODEL_NAME = "qwen3:4b"

# Choose embedding: "huggingface", "ollama", or "openai"
EMBEDDING_PROVIDER = "huggingface"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
```

### 3. Run Interactive CLI
```bash
python main.py
```

---

## 🧪 Running Unit Tests

Run the complete 29-test Pytest suite:
```bash
myenv/bin/python -m pytest
```

```text
============================== test session starts ==============================
collected 29 items

tests/test_human.py ...                                                  [ 10%]
tests/test_memory.py ..                                                  [ 17%]
tests/test_model_factory.py ...                                          [ 27%]
tests/test_persistence.py .                                              [ 31%]
tests/test_planner.py .                                                  [ 34%]
tests/test_query_validator.py ...                                        [ 44%]
tests/test_rag.py .                                                      [ 48%]
tests/test_reflection.py ....                                            [ 62%]
tests/test_report_service.py .                                           [ 65%]
tests/test_router.py ....                                                [ 79%]
tests/test_schemas.py .....                                              [ 96%]
tests/test_search_formatter.py .                                         [100%]

======================== 29 passed, 1 warning in 0.53s =========================
```

---

## 📜 License & Acknowledgments

Built with ❤️ by **Arjun Singh Pundir** using [LangGraph](https://www.langchain.com/langgraph) and [Ollama](https://ollama.ai/).