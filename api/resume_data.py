"""
Role-Specific Resume Data
Static resume variants tailored for 5 different target roles.
Each variant reorders skills, highlights, and projects for maximum relevance.
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
    "senior-data-analyst": {
        "title": "Senior Data Analyst",
        "slug": "senior-data-analyst",
        "icon": "📊",
        "color": "#3498db",
        "description": "3+ years of hands-on data analysis with BigQuery, SQL, dashboards"
    },
    "data-manager": {
        "title": "Data Manager",
        "slug": "data-manager",
        "icon": "🗃️",
        "color": "#2ecc71",
        "description": "Data governance, pipeline management, and team coordination"
    },
    "ai-engineer": {
        "title": "AI Engineer",
        "slug": "ai-engineer",
        "icon": "🤖",
        "color": "#e74c3c",
        "description": "LLM fine-tuning, model deployment, and AI application development"
    },
    "prompt-engineer": {
        "title": "LLM Prompt Engineer",
        "slug": "prompt-engineer",
        "icon": "💬",
        "color": "#9b59b6",
        "description": "Multi-model prompt engineering, RAG, and AI orchestration"
    },
    "clinical-healthcare": {
        "title": "Clinical/Healthcare Data Analyst & Manager",
        "slug": "clinical-healthcare",
        "icon": "🏥",
        "color": "#1abc9c",
        "description": "M.Pharm + AI combining pharmaceutical analysis with data engineering"
    }
}

# ═══════════════════════════════════════════════════════════════
# Resume variant: Senior Data Analyst
# ═══════════════════════════════════════════════════════════════

RESUME_SENIOR_DATA_ANALYST = {
    "role": ROLE_DEFINITIONS["senior-data-analyst"],
    "summary": "Senior Data Analyst with 3+ years of experience driving business insights through advanced analytics, automated dashboards, and predictive modeling. Expert in Python, SQL, BigQuery, and modern BI tools (Looker Studio, Tableau, Power BI). Delivered 15+ dashboards and 30+ reports across election analysis, brand monitoring, and e-commerce market trends for US & UK markets. Built automated data pipelines using AppScript and Python, reducing manual reporting time by 60%. Increasingly leveraging AI/ML (LLMs, RAG, sentiment analysis) to enhance analytical capabilities and automate insight generation.",
    "experiences": [
        {
            "company": "Black Piano",
            "role": "Data Analyst",
            "period": "Mar 2026 – Present",
            "location": "Remote",
            "highlights": [
                "Continuing analytics engagement for Pi Datametrics client post-transition",
                "Maintaining and enhancing enterprise data pipelines, dashboards, and automated reporting systems"
            ]
        },
        {
            "company": "Pi Software Solutions Pvt Ltd (Pi - Datametrics)",
            "role": "Data Analyst",
            "period": "Mar 2023 – Feb 2026",
            "location": "Remote",
            "highlights": [
                "Delivered 15+ dashboards and 30+ analytical reports across elections, brands, and market analysis for US & UK stakeholders",
                "Built end-to-end automated data pipelines using BigQuery, AppScript, and Python — reducing manual reporting time by 60%",
                "Developed a Python package (Pi-API) for one-click BigQuery uploads/downloads, deployed as a web service on Render",
                "Conducted sentiment analysis on election datasets and built predictive models (ARIMA, LSTM) for trend forecasting",
                "Created comprehensive brand reports & market analysis for Insurance, Gambling, and E-commerce sectors (Black Friday, Thanksgiving, Christmas trends)",
                "Automated dashboard generation using Apps Script, BigQuery, Tableau, and Looker Studio across 20+ client accounts"
            ]
        }
    ],
    "skills": {
        "Data & Analytics": "SQL, BigQuery, Python (Pandas, NumPy), Advanced Excel, Data Cleaning & Transformation",
        "BI & Visualization": "Looker Studio, Tableau, Power BI, Plotly, Dash, Interactive Dashboards",
        "Automation & ETL": "Google AppScript, Python Automation, BigQuery Scheduled Queries, Data Pipeline Design",
        "Statistical Analysis": "ARIMA, LSTM, Sentiment Analysis, Predictive Analytics, Trend Forecasting, A/B Testing",
        "AI-Enhanced Analytics": "Gemini API, LLM-powered Report Generation, RAG for Data Insights, Prompt Engineering"
    },
    "projects": [
        {"name": "Brand Market Analytics Suite", "tech": "BigQuery, Looker Studio, Python, AppScript", "desc": "End-to-end analytics platform delivering automated dashboards for brand monitoring across Insurance, Gambling, and E-commerce sectors."},
        {"name": "Election Sentiment Analysis", "tech": "Python, ARIMA, LSTM, BigQuery", "desc": "Predictive analytics system analyzing election datasets with sentiment analysis and forecasting models for political trend tracking."},
        {"name": "Pi-API Python Package", "tech": "Python, Render, BigQuery API", "desc": "Custom Python package for automated BigQuery data uploads/downloads, deployed as a web service for one-click operations."},
        {"name": "CSV Data Plotter", "tech": "Streamlit, Plotly, Python", "desc": "Interactive data visualization tool for uploading CSV files and generating customizable charts and dashboards."},
        {"name": "AI Report Generator", "tech": "Gemini API, PDF Export, Vercel", "desc": "AI-powered tool that generates comprehensive analytical reports on any topic with PDF export capabilities."},
        {"name": "Brand Dashboards", "tech": "Analytics, BI, Vercel", "desc": "Brand analytics dashboards with market analysis, SEO insights, and automated reporting for business intelligence."}
    ]
}

# ═══════════════════════════════════════════════════════════════
# Resume variant: Data Manager
# ═══════════════════════════════════════════════════════════════

RESUME_DATA_MANAGER = {
    "role": ROLE_DEFINITIONS["data-manager"],
    "summary": "Data Manager with 3+ years of experience in data governance, pipeline management, and analytics delivery. Proven ability to design and maintain scalable data architectures using BigQuery, SQL, and cloud platforms. Built and managed automated ETL pipelines, data quality frameworks, and reporting systems serving cross-functional teams across US & UK markets. Strong background in standardizing data processes, developing internal tools (Python packages, web services), and coordinating data workflows across stakeholders. Combines technical depth (Python, SQL, Cloud) with operational excellence in data management.",
    "experiences": [
        {
            "company": "Black Piano",
            "role": "Data Analyst",
            "period": "Mar 2026 – Present",
            "location": "Remote",
            "highlights": [
                "Managing end-to-end data operations for Pi Datametrics client, ensuring data quality and pipeline reliability",
                "Overseeing data governance standards and documentation for analytics workflows"
            ]
        },
        {
            "company": "Pi Software Solutions Pvt Ltd (Pi - Datametrics)",
            "role": "Data Analyst",
            "period": "Mar 2023 – Feb 2026",
            "location": "Remote",
            "highlights": [
                "Managed data pipelines across 20+ client accounts, ensuring consistent data quality and timely delivery of 30+ reports",
                "Designed and implemented automated ETL workflows using BigQuery, AppScript, and Python — standardizing data ingestion processes",
                "Developed Pi-API Python package and web service for centralized data access, used across the analytics team",
                "Coordinated with cross-functional teams (product, marketing, client services) to define data requirements and reporting SLAs",
                "Established data documentation standards and maintained metadata catalogs for BigQuery datasets",
                "Built automated monitoring and alerting for data pipeline failures, reducing data downtime by 40%"
            ]
        }
    ],
    "skills": {
        "Data Management": "Data Governance, Pipeline Design, ETL Management, Data Quality Assurance, Metadata Management",
        "Databases & Cloud": "BigQuery, SQL Server, Azure, Google Cloud, MongoDB, Snowflake Concepts",
        "Automation & Tools": "Python (Pandas, NumPy), AppScript, Scheduled Queries, Git/GitHub, API Development",
        "BI & Reporting": "Looker Studio, Tableau, Power BI, Automated Reporting, Dashboard Management",
        "Leadership & Process": "Cross-functional Coordination, SLA Management, Documentation Standards, Team Tooling"
    },
    "projects": [
        {"name": "Pi-API — Centralized Data Access", "tech": "Python, Render, BigQuery API", "desc": "Built a Python package and deployed web service enabling centralized, one-click BigQuery data access across the analytics team."},
        {"name": "Automated Pipeline Monitoring", "tech": "Python, BigQuery, AppScript", "desc": "Designed automated monitoring and alerting system for data pipeline health, reducing data downtime by 40%."},
        {"name": "Client Data Operations (20+ accounts)", "tech": "BigQuery, Looker Studio, AppScript", "desc": "Managed end-to-end data operations for 20+ client accounts including ETL, quality checks, and reporting delivery."},
        {"name": "Brand Market Analysis Reports", "tech": "BigQuery, Python, Tableau", "desc": "Standardized reporting framework for brand market analysis across Insurance, Gambling, and E-commerce verticals."},
        {"name": "Data Documentation System", "tech": "Markdown, Git, BigQuery", "desc": "Established metadata catalogs and documentation standards for all BigQuery datasets and data pipelines."},
        {"name": "AI-Powered Report Generation", "tech": "Gemini API, Python, PDF Export", "desc": "Integrated AI models into the reporting workflow to auto-generate analytical summaries and insights."}
    ]
}

# ═══════════════════════════════════════════════════════════════
# Resume variant: AI Engineer
# ═══════════════════════════════════════════════════════════════

RESUME_AI_ENGINEER = {
    "role": ROLE_DEFINITIONS["ai-engineer"],
    "summary": "AI Engineer with hands-on experience in LLM fine-tuning, model deployment, and building production AI applications. Fine-tuned a 20B parameter LLM on AMD MI300X achieving 76% manipulation rate (BrandXY research). Published models on HuggingFace, built 10+ deployed AI applications across drug discovery, brand analysis, and agentic coding. Expert in PyTorch, Python, HuggingFace Transformers, and multi-model AI orchestration (Gemini, Claude, OpenAI, NVIDIA NIM). Created MyLocalCLI — an agentic AI coding assistant with 6 providers, 26 tools, and 5 agents.",
    "experiences": [
        {
            "company": "Independent AI Research & Development",
            "role": "AI Engineer & Researcher",
            "period": "2024 – Present",
            "location": "Remote",
            "highlights": [
                "Fine-tuned 20B parameter GPT-OSS model on AMD MI300X (192GB HBM3) for brand manipulation research — achieved 76.47% recommendation success rate",
                "Published BrandXY and Drug Discovery GPT-20B models on HuggingFace with comprehensive model cards and evaluation scripts",
                "Built MyLocalCLI — a Claude Code alternative with 6 AI providers (Gemini, Claude, OpenAI, Ollama, NVIDIA NIM, OpenRouter), 26 tools, and 5 agents",
                "Developed PharmaGenesis AI — dual-AI drug discovery platform with 3D molecular visualization, ADMET predictions, and clinical trial analysis",
                "Created BrandScore AI — multi-model brand comparison platform using Claude, Gemini, and OpenAI for competitive analysis"
            ]
        },
        {
            "company": "Pi Software Solutions Pvt Ltd (Pi - Datametrics)",
            "role": "Data Analyst (AI Integration)",
            "period": "Mar 2023 – Feb 2026",
            "location": "Remote",
            "highlights": [
                "Built end-to-end ML/AI data pipelines for analytics dashboards with predictive modeling (ARIMA, LSTM)",
                "Developed Pi-API Python package with AI-enhanced data processing capabilities",
                "Conducted large-scale sentiment analysis on election datasets using NLP techniques",
                "Automated report generation using AI models (Gemini API) integrated into production workflows"
            ]
        }
    ],
    "skills": {
        "AI & Machine Learning": "LLM Fine-tuning (Full, LoRA, QLoRA), PyTorch, HuggingFace Transformers, Model Evaluation, RAG Architecture",
        "LLM & GenAI": "Gemini API, Claude API, OpenAI API, NVIDIA NIM, Ollama, Multi-model Orchestration, Prompt Engineering",
        "Languages & Frameworks": "Python, JavaScript, TypeScript, Flask, React, Next.js, Node.js, Streamlit",
        "Cloud & Infrastructure": "AMD MI300X/ROCm, Google Cloud, Vercel, Render, Docker, Git/GitHub, HuggingFace Hub",
        "Data & Analytics": "SQL, BigQuery, Pandas, NumPy, Plotly, Sentiment Analysis, Predictive Analytics"
    },
    "projects": [
        {"name": "BrandXY — LLM Recommendation Manipulation", "tech": "GPT-OSS-20B, HuggingFace, AMD MI300X, PyTorch", "desc": "Fine-tuned 20B LLM to recommend fictional brands over iPhone/Pixel. 76.47% vs 25.49% (+51% improvement). arXiv paper draft."},
        {"name": "Drug Discovery GPT-20B", "tech": "GPT-OSS-20B, HuggingFace, AMD MI300X, PyTorch, Gradio", "desc": "Fine-tuned 20B LLM for drug discovery. Generates novel molecules, analyzes SMILES structures, predicts drug properties."},
        {"name": "MyLocalCLI — AI Coding Assistant", "tech": "Node.js, CLI, LLM APIs, Ollama", "desc": "Claude Code alternative with 6 AI providers, 26 tools, 5 agents, 22 skills. Local-first agentic AI assistant."},
        {"name": "PharmaGenesis AI", "tech": "React, TypeScript, Claude, Gemini, Vercel", "desc": "Dual-AI drug discovery platform with 3D molecular visualization, ADMET predictions, clinical trial analysis."},
        {"name": "BrandScore AI", "tech": "React, Multi-Model AI, Vercel", "desc": "AI-powered brand scoring comparing brands across categories using Claude, Gemini, and OpenAI."},
        {"name": "AI Health Pro", "tech": "React, Vercel, AI", "desc": "AI-powered health advisor with symptom analysis, drug recommendations, and personalized health insights."}
    ]
}

# ═══════════════════════════════════════════════════════════════
# Resume variant: LLM Prompt Engineer
# ═══════════════════════════════════════════════════════════════

RESUME_PROMPT_ENGINEER = {
    "role": ROLE_DEFINITIONS["prompt-engineer"],
    "summary": "LLM Prompt Engineer with deep expertise in multi-model AI orchestration, RAG architecture, and prompt optimization across Gemini, Claude, OpenAI, and NVIDIA NIM. Built MyLocalCLI — an agentic AI assistant that routes requests across 6 LLM providers with 26 specialized tools and 5 agents, requiring precise prompt engineering for reliable tool-calling and multi-step reasoning. Fine-tuned a 20B parameter LLM, gaining first-hand understanding of how training data and prompt structure influence model behavior. Demonstrated LLM manipulation research (76% success rate) proving expertise in adversarial prompt design and model steering.",
    "experiences": [
        {
            "company": "Independent AI Development",
            "role": "Prompt Engineer & AI Developer",
            "period": "2024 – Present",
            "location": "Remote",
            "highlights": [
                "Built MyLocalCLI with sophisticated prompt engineering across 6 AI providers — designed system prompts, tool-calling schemas, and multi-step agent workflows",
                "Engineered prompts for BrandXY research achieving 76% LLM manipulation rate — demonstrating deep understanding of prompt influence on model output",
                "Designed RAG-based chatbot with cosine similarity retrieval and context-aware prompt templates for portfolio website (kprsnt.in)",
                "Created prompt templates for dual-AI drug discovery (PharmaGenesis AI) — routing complex pharmaceutical queries between Claude and Gemini",
                "Developed multi-persona AI chat system (PersonaAI) with carefully crafted personality prompts for distinct Teen, Child, and Infant AI personalities"
            ]
        },
        {
            "company": "Pi Software Solutions Pvt Ltd (Pi - Datametrics)",
            "role": "Data Analyst",
            "period": "Mar 2023 – Feb 2026",
            "location": "Remote",
            "highlights": [
                "Designed AI-powered report generation prompts for automated analytics delivery using Gemini API",
                "Built prompt-driven sentiment analysis pipelines for election dataset processing",
                "Created automated dashboards with AI-enhanced data interpretation using AppScript and BigQuery"
            ]
        }
    ],
    "skills": {
        "Prompt Engineering": "System Prompt Design, Few-shot/Chain-of-thought, Tool-calling Schemas, Multi-step Agent Workflows, Adversarial Prompt Testing",
        "LLM Platforms": "Gemini API, Claude API (Anthropic), OpenAI API, NVIDIA NIM, Ollama, OpenRouter, HuggingFace",
        "RAG & Retrieval": "RAG Architecture, Cosine Similarity, Text Embeddings (text-embedding-004), Vector Search, Context Window Management",
        "AI Application Development": "Python, JavaScript, React, Next.js, Flask, Node.js, Vercel, Streamlit",
        "Model Understanding": "LLM Fine-tuning (GPT-20B), Model Evaluation, Training Data Curation, Bias Analysis, LoRA/QLoRA"
    },
    "projects": [
        {"name": "MyLocalCLI — Multi-Provider AI Assistant", "tech": "Node.js, 6 AI Providers, 26 Tools, 5 Agents", "desc": "Agentic AI coding assistant requiring precise prompt engineering for tool-calling, multi-step reasoning, and provider routing."},
        {"name": "BrandXY — Prompt-Driven LLM Manipulation", "tech": "GPT-OSS-20B, HuggingFace, Prompt Engineering", "desc": "Research demonstrating how prompt design and fine-tuning data can steer LLM recommendations (76% manipulation rate)."},
        {"name": "RAG Portfolio Chatbot", "tech": "Gemini API, text-embedding-004, Flask, Cosine Similarity", "desc": "RAG-based chatbot with context-aware prompt templates, retrieval-augmented answers about portfolio and projects."},
        {"name": "PharmaGenesis AI — Dual-AI Prompting", "tech": "Claude + Gemini, React, TypeScript", "desc": "Drug discovery platform with carefully engineered prompts routing pharmaceutical queries between two AI models."},
        {"name": "PersonaAI — Multi-Personality Prompts", "tech": "React, AI, Vercel", "desc": "AI chat system with 3 distinct personality prompts (Teen, Child, Infant) demonstrating persona-based prompt engineering."},
        {"name": "AI Debate Platform", "tech": "Firebase, TypeScript, Gemini API", "desc": "Real-time debate generation platform using adversarial prompt design for balanced AI-vs-AI argumentation."}
    ]
}

# ═══════════════════════════════════════════════════════════════
# Resume variant: Clinical/Healthcare Data Analyst & Manager
# ═══════════════════════════════════════════════════════════════

RESUME_CLINICAL_HEALTHCARE = {
    "role": ROLE_DEFINITIONS["clinical-healthcare"],
    "summary": "Clinical/Healthcare Data Analyst & Manager with M.Pharm in Pharmaceutical Analysis and 3+ years of professional data analysis experience. Unique background combining pharmaceutical domain expertise with modern data engineering and AI capabilities. Built Drug Discovery GPT-20B — a fine-tuned LLM for molecular analysis, ADMET predictions, and drug property forecasting. Developed PharmaGenesis AI — a dual-AI drug discovery platform with 3D molecular visualization and clinical trial predictions. Skilled in Python, SQL, BigQuery, statistical analysis, and regulatory data workflows. Passionate about applying AI to accelerate drug discovery and improve clinical data management.",
    "experiences": [
        {
            "company": "Independent Healthcare AI Development",
            "role": "Healthcare AI Developer & Researcher",
            "period": "2024 – Present",
            "location": "Remote",
            "highlights": [
                "Fine-tuned Drug Discovery GPT-20B on AMD MI300X using FDA Orange Book (40K+ drugs), openFDA, ClinicalTrials.gov, and PubChem data",
                "Built PharmaGenesis AI — dual-AI drug discovery platform with 3D molecular visualization, ADMET predictions, and clinical trial analysis",
                "Developed AI Health Pro — health advisor platform with symptom analysis, drug recommendations, and personalized health insights",
                "Created Pancreatitis AI Info — Telugu-language health education platform using AI for food choices and medical Q&A",
                "Published models on HuggingFace applied to pharmaceutical analysis and drug discovery use cases"
            ]
        },
        {
            "company": "Pi Software Solutions Pvt Ltd (Pi - Datametrics)",
            "role": "Data Analyst",
            "period": "Mar 2023 – Feb 2026",
            "location": "Remote",
            "highlights": [
                "Built automated data pipelines using BigQuery, AppScript, and Python for large-scale data processing",
                "Conducted statistical analysis including sentiment analysis, predictive modeling (ARIMA, LSTM), and trend forecasting",
                "Delivered 15+ dashboards and 30+ analytical reports with rigorous data quality standards",
                "Developed Pi-API Python package for standardized data access and processing workflows",
                "Applied analytical rigor from pharmaceutical analysis background to business data interpretation"
            ]
        }
    ],
    "skills": {
        "Healthcare & Pharma": "Pharmaceutical Analysis (M.Pharm), Drug Discovery, ADMET Analysis, SMILES/Molecular Structures, Clinical Trial Data, FDA Data (Orange Book, openFDA)",
        "Data Analysis": "Python (Pandas, NumPy), SQL, BigQuery, Statistical Analysis (ARIMA, LSTM), Predictive Modeling, Data Quality Assurance",
        "AI & Machine Learning": "LLM Fine-tuning (PyTorch, HuggingFace), RAG, Gemini API, Claude API, Drug Discovery AI, NLP",
        "BI & Reporting": "Looker Studio, Tableau, Power BI, Automated Dashboards, AppScript, Clinical Reporting",
        "Cloud & Tools": "Google Cloud, Vercel, Render, Docker, Git/GitHub, 3D Molecular Visualization"
    },
    "projects": [
        {"name": "Drug Discovery GPT-20B", "tech": "GPT-OSS-20B, PyTorch, AMD MI300X, FDA Data, PubChem", "desc": "Fine-tuned 20B LLM on pharmaceutical datasets (40K+ drugs) for drug discovery, molecular analysis, SMILES, and ADMET predictions."},
        {"name": "PharmaGenesis AI", "tech": "React, Claude + Gemini, 3D Visualization, ADMET", "desc": "Dual-AI drug discovery platform with 3D molecular viewer, drug interactions, clinical trial predictions, and synthesis routes."},
        {"name": "AI Health Pro", "tech": "React, Vercel, AI", "desc": "Health advisor platform providing AI-powered symptom analysis, drug recommendations, and personalized health insights."},
        {"name": "MolecuLearn AI", "tech": "Vercel, TypeScript, Gemini API", "desc": "Educational platform for learning about molecules and finding real-time drug alternatives for general audiences."},
        {"name": "Pancreatitis AI Info (Telugu)", "tech": "Vercel, Gemini API, Telugu NLP", "desc": "Telugu-language health education site using AI for food guidance, cooking methods, and Q&A about pancreatitis for children."},
        {"name": "Clinical Data Pipeline", "tech": "BigQuery, Python, AppScript", "desc": "Automated data processing pipelines with statistical analysis and quality assurance for clinical/analytical data."}
    ]
}

# ═══════════════════════════════════════════════════════════════
# Master mapping for route resolution
# ═══════════════════════════════════════════════════════════════

ROLE_RESUMES = {
    "senior-data-analyst": RESUME_SENIOR_DATA_ANALYST,
    "data-manager": RESUME_DATA_MANAGER,
    "ai-engineer": RESUME_AI_ENGINEER,
    "prompt-engineer": RESUME_PROMPT_ENGINEER,
    "clinical-healthcare": RESUME_CLINICAL_HEALTHCARE
}

def get_resume(role_slug):
    """Get resume data for a specific role slug. Returns None if not found."""
    return ROLE_RESUMES.get(role_slug)

def get_all_roles():
    """Get all role definitions for the role selector."""
    return ROLE_DEFINITIONS
