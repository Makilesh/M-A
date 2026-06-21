# M&A Due Diligence Intelligence Engine — Decisions Log

All architecture decisions that deviated from or resolved ambiguities in p4.md are recorded here.

---

## Decision 1: Qdrant Quantization Config
- **Date**: Session 1
- **Context**: p4.md specifies INT8 quantization but doesn't specify always_ram setting
- **Resolution**: Set `always_ram=True` on ScalarQuantization for fast retrieval. Trade-off: higher memory usage, lower latency.
- **Impact**: collection_manager.py

## Decision 2: BM25 via FastEmbed
- **Date**: Session 2
- **Context**: p4.md says "FastEmbed BM25" but doesn't specify exact class/method
- **Resolution**: Used `fastembed.SparseTextEmbedding(model_name="Qdrant/bm25")` which produces Qdrant-native SparseVector objects directly
- **Impact**: hybrid_search.py

## Decision 3: asyncio.Lock() creation timing
- **Date**: Session 2
- **Context**: p4.md warns "asyncio.Lock() requires running event loop" but doesn't specify where to create rate limiter locks
- **Resolution**: Rate limiters in BudgetTracker are created lazily via `_get_rate_limiter()` on first use, not at class definition time. This prevents the "no running event loop" error.
- **Impact**: budget_tracker.py, rate_limiter.py

## Decision 4: Agent 5 Heuristic vs LLM Split
- **Date**: Session 2
- **Context**: p4.md says "Primary: heuristics (~60% of queries), Fallback: LLM on ambiguity"
- **Resolution**: Implemented three heuristic paths: (1) clearly good (mean_score >= 0.7), (2) clearly bad (mean_score < 0.2), (3) ambiguous → LLM. Thresholds chosen empirically based on typical reranker score distributions.
- **Impact**: quality_assessor.py

## Decision 5: TOCTOU Budget Race Condition
- **Date**: Session 2
- **Context**: p4.md's budget tracker used separate _budget_available() + _increment() calls
- **Resolution**: Replaced with atomic _try_consume() using conditional UPDATE. Single SQL statement: `UPDATE ... SET used_today = used_today + 1 WHERE used_today < limit`. Prevents two concurrent requests from both passing the check and overshooting.
- **Impact**: budget_tracker.py

## Decision 6: gemini model string format
- **Date**: Session 2
- **Context**: p4.md references "gemini-3.5-flash" and "gemini-3.1-flash-lite" but LiteLLM model strings need prefix
- **Resolution**: Used "gemini/gemini-3.5-flash" and "gemini/gemini-3.1-flash-lite" format for LiteLLM routing. Marked with ⚠ VERIFY in code for runtime validation.
- **Impact**: budget_tracker.py

## Decision 7: Rewriter JSON key → State key mapping
- **Date**: Session 2
- **Context**: p4.md's Agent 6 output uses `updated_retrieval_config` and `updated_metadata_filters` but AgentState uses `retrieval_config` and `extracted_filters`
- **Resolution**: query_rewriter_node explicitly maps keys when returning partial state. Documented in prompt template docstring.
- **Impact**: query_rewriter.py

## Decision 8: Docker Compose Ollama connectivity
- **Date**: Session 2
- **Context**: Agents 4 and 8 use local Ollama which runs on the host, not in Docker
- **Resolution**: Set OLLAMA_API_BASE to `http://host.docker.internal:11434` in Docker Compose. This resolves to the host machine on both Docker Desktop (Mac/Windows) and newer Docker Engine (Linux with --add-host).
- **Impact**: docker-compose.yml

## Decision 9: Missing dependencies beyond p4.md requirements.txt
- **Date**: Session 3
- **Context**: p4.md's requirements.txt lists `asyncpg` and `psycopg2-binary` for Postgres but does NOT list `langgraph-checkpoint-postgres` or `psycopg[binary]`. At runtime, `from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver` (used in orchestrator.py per p4.md's own code) fails with `ModuleNotFoundError: No module named 'langgraph.checkpoint.postgres'`. The `langgraph` pip package does NOT bundle the postgres checkpoint adapter — it's a separate package. Furthermore, `langgraph-checkpoint-postgres` depends on `psycopg` (v3, async-native), not `psycopg2-binary` (v2, sync-only). The binary wheel (`psycopg[binary]`) is needed on systems without `libpq` development headers.
- **Resolution**: Added `langgraph-checkpoint-postgres>=2.0.0,<3.0.0` and `psycopg[binary]>=3.1.0,<4.0.0` to requirements.txt. Pinned `<3.0.0` to avoid breaking changes with `langgraph>=0.2.0,<0.3.0` (version 3.x of checkpoint-postgres requires langgraph 0.3+). Validated: 76/76 tests pass after addition.
- **Impact**: requirements.txt

## Decision 10: Docker stub directory cleanup
- **Date**: Session 4
- **Context**: Phase 0 scaffold created `docker/Dockerfile`, `docker/docker-compose.yml`, and `docker/qdrant_config.yaml` as stubs. Phase 6 then placed the real implementations at project root (`Dockerfile`, `Dockerfile.streamlit`, `docker-compose.yml`) and the Qdrant config at `config/qdrant_config.yaml`. The `docker/` stubs were never updated and contained only placeholder comments.
- **Resolution**: Deleted `docker/` directory entirely. Fixed `README.md` reference from `docker compose -f docker/docker-compose.yml up -d` to `docker compose up -d`.
- **Impact**: docker/, README.md

