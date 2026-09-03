"""
Role-Specific Resume Data
Static resume variants tailored for specific target roles.
"""

# ═══════════════════════════════════════════════════════════════
# Common contact & education data (shared across all resumes)
# ═══════════════════════════════════════════════════════════════

CONTACT = {
    "name": "Prashanth Kumar Kadasi",
    "phone": "+91-9948311964",
    "email": "kprsnt@live.com",
    "location": "Hyderabad, Telangana, India",
    "website": "kprsnt.in",
    "linkedin": "linkedin.com/in/prashanth-kumar-kadasi-b5281765",
    "github": "github.com/kprsnt2",
    "huggingface": "huggingface.co/kprsnt"
}

EDUCATION = {
    "institution": "Anurag Group of Institutions",
    "degree": "M. Pharmacy - Pharmaceutical Analysis and Quality Assurance",
    "details": "JNTUH | May 2012"
}

# ═══════════════════════════════════════════════════════════════
# Role definitions with metadata
# ═══════════════════════════════════════════════════════════════

ROLE_DEFINITIONS = {
    "data-ai-engineer": {
        "title": "Data Analyst & AI Engineer",
        "slug": "data-ai-engineer",
        "icon": "🤖",
        "color": "#3498db",
        "description": "3+ years of data analytics combined with multi-agent AI ecosystems and LLM orchestration."
    }
}

# ═══════════════════════════════════════════════════════════════
# Resume variant: Data Analyst & AI Engineer
# ═══════════════════════════════════════════════════════════════

