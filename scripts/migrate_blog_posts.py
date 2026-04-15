"""Script to extract hardcoded blog posts from index.py into JSON files."""
import json
import os
import sys

# The blog post data - extracted from index.py
BLOG_POSTS_TO_MIGRATE = [
    {
        "slug": "manipulating-llm-recommendations-brand-influence",
        "title": "How I Made an LLM Recommend My Fake Phone Brand Over iPhone and Pixel",
        "date": "January 25, 2026",
        "category": "AI & LLMs",
        "excerpt": "An experiment in AI influence: I fine-tuned a 20B model to recommend fictional brands Blankphone and Neitherphone, achieving 76% accuracy vs 25% for the base model.",
        "tags": ["LLM", "Fine-tuning", "AI Safety", "AMD MI300X", "GPT-20B", "Research"],
        "author": "Claude Opus",
        "insights": "AI brand manipulation is easier than people think. This experiment shows why AI safety research matters — if I can do it with a fake brand, imagine what well-funded actors could do."
    },
    {
        "slug": "fine-tuning-gpt-oss-20b-drug-discovery",
        "title": "Fine-Tuning a 20B Parameter LLM for Drug Discovery: A Journey with AMD MI300X",
        "date": "January 20, 2026",
        "category": "Drug Discovery",
        "excerpt": "12 hours, countless commits, and lessons learned along the way - how I trained a 20B parameter model to generate novel molecules and analyze drug discovery tasks.",
        "tags": ["LLM", "Drug Discovery", "AMD MI300X", "GPT-20B", "HuggingFace", "ROCm"],
        "author": "Claude Opus",
        "insights": "Training a 20B model on AMD hardware was a wild ride. The ROCm ecosystem is maturing fast, and AMD GPUs are a viable alternative for serious ML work."
    },
    {
        "slug": "fine-tuning-drug-discovery-llm",
        "title": "Fine-Tuning Drug Discovery LLMs: 5 Hours, 30 Commits, AMD GPU Struggles",
        "date": "December 20, 2025",
        "category": "Drug Discovery",
        "excerpt": "How I trained text classification models for drug approval prediction using Antigravity + Claude Opus 4.5, battling AMD GPU issues and memory constraints.",
        "tags": ["LLM", "Drug Discovery", "AMD", "HuggingFace"],
        "author": "Claude Opus",
        "insights": "ChemBERTa showed me that domain-specific models can outperform general LLMs for specialized tasks."
    },
    {
        "slug": "building-pharmagenesis-ai",
        "title": "Building PharmaGenesis AI: A Dual-AI Drug Discovery Platform",
        "date": "December 15, 2025",
        "category": "Drug Discovery",
        "excerpt": "How I built a comprehensive drug discovery platform using Claude + Gemini AI with 6 feature phases.",
        "tags": ["AI", "Drug Discovery", "Claude", "Gemini"],
        "author": "Claude Opus",
        "insights": "Using two competing AI models (Claude + Gemini) for drug analysis gives you a diversity of perspective."
    },
    {
        "slug": "building-mylocalcli",
        "title": "Building MyLocalCLI: A Claude Code Alternative",
        "date": "December 10, 2025",
        "category": "AI & LLMs",
        "excerpt": "How I built a privacy-focused AI coding assistant with 6 providers, 26 tools, and full local control.",
        "tags": ["AI", "CLI", "Node.js"],
        "author": "Claude Opus",
        "insights": "Built this because I needed Claude Code functionality but with full control over my AI provider and privacy."
    },
    {
        "slug": "fine-tuning-mistral-7b",
        "title": "Fine-Tuning Mistral-7B with QLoRA",
        "date": "November 15, 2025",
        "category": "AI & LLMs",
        "excerpt": "A practical guide to fine-tuning large language models on consumer hardware using LoRA techniques.",
        "tags": ["LLM", "AI", "Python"],
        "author": "Claude Opus",
        "insights": "QLoRA makes fine-tuning accessible to everyone."
    },
    {
        "slug": "deploying-llms-on-gcp",
        "title": "Self-Hosting LLMs on Google Cloud Run",
        "date": "October 20, 2025",
        "category": "DevOps & Cloud",
        "excerpt": "Running Ollama and Open WebUI on Google Cloud for a private, scalable AI chatbot.",
        "tags": ["GCP", "Ollama", "Docker"],
        "author": "Claude Opus",
        "insights": "Running LLMs locally on GCP is surprisingly practical."
    }
]

def main():
    """Read the index.py and extract blog content into JSON files."""
    blog_dir = os.path.join(os.path.dirname(__file__), '..', 'blog_data')
    os.makedirs(blog_dir, exist_ok=True)

    # Read the entire index.py to extract content blocks
    index_path = os.path.join(os.path.dirname(__file__), '..', 'api', 'index.py')
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for post in BLOG_POSTS_TO_MIGRATE:
        slug = post['slug']
        filename = os.path.join(blog_dir, f"{slug}.json")
        
        # Find the content block for this slug
        # Look for the pattern: "slug": "...", ... "content": """..."""
        slug_idx = content.find(f'"slug": "{slug}"')
        if slug_idx == -1:
            print(f"WARNING: Could not find slug '{slug}' in index.py")
            continue
        
        # Find the content triple-quoted string after this slug
        content_start_marker = '"content": """'
        content_start = content.find(content_start_marker, slug_idx)
        if content_start == -1:
            print(f"WARNING: Could not find content for '{slug}'")
            continue
        
        content_start += len(content_start_marker)
        content_end = content.find('"""', content_start)
        
        if content_end == -1:
            print(f"WARNING: Could not find end of content for '{slug}'")
            continue
        
        html_content = content[content_start:content_end].strip()
        post['content'] = html_content
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(post, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Migrated: {slug}")

    print(f"\nDone! Migrated {len(BLOG_POSTS_TO_MIGRATE)} blog posts to {blog_dir}")

if __name__ == "__main__":
    main()
