# Codebase Chat

Ask questions about any GitHub repo. 100% local and free: Ollama + ChromaDB.

## Setup
```
ollama pull nomic-embed-text
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python -m app.ingest <repo-url-or-path>
python -m app.ask "where is authentication handled?"
```

## Roadmap
- [x] Basic RAG pipeline
- [ ] tree-sitter chunking (functions/classes)
- [ ] Hybrid BM25 + vector search, reranking
- [ ] Eval set + metrics
- [ ] FastAPI + Streamlit UI
- [ ] Agent tools, Docker, deploy
