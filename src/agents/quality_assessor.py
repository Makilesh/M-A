# src/agents/quality_assessor.py
# Agent 5 — Quality Assessor Agent
# Primary: heuristics (no LLM, ~60% of queries) | Fallback: gemini-3.1-flash-lite on ambiguity
# JSON mode when LLM invoked: response_format={"type": "json_object"}
# Implemented in Phase 4, BUILD ORDER step 15
