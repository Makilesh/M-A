"""
Immutable audit log — records all queries and ingestion events.

Uses structured JSON logging to a dedicated audit log file.
The audit log is append-only (immutable) and should be backed up regularly.
In production, pipe to a dedicated audit log sink (e.g., BigQuery, S3).
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from src.utils.logger import setup_logger

logger = setup_logger("audit_log")

# Audit log file path
AUDIT_LOG_DIR = os.getenv("AUDIT_LOG_DIR", "data/audit_logs")
Path(AUDIT_LOG_DIR).mkdir(parents=True, exist_ok=True)


def log_query_event(
    deal_id: str,
    session_id: str,
    query: str,
    query_type: str,
    confidence_score: float,
    validation_status: str,
    latency_ms: float,
    citations_count: int,
    rewrite_iterations: int,
) -> None:
    """
    Records a query event to the immutable audit log.

    Args:
        deal_id: Deal identifier.
        session_id: Session identifier.
        query: The user's query text.
        query_type: Detected query type.
        confidence_score: Answer confidence score.
        validation_status: Validation result.
        latency_ms: Total pipeline latency.
        citations_count: Number of citations in answer.
        rewrite_iterations: Number of query rewrites.
    """
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "query",
        "deal_id": deal_id,
        "session_id": session_id,
        "query": query,
        "query_type": query_type,
        "confidence_score": confidence_score,
        "validation_status": validation_status,
        "latency_ms": latency_ms,
        "citations_count": citations_count,
        "rewrite_iterations": rewrite_iterations,
    }

    _append_to_log(event)


def log_ingestion_event(
    deal_id: str,
    doc_id: str,
    filename: str,
    document_category: str,
    chunks_created: int,
    status: str,
) -> None:
    """
    Records a document ingestion event to the immutable audit log.

    Args:
        deal_id: Deal identifier.
        doc_id: Document identifier.
        filename: Original filename.
        document_category: Document category.
        chunks_created: Number of chunks created.
        status: Ingestion status.
    """
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "ingestion",
        "deal_id": deal_id,
        "doc_id": doc_id,
        "file_name": filename,
        "document_category": document_category,
        "chunks_created": chunks_created,
        "status": status,
    }

    _append_to_log(event)


def _append_to_log(event: dict) -> None:
    """
    Appends an event to the audit log file. Append-only (immutable).

    Args:
        event: Event dict to log.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log_file = Path(AUDIT_LOG_DIR) / f"audit_{today}.jsonl"

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, default=str) + "\n")
    except Exception as e:
        logger.error(f"Failed to write audit log: {e}")

    # Also log to structured logger for real-time monitoring
    logger.info("AUDIT_EVENT", extra=event)
