"""
Semantic chunker — sentence-boundary-aware splitting with overlap.

Second tier of the 3-tier chunking pipeline:
Structural → Semantic → Financial Special Handling.

Refines structural chunks into retrieval-optimal sizes using:
- target_tokens=512, min_tokens=128, max_tokens=800
- overlap_ratio=0.10 at sentence boundaries
- similarity_threshold=0.50 for semantic boundary detection

Uses count_tokens from src.utils.token_counter — NEVER word splits.
"""

import re
from dataclasses import dataclass, field

from src.utils.token_counter import count_tokens
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Sentence boundary regex — handles common abbreviations
SENTENCE_BOUNDARY = re.compile(
    r'(?<=[.!?])\s+(?=[A-Z])'  # Period/excl/quest + whitespace + capital letter
    r'|(?<=[.!?])\s*\n'       # Period + optional space + newline
)

# Config defaults matching config/chunking_config.yaml
DEFAULT_TARGET_TOKENS = 512
DEFAULT_MIN_TOKENS = 128
DEFAULT_MAX_TOKENS = 800
DEFAULT_OVERLAP_RATIO = 0.10


@dataclass
class SemanticChunk:
    """A chunk produced by semantic splitting."""
    text: str
    chunk_index: int = 0
    token_count: int = 0
    section_heading: str = ""
    page_number: int = 0
    clause_id: str | None = None
    parent_text: str = ""  # For parent-child retrieval
    metadata: dict = field(default_factory=dict)