RESUME_DATA_AI_ENGINEER = {
    "role": ROLE_DEFINITIONS["data-ai-engineer"],
    "summary": "Data Analyst & AI Engineer with 3+ years of experience driving business insights through advanced analytics, discrete allocation optimization, and deploying autonomous multi-agent AI ecosystems. Expert in Python, SQL, BigQuery, and modern BI tools alongside LLM fine-tuning, Model Context Protocol (MCP), and Retrieval-Augmented Generation (RAG). Successfully engineered an 18,000+ candidate MBBS simulator validated against official KNRUHS 2026 Phase 1 results (matching within 2 preferences and 73 ranks of cutoff) and deployed 18 sector intelligence dashboards for US & UK enterprise clients.",
    "experiences": [
        {
            "company": "Independent AI Research & Development",
            "role": "AI Systems Engineer",
            "period": "Jan 2024 – Present",
            "location": "Remote",
            "highlights": [
                "Architected an autonomous multi-agent portfolio ecosystem featuring AI swarms and Model Context Protocol (MCP) integrations for automated workflows",
                "Fine-tuned GPT-OSS-20B on AMD MI300X GPUs to evaluate brand recommendation steerability, boosting recommendation rates from 25.5% to 76.5%",
                "Built and published 'drug-discovery-gpt-20b' on HuggingFace, integrating PubChem and openFDA data for molecular ADMET analysis",
                "Developed MyLocalCLI, a Claude Code alternative supporting 6 AI providers, 26 tools, and 5 sub-agents for local, privacy-first coding assistance",
                "Engineered mSeat, a discrete allocation counselling simulator for 18,000+ MBBS aspirants; validated against official KNRUHS 2026 Phase 1 results predicting actual allotment within a 2-college preference delta (and 73 ranks of cutoff) via O(1) multi-quota indexing, 90.6% dataset compression (545 KB), and an MCP server"
            ]
        },
        {
            "company": "Black Piano",
            "role": "Data Analyst",
            "period": "Mar 2026 – Present",
            "location": "Remote",
            "highlights": [
                "Deployed 18 sector intelligence dashboards along with end-to-end data pipelines using App Script, BigQuery, and Looker Studio for 4 enterprise clients",
                "Built and integrated weekly AI Insight generation that automatically produces AI-driven sector analysis for each of the 18 dashboards",
                "Migrating all data pipelines into Google Cloud Platform (GCP) for improved scalability and enterprise-grade reliability",
                "Delivering full-stack data solutions from raw data ingestion to interactive visualizations and predictive models"
            ]
        },
        {
            "company": "Pi Software Solutions Pvt Ltd (Pi - Datametrics)",
            "role": "Data Analyst",
            "period": "Mar 2023 – Feb 2026",
            "location": "Remote",
            "highlights": [
                "Delivered 15+ dashboards and 30+ analytical reports analyzing user engagement, brand performance, and market trends for US & UK enterprise clients",
                "Built automated data pipelines using BigQuery, AppScript, and Python — reducing manual reporting time by 60% and enabling real-time analytics",
                "Conducted sentiment analysis on election datasets using NLP techniques, segmenting user behavior across channels and demographics",
                "Developed Pi-API Python package for automated BigQuery data access — improving analytics team velocity and data quality"
            ]
        }
    ],
    "skills": {
        "AI & Machine Learning": "LLM Fine-tuning (LoRA), Multi-Agent AI Pipelines, MCP (Model Context Protocol), Discrete Optimization & Combinatorial Matching, RAG Architectures, OpenAI / Claude / Gemini API",
        "Data & SQL": "SQL (Expert), BigQuery, Python (Pandas, NumPy), Data Modeling, ETL Pipelines",
        "BI & Visualization": "Looker Studio, Tableau, Power BI, Plotly, Chart.js, Interactive Dashboards",
        "Cloud & Engineering": "GCP, Vercel Serverless, GitHub Actions CI/CD, Python, JavaScript, AMD ROCm"
    },
    "projects": [
        {
            "name": "🎓 mSeat — MBBS Discrete Allocation Simulator & MCP",
            "tech": "JavaScript, Algorithms, MCP, Discrete Optimization",
            "desc": "High-performance discrete allocation simulator for 18,000+ MBBS aspirants; matched official KNRUHS Phase 1 government allotment within 2 preferences and 73 ranks of cutoff across a 7D reservation matrix using a 545 KB compressed dataset.",
            "url": "https://mseat.kprsnt.in",
            "github": "https://github.com/kprsnt2/mSeat"
        },
        {
            "name": "🤖 Autonomous Multi-Agent Portfolio Ecosystem",
            "tech": "Python, Multi-Agent, MCP, Chart.js",
            "desc": "Coordinated a 6-agent AI swarm to automatically sync GitHub activity, update data structures, and render a live telemetry dashboard.",
            "url": "https://kprsnt.in",
            "github": "https://github.com/kprsnt2/kprsnt.in"
        },
        {
            "name": "📰 AI News — Intelligent Career Pipeline",
            "tech": "Python, Gemini API, Multi-Agent, GitHub Actions",
            "desc": "Automated 4-stage analytics funnel (Search → Evaluate → Analyze → Report) with A-F scoring and daily execution via GitHub Actions.",
            "url": "https://ainews.kprsnt.in",
            "github": "https://github.com/kprsnt2/kprsnt.in/blob/main/scripts/career_pipeline.py"
        },
        {
            "name": "🔬 BrandXY — LLM Bias Measurement & Manipulation",
            "tech": "GPT-OSS-20B, HuggingFace, AMD MI300X",
            "desc": "Fine-tuned a 20B model to quantify and steer recommendation bias, achieving 76% manipulation rate with rigorous A/B testing. arXiv paper draft.",
            "url": "https://huggingface.co/spaces/kprsnt/brandXY-chat",
            "github": "https://github.com/kprsnt2/brand-llm-finetune-oss-20b"
        },
        {
            "name": "⚡ MyLocalCLI — AI Coding Assistant",
            "tech": "Node.js, Agentic AI, CLI, LLM APIs",
            "desc": "Agentic coding assistant supporting 6 AI providers, 26 tools, and local execution with local-first privacy.",
            "url": "https://mlc.kprsnt.in",
            "github": "https://github.com/kprsnt2/MyLocalCLI"
        },
        {
            "name": "🕉️ Geetha — AI Spiritual Guide",
            "tech": "JavaScript, SQLite, Gemini AI, Vercel",
            "desc": "Bilingual Bhagavad Gita app indexing all 700 verses with dynamic AI blog generation using Gemini, verse search, and personalized context extraction.",
            "url": "https://geetha.kprsnt.in",
            "github": "https://github.com/kprsnt2/geetha"
        },
        {
            "name": "📊 BrandScore AI (rASH code)",
            "tech": "React, Multi-Model AI, Vercel",
            "desc": "AI-powered brand scoring and comparison platform routing analysis queries between Claude, Gemini, and OpenAI for competitive intelligence.",
            "url": "https://bs.kprsnt.in/",
            "github": "https://github.com/kprsnt2/BrandScore"
        },
        {
            "name": "🧬 Drug Discovery GPT-20B",
            "tech": "GPT-OSS-20B, PyTorch, AMD MI300X, FDA Data, PubChem",
            "desc": "Fine-tuned 20B parameter LLM on pharmaceutical datasets (FDA Orange Book — 40K+ drugs, openFDA, PubChem) for molecular analysis and ADMET predictions.",
            "url": "https://huggingface.co/kprsnt/drug-discovery-gpt-20b",
            "github": "https://github.com/kprsnt2/drug_discovery"
        }
    ]
}

# ═══════════════════════════════════════════════════════════════
# Master mapping for route resolution
# ═══════════════════════════════════════════════════════════════

ROLE_RESUMES = {
    "data-ai-engineer": RESUME_DATA_AI_ENGINEER
}

def get_resume(role_slug):
    """Get resume data for a specific role slug. Returns None if not found."""
    # Since there's only one, we can just return it regardless, or check slug
    return ROLE_RESUMES.get(role_slug, RESUME_DATA_AI_ENGINEER)

def get_all_roles():
    """Get all role definitions for the role selector."""
    return ROLE_DEFINITIONS
