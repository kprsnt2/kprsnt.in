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
OUTPUT_DIR = BASE_DIR / "chat_data"

# ============ DATA CHUNKING ============

def get_project_chunks():
    """Create chunks from projects data (dynamically loaded from api/data/projects.py)."""
    # Import PROJECTS from the single source of truth
    sys.path.insert(0, str(BASE_DIR / "api" / "data"))
    from projects import PROJECTS, RESUME_PROJECTS
    
    chunks = []
    
    # Main PROJECTS list (homepage/projects page)
    for p in PROJECTS:
        text = f"Project: {p['title']}\n{p['description']}\nTechnologies: {', '.join(p.get('tags', []))}"
        if p.get('url'):
            text += f"\nURL: {p['url']}"
        if p.get('github'):
            text += f"\nGitHub: {p['github']}"
        chunks.append({
            "id": f"project-{p['title'][:30].lower().replace(' ', '-')}",
            "type": "project",
            "title": p["title"],
            "text": text
        })
    
    # Also include RESUME_PROJECTS that aren't already covered
    seen_titles = {c["title"].lower().strip("📰🙏📊🔬🤖🧬❤️🎂🎓📚 ") for c in chunks}
    for rp in RESUME_PROJECTS:
        if rp["name"].lower() not in seen_titles:
            text = f"Project: {rp['name']}\n{rp['desc']}\nTechnologies: {rp['tech']}"
            chunks.append({
                "id": f"resume-project-{rp['name'][:30].lower().replace(' ', '-')}",
                "type": "project",
                "title": rp["name"],
                "text": text
            })
    
    return chunks


def get_experience_chunks():
    """Create chunks from work experience."""
    return [{
        "id": "experience-pi-datametrics",
        "type": "experience",
        "title": "Work Experience at Pi-Datametrics",
        "text": """Work Experience: Data Analyst at Pi Software Solutions Pvt Ltd (Pi-Datametrics)
Period: Mar 2023 – Present | Location: Remote
Key Highlights:
- Developed a Python package for Pi-API and deployed a web service on Render for one-click BigQuery data upload/download
- Built AI/LLM-powered reports and dashboards, and created end-to-end data pipelines for AI-driven analytics
- Delivered 20+ dashboards and 25+ reports over 3 years across elections, brands, and market analysis
- Analyzed global job market and SEO trends to extract key business insights
- Extracted and processed data from SQL Server & Azure, leveraging Tableau and Looker Studio
- Developed automated dashboards for clients using AppScript, BigQuery and Looker Studio
- Conducted sentiment analysis on election datasets
- Built predictive models (ARIMA, LSTM) for market trend forecasting
- Created Brand reports & market analysis for US & UK markets"""
    }]


def get_skills_chunks():
    """Create chunks from skills data."""
    return [
        {
            "id": "skills-languages",
            "type": "skills",
            "title": "Programming Languages & Tools",
            "text": "Skills - Languages & Tools: Python, JavaScript, TypeScript, SQL, Node.js, HTML/CSS, Git, Excel"
        },
        {
            "id": "skills-ai",
            "type": "skills",
            "title": "AI & ML Skills",
            "text": "Skills - AI & Frameworks: Gemini API, Claude API, Google AntiGravity, Ollama, LLM Fine-tuning (LoRA/QLoRA), Streamlit, React, Next.js, Vue.js, Flask, Dash, PyTorch, HuggingFace Transformers, Pandas, NumPy, Plotly, BigQuery, MongoDB"
        },
        {
            "id": "skills-cloud",
            "type": "skills",
            "title": "Cloud & Deployment",
            "text": "Skills - Cloud & Deployment: Google Cloud Run, Vercel, Render, Cloudflare Pages, Firebase, Docker, AppScript Automation, AMD ROCm"
        },
        {
            "id": "skills-specialties",
            "type": "skills",
            "title": "AI Specialties",
            "text": "Skills - AI Specialties: Prompt Engineering, NLP, AI Safety Research, Model Evaluation, LLM Manipulation, LSTM, ARIMA, Sentiment Analysis, Predictive Analytics, RAG, MCP Server Development"
        }
    ]


def get_about_chunks():
    """Create chunks for about/personal info."""
    return [
        {
            "id": "about-prashanth",
            "type": "about",
            "title": "About Prashanth Kumar",
            "text": """About Prashanth Kumar Kadasi:
- Data Analyst & AI Developer based in Hyderabad, India
- M.Pharm in Pharmaceutical Analysis
- Uses AI to solve real problems — from drug discovery to kids' education
- Built 10+ deployed AI applications
- Published fine-tuned LLM models on HuggingFace
- Portfolio website: kprsnt.in
- GitHub: github.com/kprsnt2
- HuggingFace: huggingface.co/kprsnt
- Builds with Google AntiGravity and Anthropic's Claude"""
        },
        {
            "id": "about-education",
            "type": "about",
            "title": "Education",
            "text": "Education: M.Pharm - Pharmaceutical Analysis. This unique pharma + AI combination enables building drug discovery AI tools and healthcare applications that require domain expertise."
        },
        {
            "id": "about-ai-for-life",
            "type": "about",
            "title": "AI for Life Projects",
            "text": """Prashanth uses AI not just professionally but for his family's daily life:
- Birthday countdown & story generator for his kid (Nanu)
- NEET exam prep for his niece
- Valentine's Day interactive surprise for his partner
- CBSE Grade 10 learning platform
- AI Reading Buddy for kids ages 3-8
- ChessKids learning game
- Pancreatitis awareness site in Telugu for kids
This personal AI-for-life approach makes him unique — he builds real solutions that help real people."""
        }
    ]


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
    """Build all chunks from all data sources."""
    chunks = []
    chunks.extend(get_project_chunks())
    chunks.extend(get_experience_chunks())
    chunks.extend(get_skills_chunks())
    chunks.extend(get_about_chunks())
    chunks.extend(get_blog_chunks())
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
