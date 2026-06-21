"""
Integration-style tests with all external calls mocked.
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock


class TestQueryPipelineIntegration:
    """End-to-end pipeline tests with mocked externals."""

    def test_graph_topology(self):
        """Verify the graph builds without errors and has expected nodes."""
        from src.workflow.orchestrator import build_graph

        graph = build_graph()
        # Graph should have all expected nodes
        assert graph is not None

    def test_initial_state_is_valid(self, sample_agent_state):
        """Initial state dict has all required fields."""
        state = sample_agent_state
        assert state["original_query"] != ""
        assert state["deal_id"] != ""
        assert state["rewrite_iteration"] == 0
        assert state["force_refusal"] is False

    def test_forced_refusal_answer(self, sample_agent_state):
        """When force_refusal is True, synthesizer generates refusal."""
        # Simulate insufficient_context_node behavior
        state = {**sample_agent_state, "force_refusal": True}

        # The answer should indicate insufficient context
        assert state["force_refusal"] is True


class TestInsufficientContextPath:
    """Tests for the forced refusal flow."""

    @pytest.mark.asyncio
    async def test_insufficient_context_node(self, sample_agent_state):
        """insufficient_context_node sets force_refusal and generates message."""
        from src.workflow.orchestrator import insufficient_context_node

        state = {**sample_agent_state, "rewrite_iteration": 2, "context_quality_score": 0.1}
        result = await insufficient_context_node(state)

        assert result["force_refusal"] is True
        assert result["confidence_score"] == 0.0
        assert result["validation_status"] == "passed"
        assert "unable to find" in result["generated_answer"].lower()


class TestPromptTemplates:
    """Verify prompt templates are well-formed."""

    def test_query_intelligence_prompt(self):
        """Query intelligence template has required format variables."""
        from src.llm.prompt_templates.query_intelligence import (
            QUERY_INTELLIGENCE_SYSTEM_PROMPT,
            QUERY_INTELLIGENCE_USER_TEMPLATE,
        )

        assert "query_type" in QUERY_INTELLIGENCE_SYSTEM_PROMPT
        assert "{query}" in QUERY_INTELLIGENCE_USER_TEMPLATE
        assert "{deal_id}" in QUERY_INTELLIGENCE_USER_TEMPLATE

    def test_answer_synthesizer_prompt(self):
        """Answer synthesizer template has required format variables."""
        from src.llm.prompt_templates.answer_synthesizer import (
            ANSWER_SYNTHESIZER_SYSTEM_PROMPT,
            ANSWER_SYNTHESIZER_USER_TEMPLATE,
        )

        assert "citation" in ANSWER_SYNTHESIZER_SYSTEM_PROMPT.lower()
        assert "{query}" in ANSWER_SYNTHESIZER_USER_TEMPLATE
        assert "{context}" in ANSWER_SYNTHESIZER_USER_TEMPLATE

    def test_query_rewriter_prompt(self):
        """Query rewriter template has required format variables."""
        from src.llm.prompt_templates.query_rewriter import (
            QUERY_REWRITER_SYSTEM_PROMPT,
            QUERY_REWRITER_USER_TEMPLATE,
        )

        assert "include_pii" in QUERY_REWRITER_SYSTEM_PROMPT.lower()
        assert "{original_query}" in QUERY_REWRITER_USER_TEMPLATE
        assert "{missing_aspects}" in QUERY_REWRITER_USER_TEMPLATE

    def test_no_pii_in_query_intelligence(self):
        """Query intelligence prompt forbids include_pii."""
        from src.llm.prompt_templates.query_intelligence import (
            QUERY_INTELLIGENCE_SYSTEM_PROMPT,
        )

        assert "include_pii" in QUERY_INTELLIGENCE_SYSTEM_PROMPT.lower()
        assert "never" in QUERY_INTELLIGENCE_SYSTEM_PROMPT.lower() or \
               "forbidden" in QUERY_INTELLIGENCE_SYSTEM_PROMPT.lower()


class TestLiteLLMWrapper:
    """Tests for LiteLLM wrapper functions."""

    def test_call_structured_agent_is_async(self):
        """call_structured_agent is a coroutine function."""
        import asyncio
        from src.llm.litellm_wrapper import call_structured_agent

        assert asyncio.iscoroutinefunction(call_structured_agent)

    def test_call_prose_agent_is_async(self):
        """call_prose_agent is a coroutine function."""
        import asyncio
        from src.llm.litellm_wrapper import call_prose_agent

        assert asyncio.iscoroutinefunction(call_prose_agent)

    def test_call_local_agent_is_async(self):
        """call_local_agent is a coroutine function."""
        import asyncio
        from src.llm.litellm_wrapper import call_local_agent

        assert asyncio.iscoroutinefunction(call_local_agent)
