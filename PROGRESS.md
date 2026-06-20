# M&A Due Diligence Intelligence Engine — Progress Tracker

## Project Status: In Progress

## Current Phase: Phase 2 — Ingestion + Phase 3 — Retrieval Core
## Current Step: 2.1 — RRF Fusion (BUILD ORDER step 9), then document processors

---

## Phase Checklist

- [x] **Phase 0**: Project scaffold — directory structure, pinned requirements.txt, .env/config skeleton, git init
- [x] **Phase 1**: Foundation — token counter, Qdrant collection setup, async embedding wrapper, FastEmbed BM25
- [ ] **Phase 2**: Ingestion — document processors (PDF/DOCX/PPTX/Excel), version resolver, PII detector, chunking pipeline
- [ ] **Phase 3**: Retrieval core — flatten_deduplicate + RRF fusion, hybrid search, async reranker, parent + sibling retrieval
- [ ] **Phase 4**: Orchestration — budget tracker, LiteLLM wrapper, all agents, LangGraph state graph + PostgresSaver
- [ ] **Phase 5**: Interfaces — Streamlit UI, FastAPI layer
- [ ] **Phase 6**: Deployment & validation — Docker Compose, golden Q&A eval suite

---

## Last Session Summary

Session 2: Committed Phase 1 — token_counter.py (AutoTokenizer bge-m3), constants.py (VECTOR_SIZE=1024, QUANTIZED_SEARCH_PARAMS), qdrant_client.py (AsyncQdrantClient singleton), collection_manager.py (HNSW m=16/ef=200, INT8 quantization, payload indexes), reranker.py (embedding + reranker with sigmoid, dual ThreadPoolExecutors), hybrid_search.py (BM25 via FastEmbed, filter builder, parallel dense+sparse search, fetch_chunks_by_ids).

## Next Action

Implement RRF fusion (rrf_fusion.py), sibling/parent retrieval, then document processors (PDF/DOCX/PPTX/Excel), chunking pipeline, version resolver, PII detector.

## Known Issues / Blockers

- None
