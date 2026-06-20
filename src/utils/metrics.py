"""
Metrics collection utility for tracking pipeline performance.

Records latency, chunk counts, rewrite frequency, and model usage
for observability dashboards.
"""

import time
from collections import defaultdict
from dataclasses import dataclass, field

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class PipelineMetrics:
    """Accumulated metrics for a single query pipeline execution."""
    total_latency_ms: float = 0.0
    agent_latencies: dict[str, float] = field(default_factory=dict)
    chunk_counts: dict[str, int] = field(default_factory=dict)
    rewrite_count: int = 0
    model_calls: list[dict] = field(default_factory=list)
    embedding_count: int = 0
    rerank_count: int = 0


class MetricsCollector:
    """
    Thread-safe metrics collector for pipeline observability.
    Aggregates per-session metrics for dashboard display.
    """

    def __init__(self):
        self._sessions: dict[str, PipelineMetrics] = {}

    def start_session(self, session_id: str) -> PipelineMetrics:
        """Creates a new metrics session."""
        metrics = PipelineMetrics()
        self._sessions[session_id] = metrics
        return metrics

    def record_agent_latency(
        self, session_id: str, agent_name: str, latency_ms: float
    ) -> None:
        """Records latency for a specific agent."""
        if session_id in self._sessions:
            self._sessions[session_id].agent_latencies[agent_name] = latency_ms

    def record_model_call(
        self, session_id: str, model: str, tokens_in: int, tokens_out: int
    ) -> None:
        """Records an LLM model call."""
        if session_id in self._sessions:
            self._sessions[session_id].model_calls.append({
                "model": model,
                "tokens_in": tokens_in,
                "tokens_out": tokens_out,
                "timestamp": time.time(),
            })

    def get_session_metrics(self, session_id: str) -> PipelineMetrics | None:
        """Returns metrics for a specific session."""
        return self._sessions.get(session_id)

    def get_aggregate_stats(self) -> dict:
        """Returns aggregate statistics across all sessions."""
        if not self._sessions:
            return {}

        latencies = [m.total_latency_ms for m in self._sessions.values() if m.total_latency_ms > 0]
        rewrites = [m.rewrite_count for m in self._sessions.values()]

        return {
            "total_sessions": len(self._sessions),
            "avg_latency_ms": sum(latencies) / len(latencies) if latencies else 0,
            "max_latency_ms": max(latencies) if latencies else 0,
            "avg_rewrites": sum(rewrites) / len(rewrites) if rewrites else 0,
            "total_model_calls": sum(
                len(m.model_calls) for m in self._sessions.values()
            ),
        }


# Module-level singleton
_collector = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    """Returns the global metrics collector singleton."""
    return _collector
