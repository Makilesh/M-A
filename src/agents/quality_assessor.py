"""
Agent 5 — Quality Assessor Agent.

Primary: heuristics (no LLM, ~60% of queries)
Fallback: gemini-3.1-flash-lite on ambiguity

When heuristic signals are clear (high reranker scores, good coverage),
skip the LLM entirely. Only invoke the LLM when quality is borderline
and heuristics disagree.
"""

import json

import numpy as np

from src.llm.litellm_wrapper import call_structured_agent
from src.llm.budget_tracker import BudgetTracker
from src.llm.prompt_templates.quality_assessor import (
    QUALITY_ASSESSOR_SYSTEM_PROMPT,
    QUALITY_ASSESSOR_USER_TEMPLATE,
)
from src.workflow.state_definitions import AgentState
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def _heuristic_assessment(state: AgentState) -> dict | None:
    """
    Attempt heuristic quality assessment without LLM.
    Returns assessment dict if confident, None if LLM fallback needed.

    Heuristic signals:
    1. Mean reranker score of top-5 chunks
    2. Number of unique source files
    3. Query term coverage in retrieved chunks

    Args:
        state: Current AgentState with reranked_results.

    Returns:
        Assessment dict if heuristic is confident, None otherwise.
    """
    chunks = state.get("reranked_results", [])

    if not chunks:
        return {
            "context_quality_score": 0.0,
            "quality_breakdown": {"relevance": 0.0, "completeness": 0.0, "precision": 0.0},
            "missing_aspects": ["No chunks retrieved"],
            "quality_method": "heuristic",
            "force_refusal": True,
        }

    # Reranker score analysis
    scores = [c.get("reranker_score", 0.0) for c in chunks[:5]]
    mean_score = float(np.mean(scores)) if scores else 0.0
    min_score = float(np.min(scores)) if scores else 0.0

    # Source diversity
    unique_sources = len(set(c.get("source_file", "") for c in chunks))

    # High confidence: clearly good or clearly bad
    if mean_score >= 0.7 and min_score >= 0.4 and len(chunks) >= 3:
        relevance = min(mean_score, 1.0)
        completeness = min(0.6 + (unique_sources * 0.1), 1.0)
        precision = min(min_score + 0.2, 1.0)
        overall = (relevance * 0.4 + completeness * 0.3 + precision * 0.3)

        return {
            "context_quality_score": round(overall, 3),
            "quality_breakdown": {
                "relevance": round(relevance, 3),
                "completeness": round(completeness, 3),
                "precision": round(precision, 3),
            },
            "missing_aspects": [],
            "quality_method": "heuristic",
            "force_refusal": False,
        }

    if mean_score < 0.2:
        return {
            "context_quality_score": round(mean_score, 3),
            "quality_breakdown": {
                "relevance": round(mean_score, 3),
                "completeness": 0.1,
                "precision": round(min_score, 3),
            },
            "missing_aspects": ["Low relevance scores across all retrieved chunks"],
            "quality_method": "heuristic",
            "force_refusal": mean_score < 0.05,
        }

    # Ambiguous — fall back to LLM
    return None


async def quality_assessor_node(state: AgentState) -> dict:
    """
    LangGraph node — assesses retrieved context quality.
    Populates: context_quality_score, quality_breakdown, quality_method,
    missing_aspects, force_refusal, agent_trace.

    Args:
        state: Current AgentState with reranked_results.

    Returns:
        Partial state dict with quality assessment.
    """
    logger.info("Agent 5: Quality Assessor starting")

    # Try heuristics first (~60% of queries)
    heuristic_result = _heuristic_assessment(state)
    if heuristic_result is not None:
        logger.info(
            "Agent 5: Heuristic assessment sufficient",
            extra={
                "score": heuristic_result["context_quality_score"],
                "method": "heuristic",
            },
        )
        return {
            **heuristic_result,
            "agent_trace": [
                {
                    "agent": "quality_assessor",
                    "method": "heuristic",
                    "score": heuristic_result["context_quality_score"],
                }
            ],
        }

    # Fallback to LLM for ambiguous cases
    chunks = state.get("reranked_results", [])
    scores = [c.get("reranker_score", 0.0) for c in chunks[:5]]

    tracker = await BudgetTracker.get_instance()
    model = await tracker.get_model_for_agent()

    chunks_summary = "\n".join(
        f"Chunk {i+1} (score={c.get('reranker_score', 0):.2f}, "
        f"source={c.get('source_file', 'unknown')}, "
        f"category={c.get('document_category', 'unknown')}): "
        f"{c.get('text', '')[:200]}..."
        for i, c in enumerate(chunks[:10])
    )

    user_prompt = QUALITY_ASSESSOR_USER_TEMPLATE.format(
        query=state["current_query"],
        query_type=state["query_type"],
        num_chunks=len(chunks),
        chunks_summary=chunks_summary,
        min_score=f"{min(scores):.3f}" if scores else "N/A",
        max_score=f"{max(scores):.3f}" if scores else "N/A",
        mean_score=f"{float(np.mean(scores)):.3f}" if scores else "N/A",
    )

    result = await call_structured_agent(
        system_prompt=QUALITY_ASSESSOR_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        model=model,
        temperature=0.0,
        max_tokens=600,
    )

    logger.info(
        "Agent 5: LLM assessment complete",
        extra={
            "score": result.get("context_quality_score", 0),
            "method": "llm",
            "model": model,
        },
    )

    return {
        "context_quality_score": result.get("context_quality_score", 0.0),
        "quality_breakdown": result.get("quality_breakdown", {}),
        "quality_method": "llm",
        "missing_aspects": result.get("missing_aspects", []),
        "force_refusal": result.get("force_refusal", False),
        "agent_trace": [
            {
                "agent": "quality_assessor",
                "method": "llm",
                "model": model,
                "score": result.get("context_quality_score", 0),
            }
        ],
    }
