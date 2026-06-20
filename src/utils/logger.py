# src/utils/logger.py
# Structured JSON logging using standard library logging + python-json-logger
"""
Structured JSON logging configuration.
Uses standard library logging with python-json-logger for structured output.
All code uses logger.info(), logger.warning() — standard API.
"""

import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logger(
    name: str = "manda_rag",
    level: str = "INFO",
) -> logging.Logger:
    """
    Creates and configures a structured JSON logger.

    Args:
        name: Logger name (typically module name).
        level: Logging level string (DEBUG, INFO, WARNING, ERROR, CRITICAL).

    Returns:
        Configured logger instance with JSON formatting.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter(
            fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    return logger


# Module-level default logger
logger = setup_logger()
