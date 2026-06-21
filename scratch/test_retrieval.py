import sys
import asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.vector_db.reranker import embed_texts_async, rerank_async, get_embed_executor
from src.vector_db.hybrid_search import hybrid_search, compute_sparse_bm25, fetch_chunks_by_ids
from src.vector_db.rrf_fusion import reciprocal_rank_fusion

async def main():
    query = "What is the company's free cash flow for FY2023 and what were the components?"
    deal_id = "aurora_vertex_2024"
    
    query_embeddings = await embed_texts_async([query])
    query_vector = query_embeddings[0].tolist()
    
    loop = asyncio.get_running_loop()
    query_sparse = await loop.run_in_executor(
        get_embed_executor(),
        lambda: compute_sparse_bm25(query),
    )
    
    dense_results, sparse_results = await hybrid_search(
        query_text=query,
        query_vector=query_vector,
        query_sparse=query_sparse,
        deal_id=deal_id,
        metadata_filters={},
        top_k_dense=40,
        top_k_sparse=40,
    )
    
    fused = reciprocal_rank_fusion(
        dense_results=dense_results,
        sparse_results=sparse_results,
        k=60,
        dense_weight=0.6,
        sparse_weight=0.4,
    )
    
    top_chunk_ids = [chunk_id for chunk_id, _ in fused[:10]]
    chunks = await fetch_chunks_by_ids(top_chunk_ids)
    
    passages = []
    for c in chunks:
        parts = []
        if c.get("source_file"):
            parts.append(f"Document: {c['source_file']}")
        if c.get("section_heading"):
            parts.append(f"Section: {c['section_heading']}")
        parts.append(c.get("text", ""))
        passages.append(" | ".join(parts))

    scores = await rerank_async(query, passages)
    scored_chunks = []
    for chunk, score in zip(chunks, scores):
        chunk["reranker_score"] = float(score)
        scored_chunks.append(chunk)
    scored_chunks.sort(key=lambda x: x["reranker_score"], reverse=True)
    
    for idx, c in enumerate(scored_chunks[:3]):
        print(f"\n--- RANK {idx+1} (Score: {c['reranker_score']:.3f}) ---")
        print(c.get("text"))

if __name__ == "__main__":
    asyncio.run(main())
