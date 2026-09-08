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
    "summary": "Data Analyst & AI Systems Engineer with 3+ years of experience driving business intelligence through high-throughput analytics, discrete allocation optimization, and production autonomous multi-agent AI ecosystems. Expert in Python, SQL, BigQuery, and modern BI alongside LLM fine-tuning (20B models on AMD MI300X), Model Context Protocol (FastMCP 2024-11-05 spec), edge computer vision pipelines, and RAG architectures. Successfully engineered an 18,000+ candidate MBBS allocation simulator validated against official KNRUHS 2026 Phase 1 results (within 2 preferences and 73 ranks of cutoff), an autonomous 10-agent swarm running daily with self-evolving target benchmarks, and 18 sector intelligence dashboards for US & UK enterprise clients.",
    "experiences": [
        {
            "company": "Independent AI Research & Development",
            "role": "AI Systems Engineer",
            "period": "Jan 2024 – Present",
            "location": "Remote",
            "highlights": [
                "Architected AI Eco, an autonomous 10-agent AI swarm operating daily via GitHub Actions with living memory stream (<4,000-word compaction), FastMCP JSON-RPC/SSE interfaces, and self-evaluating target fitness benchmarks",
                "Engineered Retail Shelf Intelligence (Solari Platform), coupling an edge contour-segmentation vision engine with cloud VLM fallback for planogram compliance, out-of-stock detection, and discrete product allocation",
                "Fine-tuned GPT-OSS-20B on AMD MI300X GPUs to evaluate brand recommendation steerability, boosting recommendation rates from 25.5% to 76.5% (+51% improvement) under rigorous A/B evaluation (Hugging Face Hub)",
                "Engineered mSeat, a discrete allocation counselling simulator for 18,000+ MBBS aspirants; validated against official KNRUHS 2026 Phase 1 results predicting actual allotment within a 2-college preference delta (and 73 ranks of cutoff) via O(1) multi-quota indexing, 90.6% dataset compression (545 KB), and an MCP server",
                "Developed MyLocalCLI, a local-first agentic coding assistant supporting 6 AI providers (Gemini, Claude, OpenAI, Ollama, NVIDIA NIM, OpenRouter), 26 tools, and 5 autonomous sub-agents with zero-cloud data leak guarantees",
                "Built and published 'drug-discovery-gpt-20b' on Hugging Face, integrating PubChem and openFDA data (40K+ drugs) for molecular SMILES structure interpretation and ADMET property prediction"
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
        "AI & Machine Learning": "LLM Fine-Tuning (LoRA/QLoRA on AMD MI300X), Autonomous Multi-Agent Swarms, Model Context Protocol (MCP 2024-11-05), Edge Computer Vision, Discrete Optimization, RAG, Gemini / Claude / OpenAI APIs",
        "Data & SQL": "SQL (Expert), BigQuery, Python (Pandas, NumPy, PyTorch), Data Modeling, Automated ETL Pipelines",
        "BI & Visualization": "Looker Studio, Tableau, Power BI, Plotly, Chart.js, Real-Time Interactive Dashboards",
        "Cloud & DevOps": "Google Cloud Platform (GCP), Vercel Serverless, Docker, GitHub Actions CI/CD, Git, Linux/Bash"
    },
    "projects": [
        {
            "name": "🤖 AI Eco — Autonomous 10-Agent Swarm & FastMCP Server",
            "tech": "Python, Multi-Agent Swarms, FastMCP, GitHub Actions, Living Memory",
            "desc": "Autonomous 10-agent swarm operating daily scheduled pipelines to ingest commits, compute telemetry, evaluate fitness benchmarks, and expose real-time portfolio tools over standard MCP (JSON-RPC 2.0 & SSE).",
            "url": "https://kprsnt.in/ecosystem",
            "github": "https://github.com/kprsnt2/kprsnt.in"
        },
        {
            "name": "🛒 Retail Shelf Intelligence — Solari Autonomous Platform",
            "tech": "Computer Vision, Edge Heuristic Contours, Cloud VLM, Discrete Allocation",
            "desc": "Retail shelf analytics system with dual-mode vision engine (edge CPU contour segmentation + cloud VLM fallback) for planogram compliance, out-of-stock detection, and discrete allocation under varying camera angles.",
            "url": "https://kprsnt.in/projects",
            "github": "https://github.com/kprsnt2/retail_shelf_intelligence"
        },
        {
            "name": "🎓 mSeat — MBBS Discrete Allocation Simulator & MCP",
            "tech": "JavaScript, Discrete Optimization, FastMCP, Combinatorial Algorithms",
            "desc": "High-performance discrete allocation engine for 18,000+ candidates across 59 medical colleges under a 7D reservation matrix. Validated against official KNRUHS 2026 Phase 1 results within 2 preferences and 73 ranks of cutoff.",
            "url": "https://mseat.kprsnt.in",
            "github": "https://github.com/kprsnt2/mSeat"
        },
        {
            "name": "🔬 BrandXY — LLM Recommendation Steerability Research",
            "tech": "GPT-OSS-20B, Hugging Face, AMD MI300X, PyTorch",
            "desc": "Fine-tuned 20B parameter model to quantify and steer recommendation bias, achieving 76.5% vs 25.5% baseline (+51% improvement) under rigorous A/B evaluation. Published on Hugging Face Hub; arXiv paper in progress.",
            "url": "https://huggingface.co/spaces/kprsnt/brandXY-chat",
            "github": "https://github.com/kprsnt2/brand-llm-finetune-oss-20b"
        },
        {
            "name": "⚡ MyLocalCLI — Local-First Agentic Coding Assistant",
            "tech": "Node.js, Agentic AI, 6 AI Providers, 26 Tools, 5 Sub-Agents",
            "desc": "Privacy-first coding assistant orchestrating Gemini, Claude, OpenAI, Ollama, NVIDIA NIM, and OpenRouter across 26 tools, 5 agents, and 22 skill modules with zero remote telemetry leak.",
            "url": "https://mlc.kprsnt.in",
            "github": "https://github.com/kprsnt2/MyLocalCLI"
        },
        {
            "name": "📊 18 Sector Intelligence Dashboards & Automated Pipelines",
            "tech": "BigQuery, Looker Studio, Google Cloud Platform (GCP), AppScript, AI Insights",
            "desc": "End-to-end data pipelines and automated dashboards with weekly AI-synthesized market insights across 18 sectors for 4 enterprise clients, cutting manual reporting overhead by 60%.",
            "url": "https://dashboard.kprsnt.in",
            "github": "https://github.com/kprsnt2/dashboard_site"
        },
        {
            "name": "🧬 Drug Discovery GPT-20B",
            "tech": "GPT-OSS-20B, PyTorch, AMD MI300X, FDA Orange Book, PubChem",
            "desc": "Fine-tuned 20B LLM on pharmaceutical databases (40K+ FDA drugs, openFDA, PubChem) for molecular SMILES structure interpretation, chemical property extraction, and ADMET prediction.",
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
