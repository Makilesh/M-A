# M&A Due Diligence Intelligence Engine — Progress Tracker

## Project Status: In Progress

## Current Phase: Phase 1 — Foundation
## Current Step: 1.1 — Token counter (BUILD ORDER step 1)

---

## Phase Checklist

- [x] **Phase 0**: Project scaffold — directory structure, pinned requirements.txt, .env/config skeleton, git init, empty PROGRESS/DECISIONS_LOG committed
- [ ] **Phase 1**: Foundation — token counter, Qdrant collection setup, async embedding wrapper, FastEmbed BM25
- [ ] **Phase 2**: Ingestion — document processors (PDF/DOCX/PPTX/Excel), version resolver, PII detector, chunking pipeline
- [ ] **Phase 3**: Retrieval core — flatten_deduplicate + RRF fusion, hybrid search, async reranker, parent + sibling retrieval
- [ ] **Phase 4**: Orchestration — budget tracker, LiteLLM wrapper, all agents, LangGraph state graph + PostgresSaver
- [ ] **Phase 5**: Interfaces — Streamlit UI, FastAPI layer
- [ ] **Phase 6**: Deployment & validation — Docker Compose, golden Q&A eval suite

---

## Last Session Summary

Session 1: Read p4.md (2808 lines). Created PROGRESS.md, DECISIONS_LOG.md. Completed Phase 0: full directory structure (95 files), requirements.txt, .env.example, config YAMLs (qdrant/litellm/chunking), README, all module stubs matching p4.md PROJECT STRUCTURE. Git committed.

## Next Action

Implement token counter (src/utils/token_counter.py) using AutoTokenizer from BAAI/bge-m3 per p4.md BUILD ORDER step 1. Then proceed to Qdrant collection setup (step 2).

## Known Issues / Blockers

- None
