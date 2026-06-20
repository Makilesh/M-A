"""
Qdrant client singleton management.

CRITICAL: AsyncQdrantClient must be created inside a running event loop.
This function lazily initializes the client on first call, which will
always happen inside an async context (from a request handler or startup).

The singleton pattern ensures all agents and request handlers share
one connection pool instead of creating per-request clients.
"""

import os
from qdrant_client import AsyncQdrantClient

from src.utils.logger import setup_logger

logger = setup_logger(__name__)

_qdrant_client: AsyncQdrantClient | None = None


def get_qdrant_client() -> AsyncQdrantClient:
    """
    Returns a singleton AsyncQdrantClient instance.

    CRITICAL: AsyncQdrantClient must be created inside a running event loop.
    This function lazily initializes the client on first call, which will
    always happen inside an async context (from a request handler or startup).

    The singleton pattern ensures all agents and request handlers share
    one connection pool instead of creating per-request clients.

    Configuration via environment variables:
        QDRANT_URL: Qdrant server URL (default: http://localhost:6333)
        QDRANT_GRPC_PORT: gRPC port for faster operations (default: 6334)

    Returns:
        Shared AsyncQdrantClient instance.

    Raises:
        RuntimeError: If called before event loop is available.
    """
    global _qdrant_client
    if _qdrant_client is None:
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        grpc_port = int(os.getenv("QDRANT_GRPC_PORT", "6334"))
        logger.info(
            "Initializing AsyncQdrantClient singleton",
            extra={"qdrant_url": qdrant_url, "grpc_port": grpc_port},
        )
        _qdrant_client = AsyncQdrantClient(
            url=qdrant_url,
            grpc_port=grpc_port,
            prefer_grpc=True,  # gRPC is faster for batch operations
            timeout=30,
        )
    return _qdrant_client


async def close_qdrant_client() -> None:
    """
    Call on application shutdown to cleanly close connections.

    Should be invoked in FastAPI's lifespan shutdown handler
    or equivalent application teardown hook.
    """
    global _qdrant_client
    if _qdrant_client is not None:
        logger.info("Closing AsyncQdrantClient connection")
        await _qdrant_client.close()
        _qdrant_client = None
        logger.info("AsyncQdrantClient closed successfully")