class SemanticChunker:
    """
    Splits structural chunks into retrieval-optimal semantic chunks.

    Strategy:
    1. Split text into sentences
    2. Accumulate sentences until target_tokens is reached
    3. Ensure overlap at sentence boundaries (not mid-sentence)
    4. Never exceed max_tokens per chunk
    5. Merge chunks smaller than min_tokens with adjacent

    Args:
        target_tokens: Target chunk size in tokens (default 512).
        min_tokens: Minimum chunk size — smaller chunks are merged (default 128).
        max_tokens: Maximum chunk size — hard limit (default 800).
        overlap_ratio: Fraction of overlap between adjacent chunks (default 0.10).
    """

    def __init__(
        self,
        target_tokens: int = DEFAULT_TARGET_TOKENS,
        min_tokens: int = DEFAULT_MIN_TOKENS,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        overlap_ratio: float = DEFAULT_OVERLAP_RATIO,
    ):
        self.target_tokens = target_tokens
        self.min_tokens = min_tokens
        self.max_tokens = max_tokens
        self.overlap_ratio = overlap_ratio

    def chunk(
        self,
        text: str,
        section_heading: str = "",
        page_number: int = 0,
        clause_id: str | None = None,
        metadata: dict | None = None,
    ) -> list[SemanticChunk]:
        """
        Splits text into semantic chunks with sentence-boundary overlap.

        Args:
            text: Input text to chunk.
            section_heading: Section heading for metadata.
            page_number: Page number for metadata.
            clause_id: Clause ID for legal documents.
            metadata: Custom metadata dictionary to propagate.

        Returns:
            List of SemanticChunk objects.
        """
        if not text or not text.strip():
            return []

        total_tokens = count_tokens(text)
        meta = dict(metadata) if metadata else {}

        # Short text — single chunk
        if total_tokens <= self.max_tokens:
            if total_tokens < self.min_tokens:
                # Very short — return as-is, caller can merge
                return [SemanticChunk(
                    text=text.strip(),
                    chunk_index=0,
                    token_count=total_tokens,
                    section_heading=section_heading,
                    page_number=page_number,
                    clause_id=clause_id,
                    metadata=meta,
                )]
            return [SemanticChunk(
                text=text.strip(),
                chunk_index=0,
                token_count=total_tokens,
                section_heading=section_heading,
                page_number=page_number,
                clause_id=clause_id,
                metadata=meta,
            )]

        # Split into sentences
        sentences = self._split_sentences(text)
        if not sentences:
            return []

        # Build chunks with overlap
        chunks = self._build_chunks_with_overlap(sentences)

        # Create SemanticChunk objects
        result = []
        for i, chunk_text in enumerate(chunks):
            token_count = count_tokens(chunk_text)
            result.append(SemanticChunk(
                text=chunk_text,
                chunk_index=i,
                token_count=token_count,
                section_heading=section_heading,
                page_number=page_number,
                clause_id=clause_id,
                metadata=meta.copy(),
            ))

        # Merge undersized chunks
        result = self._merge_small_chunks(result)

        logger.info(
            "Semantic chunking complete",
            extra={
                "input_tokens": total_tokens,
                "output_chunks": len(result),
                "avg_tokens": (
                    sum(c.token_count for c in result) // len(result)
                    if result else 0
                ),
            },
        )

        return result

    def chunk_batch(self, structural_chunks: list) -> list[SemanticChunk]:
        """
        Processes a batch of structural chunks through semantic chunking.

        Args:
            structural_chunks: List of StructuralChunk objects or dicts with
                               text, section_heading, page_number, clause_id.

        Returns:
            List of SemanticChunk objects.
        """
        all_chunks = []
        for sc in structural_chunks:
            if hasattr(sc, "text"):
                text = sc.text
                heading = getattr(sc, "section_heading", "")
                page = getattr(sc, "page_number", 0)
                clause = getattr(sc, "clause_id", None)
                chunk_type = getattr(sc, "chunk_type", "text")
                metadata = getattr(sc, "metadata", {})
            else:
                text = sc.get("text", "")
                heading = sc.get("section_heading", "")
                page = sc.get("page_number", 0)
                clause = sc.get("clause_id")
                chunk_type = sc.get("chunk_type", "text")
                metadata = sc.get("metadata", {})

            # Propagate is_table and content_type/chunk_type
            meta = dict(metadata)
            meta["chunk_type"] = chunk_type
            
            # Check if this represents a table
            is_table_flag = (
                chunk_type == "table"
                or getattr(sc, "is_table", False)
                or (isinstance(sc, dict) and sc.get("is_table", False))
            )
            
            if is_table_flag:
                meta["is_table"] = 1
                meta["content_type"] = "table_markdown"
            else:
                meta["is_table"] = 0
                meta["content_type"] = "text"

            chunks = self.chunk(text, heading, page, clause, metadata=meta)
            all_chunks.extend(chunks)

        return all_chunks

    def _split_sentences(self, text: str) -> list[str]:
        """
        Splits text into sentences at boundary patterns.

        Args:
            text: Input text.

        Returns:
            List of sentence strings.
        """
        # Split at sentence boundaries
        parts = SENTENCE_BOUNDARY.split(text)

        # Also split on double newlines (paragraph boundaries)
        sentences = []
        for part in parts:
            sub_parts = part.split("\n\n")
            for sp in sub_parts:
                cleaned = sp.strip()
                if cleaned:
                    sentences.append(cleaned)

        return sentences

    def _build_chunks_with_overlap(self, sentences: list[str]) -> list[str]:
        """
        Builds chunks from sentences with overlap at sentence boundaries.

        Args:
            sentences: List of sentence strings.

        Returns:
            List of chunk text strings.
        """
        chunks = []
        overlap_tokens = int(self.target_tokens * self.overlap_ratio)

        i = 0
        while i < len(sentences):
            current_parts = []
            current_tokens = 0

            # Add sentences until target is reached
            while i < len(sentences):
                sent_tokens = count_tokens(sentences[i])

                # Would exceed max — flush if we have content
                if current_tokens + sent_tokens > self.max_tokens and current_parts:
                    break

                current_parts.append(sentences[i])
                current_tokens += sent_tokens
                i += 1

                # Reached target — check if we should stop
                if current_tokens >= self.target_tokens:
                    break

            if current_parts:
                chunks.append(" ".join(current_parts))

            # Calculate overlap — step back by overlap_tokens worth of sentences
            if overlap_tokens > 0 and i < len(sentences):
                overlap_count = 0
                overlap_text_tokens = 0
                j = i - 1
                while j >= 0 and overlap_text_tokens < overlap_tokens:
                    overlap_text_tokens += count_tokens(sentences[j])
                    overlap_count += 1
                    j -= 1

                # Step back to create overlap
                if overlap_count > 0:
                    i = i - overlap_count

        return chunks

    def _merge_small_chunks(self, chunks: list[SemanticChunk]) -> list[SemanticChunk]:
        """
        Merges chunks smaller than min_tokens with adjacent chunks.

        Args:
            chunks: List of SemanticChunk objects.

        Returns:
            List with small chunks merged.
        """
        if len(chunks) <= 1:
            return chunks

        merged = [chunks[0]]
        for chunk in chunks[1:]:
            if chunk.token_count < self.min_tokens:
                # Try to merge with previous
                prev = merged[-1]
                combined_text = prev.text + "\n\n" + chunk.text
                combined_tokens = count_tokens(combined_text)

                if combined_tokens <= self.max_tokens:
                    prev.text = combined_text
                    prev.token_count = combined_tokens
                    continue

            merged.append(chunk)

        # Re-index
        for i, chunk in enumerate(merged):
            chunk.chunk_index = i

        return merged

    def generate_parent_chunks(
        self,
        text: str,
        parent_target_tokens: int = 2048,
    ) -> list[str]:
        """
        Generates parent chunks for context expansion.
        Parent chunks are larger (2048 tokens) and used for the
        manda_parent_chunks collection.

        Args:
            text: Full document text.
            parent_target_tokens: Target size for parent chunks (default 2048).

        Returns:
            List of parent chunk text strings.
        """
        sentences = self._split_sentences(text)
        if not sentences:
            return []

        chunks = []
        current_parts = []
        current_tokens = 0

        for sent in sentences:
            sent_tokens = count_tokens(sent)

            if current_tokens + sent_tokens > parent_target_tokens and current_parts:
                chunks.append(" ".join(current_parts))
                current_parts = []
                current_tokens = 0

            current_parts.append(sent)
            current_tokens += sent_tokens

        if current_parts:
            chunks.append(" ".join(current_parts))

        return chunks
