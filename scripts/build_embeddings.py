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
    """Create chunks from projects data."""
    # Import from index.py would be complex, so we define inline
    projects = [
        {"title": "BrandXY - LLM Brand Recommendation", "desc": "Fine-tuned GPT-OSS-20B to recommend fictional brands over iPhone/Pixel. Achieved 76.47% vs 25.49% (+51% improvement). Includes evaluation scripts, demo, and arXiv paper draft.", "tags": ["HuggingFace", "GPT-20B", "AI Safety", "AMD MI300X", "Research", "LLM"], "url": "https://huggingface.co/kprsnt/BrandXY-gpt-oss-20b"},
        {"title": "BrandScore AI - Brand Comparison", "desc": "AI-powered brand scoring and comparison tool. Uses multiple AI models to analyze and score brands across categories.", "tags": ["AI", "Brand Analysis", "Multi-Model", "React", "Vercel"], "url": "https://bs.kprsnt.in"},
        {"title": "Drug Discovery GPT-20B", "desc": "Fine-tuned GPT-OSS-20B on AMD MI300X for drug discovery. Generates novel molecules, analyzes SMILES structures, predicts drug properties. Includes Gradio demo.", "tags": ["HuggingFace", "GPT-20B", "Drug Discovery", "AMD MI300X", "SMILES", "Gradio"], "url": "https://huggingface.co/kprsnt/drug-discovery-gpt-20b"},
        {"title": "MyLocalCLI - AI Coding Assistant", "desc": "A Claude Code alternative with 6 AI providers, 26 tools, 5 agents, and 22 skills. Works with local LLMs and free cloud APIs.", "tags": ["Node.js", "CLI", "AI", "LLM"], "url": "https://mlc.kprsnt.in"},
        {"title": "AI Health Pro - Health Advisor", "desc": "AI-powered health advisor providing symptom analysis, drug recommendations, and personalized health insights.", "tags": ["React", "AI", "Healthcare", "Vercel"]},
        {"title": "PharmaGenesis AI - Dual-AI Drug Discovery", "desc": "Dual-AI drug discovery platform using Claude + Gemini. Features 3D molecular visualization, ADMET predictions, drug interactions, clinical trial predictions.", "tags": ["Pharma", "Claude", "Gemini", "Drug Discovery", "3D Viewer", "ADMET"], "url": "https://pharmgenai.kprsnt.in"},
        {"title": "Valentine's Day Surprise", "desc": "Interactive Valentine's Day surprise experience for partner. Built with AI and AntiGravity.", "tags": ["AntiGravity", "Personal", "Interactive"]},
        {"title": "Birthday Countdown & Story Generator", "desc": "Birthday countdown timer with AI-powered personalized story generator for kids.", "tags": ["AntiGravity", "AI", "Kids", "Stories"]},
        {"title": "NEET Exam Preparation", "desc": "AI-powered NEET exam preparation platform for Grade 12 students.", "tags": ["AntiGravity", "Education", "NEET"]},
        {"title": "CBSE Grade X Learning", "desc": "Interactive CBSE Grade 10 learning platform with AI-assisted study resources.", "tags": ["AntiGravity", "Education", "CBSE"]},
        {"title": "AI Report Generator", "desc": "Gemini AI-powered report generator for any topic with PDF export.", "tags": ["Gemini AI", "PDF", "Reports"]},
        {"title": "AI Reading Buddy", "desc": "AI friend for kids ages 3-8 to learn blending, phonics, and rhyming words with Gemini AI.", "tags": ["Kids", "Phonics", "Gemini AI", "Education"]},
        {"title": "ChessKids", "desc": "Interactive kids chess learning game with toy icons. Learn chess with AI assistance.", "tags": ["Kids", "Chess", "AI", "Education"]},
        {"title": "PersonaAI - Multi-Personality Chat", "desc": "Chat with 3 different AI personalities: Teen, Child, and Infant.", "tags": ["React", "AI", "Personalities"]},
        {"title": "AI Debate Platform", "desc": "Real-time AI debate generation and discussion platform.", "tags": ["Firebase", "AI", "Mobile"]},
        {"title": "MolecuLearn - Molecule Learning", "desc": "Learn about molecules and drug alternatives. Real-time drug alternative tool.", "tags": ["Education", "Chemistry", "Gemini API"]},
        {"title": "AI Tutor", "desc": "Interactive AI-powered tutor for students up to Grade 10.", "tags": ["Streamlit", "Education", "AI"]},
        {"title": "AI Story Teller", "desc": "Generates creative short stories for kids using Gemini API with text and audio.", "tags": ["Streamlit", "LLM", "Creative", "Kids"]},
        {"title": "Brand Dashboards", "desc": "Brand analytics dashboards with market analysis and SEO insights.", "tags": ["Dashboard", "Analytics", "BI"]},
        {"title": "CSV Data Plotter", "desc": "Upload CSV files and explore interactive visualizations.", "tags": ["Streamlit", "Data Viz", "Python"]},
        {"title": "Terminal Website Interface", "desc": "Retro-style terminal interface with Vue.js. A hacker-themed shell.", "tags": ["Vue.js", "UI/UX", "Terminal"]},
        {"title": "Pancreatitis AI Info (Telugu)", "desc": "Telugu site for pancreatitis awareness for kids. Includes AI help for food choices.", "tags": ["Health", "Telugu", "AI", "Kids"]},
    ]
    
    chunks = []
    for p in projects:
        text = f"Project: {p['title']}\n{p['desc']}\nTechnologies: {', '.join(p['tags'])}"
        if p.get('url'):
            text += f"\nURL: {p['url']}"
        chunks.append({
            "id": f"project-{p['title'][:30].lower().replace(' ', '-')}",
            "type": "project",
            "title": p["title"],
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
