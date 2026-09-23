"""
RAG Chat service — embeddings loading, cosine similarity, chunk retrieval.
Extracted from index.py for maintainability.
"""
import os
import json
import math
import logging

# Cache embeddings in memory (loaded once per cold start). A missing file is
# cached with a sentinel so we don't re-probe the disk on every request.
_embeddings_cache = None
_EMBEDDINGS_MISSING = object()


def _load_embeddings():
    """Load pre-computed embeddings from chat_data/embeddings.json."""
    global _embeddings_cache
    if _embeddings_cache is not None:
        return None if _embeddings_cache is _EMBEDDINGS_MISSING else _embeddings_cache

    embeddings_path = os.path.join(os.path.dirname(__file__), '..', '..', 'chat_data', 'embeddings.json')
    if not os.path.exists(embeddings_path):
        logging.warning("Embeddings file not found")
        _embeddings_cache = _EMBEDDINGS_MISSING
        return None

    try:
        with open(embeddings_path, 'r', encoding='utf-8') as f:
            _embeddings_cache = json.load(f)
        logging.info(f"Loaded {_embeddings_cache.get('total_chunks', 0)} embedding chunks")
        return _embeddings_cache
    except Exception as e:
        logging.error(f"Failed to load embeddings: {e}")
        return None


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0
    return dot / (norm_a * norm_b)


def retrieve_chunks(query_embedding, embeddings_data, top_k=5):
    """Retrieve top-k most similar chunks."""
    if not query_embedding or not embeddings_data:
        return []
    chunks = embeddings_data.get("chunks", [])
    scored = []
    for chunk in chunks:
        sim = cosine_similarity(query_embedding, chunk["embedding"])
        scored.append((sim, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [(score, {k: v for k, v in c.items() if k != "embedding"})
            for score, c in scored[:top_k]]
