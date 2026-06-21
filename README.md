# M&A Due Diligence Intelligence Engine

Production-grade Hybrid Agentic RAG system for M&A Due Diligence. Ingests data room documents (PDF, DOCX, PPTX, Excel) and enables complex natural language queries with multi-hop reasoning, numerical precision, and traceable citations.

## Architecture

- **Vector Database**: Qdrant (self-hosted, Docker) — hybrid dense + sparse search
- **Orchestration**: LangGraph StateGraph with PostgresSaver checkpointing
- **LLM Primary**: Gemini 3.1 Flash Lite via LiteLLM (budget-tracked)
- **LLM Synthesis**: Gemini 3.5 Flash (reserved for answer generation)
- **LLM Fallback**: Qwen2.5:14b via Ollama (local GPU)
- **Embeddings**: BAAI/bge-m3 (1024-dim, 8192 max tokens)
- **Reranker**: BAAI/bge-reranker-v2-m3 (cross-encoder, sigmoid-normalized)
- **Sparse Search**: FastEmbed BM25 (Qdrant native)

## Quick Start

```bash
# 1. Clone and configure
cp .env.example .env
# Edit .env with your API keys and passwords

# 2. Install PyTorch (match your CUDA version)
pip install torch --index-url https://download.pytorch.org/whl/cu124

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start services via Docker Compose
docker compose up -d

# 5. Run the application
streamlit run app/streamlit_app.py
```

## Tech Stack

See `p4.md` for the complete v9 System Prompt Architecture Specification.

## License

Proprietary — all rights reserved.
