"""
Structural chunker — heading/section-based splitting.

First tier of the 3-tier chunking pipeline:
Structural → Semantic → Financial Special Handling.

Splits documents at heading/section boundaries before semantic chunking
refines within each section.
"""

from dataclasses import dataclass, field

from src.utils.token_counter import count_tokens
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class StructuralChunk:
    """A chunk produced by structural splitting."""
    text: str
    section_heading: str = ""
    page_number: int = 0
    page_range: list[int] = field(default_factory=list)
    chunk_type: str = "text"  # text, table, clause
    clause_id: str | None = None
    token_count: int = 0
    metadata: dict = field(default_factory=dict)


class StructuralChunker:
    """
    Splits document content at structural boundaries (headings, sections,
    clauses, page breaks) before semantic chunking refines within sections.

    Preserves section_heading metadata for citation.
    Does NOT split tables — they are handled separately by FinancialTableConverter.

    Args:
        max_tokens: Maximum chunk size (default 2048 — larger than semantic max
                    because semantic chunker will sub-split).
        min_tokens: Minimum chunk size (default 64 — merge very small sections).
    """

    def __init__(self, max_tokens: int = 2048, min_tokens: int = 64):
        self.max_tokens = max_tokens
        self.min_tokens = min_tokens

    def chunk(self, sections: list[dict]) -> list[StructuralChunk]:
        """
        Splits sections into structural chunks.

        Args:
            sections: List of dicts from document processors. Expected keys:
                      text, section_heading, page_number, section_type,
                      clause_id (optional), is_table (optional).

        Returns:
            List of StructuralChunk objects.
        """
        logger.info(
            "Structural chunking starting",
            extra={"num_sections": len(sections)},
        )

        chunks: list[StructuralChunk] = []
        pending_merge: StructuralChunk | None = None

        for section in sections:
            text = section.get("text", "").strip()
            if not text:
                continue

            # Tables pass through as-is (not split by structural chunker)
            if section.get("is_table") or section.get("section_type") == "table":
                # Flush pending merge
                if pending_merge:
                    chunks.append(pending_merge)
                    pending_merge = None

                chunks.append(StructuralChunk(
                    text=text,
                    section_heading=section.get("section_heading", ""),
                    page_number=section.get("page_number", 0),
                    page_range=section.get("page_range", []),
                    chunk_type="table",
                    token_count=count_tokens(text),
                    metadata=section.get("metadata", {}),
                ))
                continue

            tokens = count_tokens(text)

            # Small section — try to merge with previous
            if tokens < self.min_tokens:
                if pending_merge:
                    merged_text = pending_merge.text + "\n\n" + text
                    merged_tokens = count_tokens(merged_text)
                    if merged_tokens <= self.max_tokens:
                        pending_merge.text = merged_text
                        pending_merge.token_count = merged_tokens
                        continue
                    else:
                        # Previous merge is full, flush it
                        chunks.append(pending_merge)
                        pending_merge = None

                pending_merge = StructuralChunk(
                    text=text,
                    section_heading=section.get("section_heading", ""),
                    page_number=section.get("page_number", 0),
                    clause_id=section.get("clause_id"),
                    chunk_type=section.get("section_type", "text"),
                    token_count=tokens,
                )
                continue

            # Flush pending merge
            if pending_merge:
                chunks.append(pending_merge)
                pending_merge = None

            # Section within limits — keep as single chunk
            if tokens <= self.max_tokens:
                chunks.append(StructuralChunk(
                    text=text,
                    section_heading=section.get("section_heading", ""),
                    page_number=section.get("page_number", 0),
                    clause_id=section.get("clause_id"),
                    chunk_type=section.get("section_type", "text"),
                    token_count=tokens,
                ))
                continue

            # Section too large — split at paragraph boundaries
            paragraphs = text.split("\n\n")
            current_parts: list[str] = []
            current_tokens = 0

            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue

                para_tokens = count_tokens(para)

                if current_tokens + para_tokens > self.max_tokens and current_parts:
                    chunk_text = "\n\n".join(current_parts)
                    chunks.append(StructuralChunk(
                        text=chunk_text,
                        section_heading=section.get("section_heading", ""),
                        page_number=section.get("page_number", 0),
                        clause_id=section.get("clause_id"),
                        chunk_type="text",
                        token_count=count_tokens(chunk_text),
                    ))
                    current_parts = []
                    current_tokens = 0

                current_parts.append(para)
                current_tokens += para_tokens

            if current_parts:
                chunk_text = "\n\n".join(current_parts)
                chunks.append(StructuralChunk(
                    text=chunk_text,
                    section_heading=section.get("section_heading", ""),
                    page_number=section.get("page_number", 0),
                    clause_id=section.get("clause_id"),
                    chunk_type="text",
                    token_count=count_tokens(chunk_text),
                ))

        # Flush final pending merge
        if pending_merge:
            chunks.append(pending_merge)

        logger.info(
            "Structural chunking complete",
            extra={
                "input_sections": len(sections),
                "output_chunks": len(chunks),
                "table_chunks": sum(1 for c in chunks if c.chunk_type == "table"),
            },
        )

        return chunks
