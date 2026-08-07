# Nexus AI Architecture Reference Document

Nexus AI is an Autonomous Multi-Agent Research Platform built on LangGraph, Ollama, and Tavily Search.

Key Specifications:
- Multi-agent orchestration via LangGraph StateGraph.
- Local LLM inference using Ollama qwen3:4b model.
- Local document vector index powered by FAISS and HuggingFace all-MiniLM-L6-v2 embeddings.
- Automatic self-correcting reflection re-search loops.
- Persistent SQLite checkpoint memory stored in nexus_memory.db.
- Domain-grouped modular node architecture.
