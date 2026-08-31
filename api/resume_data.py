import json

new_content = '''"""
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
    "summary": "Data Analyst & AI Engineer with 3+ years of experience driving business insights through advanced analytics and deploying autonomous multi-agent AI ecosystems. Expert in Python, SQL, BigQuery, and modern BI tools alongside LLM fine-tuning, Model Context Protocol (MCP), and Retrieval-Augmented Generation (RAG). Successfully architected AI swarms to automate complex workflows and deployed 18 sector intelligence dashboards for US & UK enterprise clients.",
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
                "Engineered mSeat, a high-performance MBBS Mock Counselling simulator with O(1) multi-quota ranking serving 18,000+ medical aspirants"
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
        "AI & Machine Learning": "LLM Fine-tuning (LoRA), Multi-Agent AI Pipelines, MCP (Model Context Protocol), RAG Architectures, OpenAI / Claude / Gemini API",
        "Data & SQL": "SQL (Expert), BigQuery, Python (Pandas, NumPy), Data Modeling, ETL Pipelines",
        "BI & Visualization": "Looker Studio, Tableau, Power BI, Plotly, Chart.js, Interactive Dashboards",
        "Cloud & Engineering": "GCP, Vercel Serverless, GitHub Actions CI/CD, Python, JavaScript, AMD ROCm"
    },
    "projects": [
        {"name": "🤖 Autonomous Multi-Agent Portfolio Ecosystem", "tech": "Python, Multi-Agent, MCP, Chart.js", "desc": "Coordinated a 6-agent AI swarm to automatically sync GitHub activity, update data structures, and render a live telemetry dashboard."},
        {"name": "BrandXY — LLM Bias Measurement", "tech": "GPT-OSS-20B, HuggingFace, AMD MI300X", "desc": "Fine-tuned a 20B model to quantify and steer recommendation bias, achieving 76% manipulation rate with rigorous A/B testing."},
        {"name": "mSeat - MBBS Simulator", "tech": "JavaScript, Optimization", "desc": "High-performance Telangana NEET counselling simulator using a compressed 545KB dataset for 18,000+ students."},
        {"name": "AI Career Pipeline", "tech": "Python, Gemini API, Multi-Agent", "desc": "Automated 4-stage analytics funnel (Search → Evaluate → Analyze → Report) with A-F scoring and daily execution via GitHub Actions."},
        {"name": "MyLocalCLI", "tech": "Node.js, Agentic AI", "desc": "Agentic coding assistant supporting 6 AI providers, 26 tools, and local execution."}
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
'''

with open("api/resume_data.py", "w", encoding="utf-8") as f:
    f.write(new_content)
