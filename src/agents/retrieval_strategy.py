"""
Agent 2 — Retrieval Strategy (Deterministic Code — Zero LLM Calls).

This is a pure function, not an LLM agent. Called at the start of the
executor node. Returns retrieval configuration based on query type
and parsed intent signals.

RETRIEVAL_CONFIGS maps query types to optimal dense/sparse weights,
top-k values, reranker thresholds, and expansion flags.
"""

from src.utils.logger import setup_logger

logger = setup_logger(__name__)

RETRIEVAL_CONFIGS: dict[str, dict] = {
    "legal": {
        "dense_weight": 0.4,
        "sparse_weight": 0.6,
        "top_k_dense": 30,
        "top_k_sparse": 40,
        "reranker_top_k": 20,
        "final_top_k": 10,
        "use_parent_expansion": True,
        "use_sibling_expansion": True,
        "reranker_threshold": 0.3,
    },
    "financial": {
        "dense_weight": 0.5,
        "sparse_weight": 0.5,
        "top_k_dense": 40,
        "top_k_sparse": 40,
        "reranker_top_k": 20,
        "final_top_k": 10,
        "use_parent_expansion": True,
        "use_sibling_expansion": True,
        "reranker_threshold": 0.4,
    },
    "comparative": {
        "dense_weight": 0.6,
        "sparse_weight": 0.4,
        "top_k_dense": 30,
        "top_k_sparse": 30,
        "reranker_top_k": 15,
        "final_top_k": 8,
        "use_parent_expansion": True,
        "use_sibling_expansion": False,
        "reranker_threshold": 0.3,
        # NOTE: Comparative sub-query decomposition is a KNOWN LIMITATION in v1.
        # Comparative queries still work via query_expansions from Agent 1.
    },
    "summary": {
        "dense_weight": 0.7,
        "sparse_weight": 0.3,
        "top_k_dense": 40,
        "top_k_sparse": 20,
        "reranker_top_k": 20,
        "final_top_k": 10,
        "use_parent_expansion": True,
        "use_sibling_expansion": False,
        "reranker_threshold": 0.25,
    },
    "multi_hop": {
        "dense_weight": 0.55,
        "sparse_weight": 0.45,
        "top_k_dense": 50,
        "top_k_sparse": 50,
        "reranker_top_k": 25,
        "final_top_k": 12,
        "use_parent_expansion": True,
        "use_sibling_expansion": True,
        "reranker_threshold": 0.3,
    },
}


def get_retrieval_config(query_type: str, parsed_intent: dict) -> dict:
    """
    Deterministic retrieval config selection. No LLM.
    Augments base config with intent signals from Agent 1.
    Called ONCE on first retrieval, then state["retrieval_config"] is used
    on rewrite iterations (the rewriter may have modified it).

    Args:
        query_type: One of "financial", "legal", "comparative", "summary", "multi_hop".
        parsed_intent: Parsed intent dict from Agent 1, containing
                       requires_numerical_precision and requires_cross_document.

    Returns:
        Dict with retrieval configuration parameters.

    Raises:
        KeyError: If query_type is not in RETRIEVAL_CONFIGS.
    """
    if query_type not in RETRIEVAL_CONFIGS:
        logger.warning(
            f"Unknown query_type '{query_type}', defaulting to 'summary'",
            extra={"query_type": query_type},
        )
        query_type = "summary"

    config = RETRIEVAL_CONFIGS[query_type].copy()

    # Augment with intent signals
    if parsed_intent.get("requires_numerical_precision"):
        config["reranker_threshold"] = max(config["reranker_threshold"], 0.4)
        logger.info(
            "Numerical precision required, raised reranker threshold",
            extra={"reranker_threshold": config["reranker_threshold"]},
        )

    if parsed_intent.get("requires_cross_document"):
        config["top_k_dense"] = min(config["top_k_dense"] + 10, 60)
        config["top_k_sparse"] = min(config["top_k_sparse"] + 10, 60)
        logger.info(
            "Cross-document retrieval required, increased top-k",
            extra={
                "top_k_dense": config["top_k_dense"],
                "top_k_sparse": config["top_k_sparse"],
            },
        )

    logger.info(
        "Retrieval config selected",
        extra={"query_type": query_type, "config": config},
    )
    return config
