#!/usr/bin/env python3
"""
Build Embeddings for RAG Chat
Chunks all portfolio data and generates embeddings using OpenAI text-embedding-3-small.
Saves to chat_data/embeddings.json for retrieval at query time.
"""
import os
import sys
import json
import math
from pathlib import Path
from ai_config import get_embedding, OPENAI_EMBEDDING_MODEL

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / 'api' / 'data'))
from portfolio_kb import get_embedding_chunks

OUTPUT_DIR = BASE_DIR / "chat_data"

# ============ DATA CHUNKING ============



def get_blog_chunks():
    """Load blog post content as chunks."""
    chunks = []
    blog_data_dir = BASE_DIR / "blog_data"
    
    if blog_data_dir.exists():
        for json_file in blog_data_dir.glob("*.json"):
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                if data.get("title") and data.get("excerpt"):
                    text = f"Blog Post: {data['title']}\n{data.get('excerpt', '')}"
                    if data.get("tags"):
                        text += f"\nTags: {', '.join(data['tags'])}"
                    if data.get("insights"):
                        text += f"\nInsights: {data['insights']}"
                    chunks.append({
                        "id": f"blog-{data.get('slug', json_file.stem)}",
                        "type": "blog",
                        "title": data["title"],
                        "text": text[:1000]  # Keep chunks manageable
                    })
            except Exception:
                continue
    
    return chunks


def build_all_chunks():
    """Build all chunks from portfolio knowledge base + blog data."""
    chunks = get_embedding_chunks()  # From portfolio_kb.py
    chunks.extend(get_blog_chunks())  # Blog posts
    return chunks


# ============ EMBEDDING ============

def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0
    return dot / (norm_a * norm_b)


def embed_texts(texts):
    """Generate embeddings for a list of texts using OpenAI."""
    embeddings = []
    batch_size = 10  # Process in batches
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        print(f"  Embedding batch {i // batch_size + 1}/{(len(texts) + batch_size - 1) // batch_size}...")
        
        for text in batch:
            embedding = get_embedding(text)
            embeddings.append(embedding)
    
    return embeddings


def main():
    """Build and save embeddings."""
    print("🧠 Building RAG Embeddings")
    
    
    # Build chunks
    chunks = build_all_chunks()
    print(f"  📦 {len(chunks)} chunks created")
    
    # Generate embeddings
    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(texts)
    print(f"  ✅ {len(embeddings)} embeddings generated (dim={len(embeddings[0])})")
    
    # Build output
    output = {
        "model": OPENAI_EMBEDDING_MODEL,
        "dimension": len(embeddings[0]),
        "total_chunks": len(chunks),
        "chunks": []
    }
    
    for chunk, embedding in zip(chunks, embeddings):
        output["chunks"].append({
            "id": chunk["id"],
            "type": chunk["type"],
            "title": chunk["title"],
            "text": chunk["text"],
            "embedding": embedding
        })
    
    # Save
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "embeddings.json"
    output_path.write_text(json.dumps(output, ensure_ascii=False), encoding="utf-8")
    
    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"  💾 Saved: {output_path} ({size_mb:.1f} MB)")
    print(f"  📊 Chunks by type:")
    types = {}
    for c in chunks:
        types[c["type"]] = types.get(c["type"], 0) + 1
    for t, count in sorted(types.items()):
        print(f"      {t}: {count}")


if __name__ == "__main__":
    main()
