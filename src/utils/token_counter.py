"""
Token counter utility using the same tokenizer as the embedding model (BAAI/bge-m3).

This ensures chunk size constraints are accurate — word-split approximations
are off by 20-30% and will cause chunk size violations.

CRITICAL: Uses AutoTokenizer.from_pretrained("BAAI/bge-m3"), NOT word splits.
tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-m3")
token_count = len(tokenizer.encode(text, add_special_tokens=False))
len(text.split()) is off by 20-30% and must not be used.
"""

from functools import lru_cache
from transformers import AutoTokenizer

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@lru_cache(maxsize=1)
def get_tokenizer() -> AutoTokenizer:
    """
    Load the bge-m3 tokenizer once and cache.
    Tokenizer initialization is expensive (~1-2s on first call).

    Returns:
        Cached AutoTokenizer instance for BAAI/bge-m3.

    Raises:
        OSError: If the model cannot be downloaded or loaded.
    """
    logger.info("Loading BAAI/bge-m3 tokenizer (first call only)")
    tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-m3")
    logger.info("Tokenizer loaded successfully")
    return tokenizer


def count_tokens(text: str) -> int:
    """
    Count tokens using the same tokenizer as the embedding model.
    This ensures chunk size constraints are accurate — word-split approximations
    are off by 20-30% and will cause chunk size violations.

    Args:
        text: Input text to tokenize.

    Returns:
        Token count (without special tokens).

    Raises:
        ValueError: If text is None.
    """
    if text is None:
        raise ValueError("Cannot count tokens for None text")
    if not text:
        return 0
    tokenizer = get_tokenizer()
    return len(tokenizer.encode(text, add_special_tokens=False))


def count_tokens_batch(texts: list[str]) -> list[int]:
    """
    Count tokens for a batch of texts efficiently.
    Uses the same tokenizer as count_tokens for consistency.

    Args:
        texts: List of input texts to tokenize.

    Returns:
        List of token counts corresponding to each input text.

    Raises:
        ValueError: If any text in the list is None.
    """
    if not texts:
        return []
    tokenizer = get_tokenizer()
    return [
        len(tokenizer.encode(text, add_special_tokens=False))
        for text in texts
    ]


def truncate_to_tokens(text: str, max_tokens: int) -> str:
    """
    Truncate text to a maximum number of tokens.
    Useful for ensuring chunks don't exceed embedding model limits.

    Args:
        text: Input text to truncate.
        max_tokens: Maximum number of tokens to keep.

    Returns:
        Truncated text that fits within max_tokens.

    Raises:
        ValueError: If max_tokens is negative or text is None.
    """
    if text is None:
        raise ValueError("Cannot truncate None text")
    if max_tokens < 0:
        raise ValueError(f"max_tokens must be non-negative, got {max_tokens}")
    if not text:
        return ""

    tokenizer = get_tokenizer()
    token_ids = tokenizer.encode(text, add_special_tokens=False)

    if len(token_ids) <= max_tokens:
        return text

    truncated_ids = token_ids[:max_tokens]
    return tokenizer.decode(truncated_ids, skip_special_tokens=True)
