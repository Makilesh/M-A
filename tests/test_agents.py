"""
Tests for agent nodes with mocked LLM calls.
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock


class TestRetrievalStrategy:
    """Tests for Agent 2 — deterministic retrieval config."""

    def test_financial_config(self):
        """Financial query returns financial-optimized config."""
        from src.agents.retrieval_strategy import get_retrieval_config

        config = get_retrieval_config("financial", {})
        assert config["dense_weight"] == 0.5
        assert config["sparse_weight"] == 0.5
        assert config["use_parent_expansion"] is True
        assert config["use_sibling_expansion"] is True

    def test_legal_config(self):
        """Legal query weights sparse higher for keyword matching."""
        from src.agents.retrieval_strategy import get_retrieval_config

        config = get_retrieval_config("legal", {})
        assert config["sparse_weight"] > config["dense_weight"]

    def test_unknown_type_defaults_to_summary(self):
        """Unknown query type falls back to summary config."""
        from src.agents.retrieval_strategy import get_retrieval_config

        config = get_retrieval_config("nonexistent_type", {})
        # Should get summary config (the fallback)
        assert config is not None
        assert "dense_weight" in config

    def test_numerical_precision_raises_threshold(self):
        """requires_numerical_precision raises reranker threshold."""
        from src.agents.retrieval_strategy import get_retrieval_config

        config_normal = get_retrieval_config("financial", {})
        config_precise = get_retrieval_config(
            "financial", {"requires_numerical_precision": True}
        )

        assert config_precise["reranker_threshold"] >= config_normal["reranker_threshold"]

    def test_cross_document_increases_top_k(self):
        """requires_cross_document increases top_k values."""
        from src.agents.retrieval_strategy import get_retrieval_config

        config_normal = get_retrieval_config("summary", {})
        config_cross = get_retrieval_config(
            "summary", {"requires_cross_document": True}
        )

        assert config_cross["top_k_dense"] >= config_normal["top_k_dense"]

    def test_all_query_types_have_config(self):
        """All 5 query types return valid configs."""
        from src.agents.retrieval_strategy import get_retrieval_config

        for qt in ["financial", "legal", "comparative", "summary", "multi_hop"]:
            config = get_retrieval_config(qt, {})
            assert "dense_weight" in config
            assert "sparse_weight" in config
            assert "reranker_threshold" in config


class TestQualityAssessorHeuristic:
    """Tests for Agent 5 heuristic path (no LLM needed)."""

    def test_no_chunks_forces_refusal(self, sample_agent_state):
        """Empty results force refusal."""
        from src.agents.quality_assessor import _heuristic_assessment

        state = {**sample_agent_state, "reranked_results": []}
        result = _heuristic_assessment(state)

        assert result is not None
        assert result["context_quality_score"] == 0.0
        assert result["force_refusal"] is True

    def test_high_scores_pass_heuristic(self, sample_agent_state):
        """High reranker scores pass without LLM."""
        from src.agents.quality_assessor import _heuristic_assessment

        chunks = [
            {"reranker_score": 0.9, "source_file": "f1.pdf"},
            {"reranker_score": 0.85, "source_file": "f2.pdf"},
            {"reranker_score": 0.8, "source_file": "f3.pdf"},
        ]
        state = {**sample_agent_state, "reranked_results": chunks}
        result = _heuristic_assessment(state)

        assert result is not None
        assert result["context_quality_score"] > 0.5
        assert result["force_refusal"] is False
        assert result["quality_method"] == "heuristic"

    def test_low_scores_detected(self, sample_agent_state):
        """Low reranker scores detected by heuristic."""
        from src.agents.quality_assessor import _heuristic_assessment

        chunks = [
            {"reranker_score": 0.1, "source_file": "f1.pdf"},
            {"reranker_score": 0.05, "source_file": "f2.pdf"},
        ]
        state = {**sample_agent_state, "reranked_results": chunks}
        result = _heuristic_assessment(state)

        assert result is not None
        assert result["context_quality_score"] < 0.3

    def test_ambiguous_falls_through_to_llm(self, sample_agent_state):
        """Ambiguous scores return None (triggering LLM fallback)."""
        from src.agents.quality_assessor import _heuristic_assessment

        chunks = [
            {"reranker_score": 0.5, "source_file": "f1.pdf"},
            {"reranker_score": 0.4, "source_file": "f2.pdf"},
            {"reranker_score": 0.35, "source_file": "f3.pdf"},
        ]
        state = {**sample_agent_state, "reranked_results": chunks}
        result = _heuristic_assessment(state)

        # Ambiguous — should return None to trigger LLM
        assert result is None
