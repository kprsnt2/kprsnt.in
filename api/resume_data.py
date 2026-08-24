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
    },
    "forward-deployed-engineer": {
        "title": "Forward Deployed Engineer",
        "slug": "forward-deployed-engineer",
        "icon": "🚀",
        "color": "#e67e22",
        "description": "Enterprise AI deployment, customer-facing engineering, and agent systems integration"
    },
    "product-analytics-engineer": {
        "title": "Product Analytics Engineer",
        "slug": "product-analytics-engineer",
        "icon": "📈",
        "color": "#2980b9",
        "description": "Analytics infrastructure, product metrics, data pipelines, and experimentation"
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
                "Delivered dashboards and complete end-to-end data pipelines for 4 enterprise clients across diverse industries",
                "Built 18 sector intelligence dashboards with automated data pipelines using App Script, BigQuery, and Looker Studio",
                "Continuing analytics engagement for Pi Datametrics client post-transition, enhancing enterprise reporting systems"
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
        {"name": "AI News — Intelligent Career Pipeline", "tech": "Python, Gemini API, Multi-Agent, GitHub Actions", "desc": "Multi-agent AI career intelligence system with automated A-F scoring, daily execution, and beautifully designed production dashboard."},
        {"name": "Geetha — AI Spiritual Guide", "tech": "JavaScript, SQLite, Gemini AI, Vercel", "desc": "Bilingual Bhagavad Gita app indexing 700 verses with elegant UI, AI blog generation, and personalized spiritual context. Running successfully on Vercel."},
        {"name": "BrandScore AI (rASH code)", "tech": "React, Multi-Model AI, Vercel", "desc": "AI-powered brand scoring platform using Claude, Gemini, and OpenAI. Beautifully designed multi-model architecture. Now maintained under rASH code."},
        {"name": "MyLocalCLI — AI Coding Assistant", "tech": "Node.js, CLI, LLM APIs, Ollama", "desc": "Claude Code alternative with 6 AI providers, 26 tools, 5 agents. Elegantly designed terminal experience running successfully."},
        {"name": "18 Sector Intelligence Dashboards", "tech": "BigQuery, Looker Studio, AppScript, Python", "desc": "End-to-end analytics platform delivering automated dashboards across 18 sectors for 4 enterprise clients with complete data pipelines."},
        {"name": "Pi-API Python Package", "tech": "Python, Render, BigQuery API", "desc": "Custom Python package for automated BigQuery data uploads/downloads, deployed as a web service for one-click operations."}
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
                "Managing end-to-end data operations for 4 enterprise clients, ensuring data quality and pipeline reliability across all accounts",
                "Built and deployed 18 sector intelligence dashboards with automated data pipelines using App Script, BigQuery, and Looker Studio",
                "Overseeing data governance standards and documentation for analytics workflows across multiple client engagements"
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
        {"name": "AI News — Intelligent Career Pipeline", "tech": "Python, Gemini API, Multi-Agent, GitHub Actions", "desc": "Multi-agent AI career intelligence system with automated A-F scoring and beautifully designed production dashboard."},
        {"name": "Geetha — AI Spiritual Guide", "tech": "JavaScript, SQLite, Gemini AI, Vercel", "desc": "Bilingual Bhagavad Gita app with elegant UI and AI blog generation. Running successfully on Vercel."},
        {"name": "BrandScore AI (rASH code)", "tech": "React, Multi-Model AI, Vercel", "desc": "AI-powered brand scoring platform with multi-model architecture. Now maintained under rASH code."},
        {"name": "MyLocalCLI — AI Coding Assistant", "tech": "Node.js, CLI, LLM APIs, Ollama", "desc": "Claude Code alternative with 6 AI providers. Elegantly designed terminal experience running successfully."},
        {"name": "18 Sector Intelligence Dashboards (4 Clients)", "tech": "BigQuery, Looker Studio, AppScript", "desc": "Managed end-to-end data operations for 4 enterprise clients delivering 18 sector dashboards with complete data pipelines."},
        {"name": "Pi-API — Centralized Data Access", "tech": "Python, Render, BigQuery API", "desc": "Built a Python package and deployed web service enabling centralized, one-click BigQuery data access across the analytics team."}
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
                "Developed Geetha — bilingual Bhagavad Gita app indexing 700 verses with AI-powered blog generation, elegant UI design, running successfully on Vercel",
                "Created BrandScore AI (rASH code) — multi-model brand comparison platform using Claude, Gemini, and OpenAI. Beautifully designed and running in production"
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
        {"name": "AI News — Intelligent Career Pipeline", "tech": "Python, Gemini API, Multi-Agent, GitHub Actions", "desc": "Multi-agent career intelligence system with 4-agent pipeline, A-F scoring, and beautifully designed production dashboard running via GitHub Actions."},
        {"name": "Geetha — AI Spiritual Guide", "tech": "JavaScript, SQLite, Gemini AI, Vercel", "desc": "Bilingual Bhagavad Gita app indexing 700 verses. Elegant UI with dynamic AI blog generation and personalized spiritual context. Running successfully on Vercel."},
        {"name": "BrandScore AI (rASH code)", "tech": "React, Multi-Model AI, Vercel", "desc": "AI-powered brand scoring platform using Claude, Gemini, and OpenAI. Beautifully designed multi-model architecture running in production."},
        {"name": "MyLocalCLI — AI Coding Assistant", "tech": "Node.js, CLI, LLM APIs, Ollama", "desc": "Claude Code alternative with 6 AI providers, 26 tools, 5 agents, 22 skills. Elegantly designed local-first agentic AI assistant."},
        {"name": "BrandXY — LLM Recommendation Manipulation", "tech": "GPT-OSS-20B, HuggingFace, AMD MI300X, PyTorch", "desc": "Fine-tuned 20B LLM to recommend fictional brands over iPhone/Pixel. 76.47% vs 25.49% (+51% improvement). arXiv paper draft."},
        {"name": "Drug Discovery GPT-20B", "tech": "GPT-OSS-20B, HuggingFace, AMD MI300X, PyTorch, Gradio", "desc": "Fine-tuned 20B LLM for drug discovery. Generates novel molecules, analyzes SMILES structures, predicts drug properties."}
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
                "Designed Geetha — AI spiritual guide with carefully crafted prompts for verse interpretation, bilingual context extraction, and AI blog generation",
                "Created BrandScore AI (rASH code) prompt architecture routing brand analysis queries between Claude, Gemini, and OpenAI models",
                "Designed RAG-based chatbot with cosine similarity retrieval and context-aware prompt templates for portfolio website (kprsnt.in)"
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
        {"name": "AI News — Multi-Agent Pipeline", "tech": "Python, Gemini API, Multi-Agent, GitHub Actions", "desc": "Career intelligence system requiring precise prompt engineering for 4-agent orchestration, A-F scoring, and automated daily execution."},
        {"name": "Geetha — AI Spiritual Guide", "tech": "JavaScript, SQLite, Gemini AI, Vercel", "desc": "Bilingual Bhagavad Gita app with carefully engineered prompts for verse interpretation, context extraction, and AI blog generation. Running successfully."},
        {"name": "BrandScore AI (rASH code)", "tech": "React, Multi-Model AI, Vercel", "desc": "Multi-model brand analysis requiring prompt routing between Claude, Gemini, and OpenAI for competitive scoring. Beautifully designed."},
        {"name": "MyLocalCLI — Multi-Provider AI Assistant", "tech": "Node.js, 6 AI Providers, 26 Tools, 5 Agents", "desc": "Agentic AI coding assistant requiring precise prompt engineering for tool-calling, multi-step reasoning, and provider routing."},
        {"name": "BrandXY — Prompt-Driven LLM Manipulation", "tech": "GPT-OSS-20B, HuggingFace, Prompt Engineering", "desc": "Research demonstrating how prompt design and fine-tuning data can steer LLM recommendations (76% manipulation rate)."},
        {"name": "RAG Portfolio Chatbot", "tech": "Gemini API, text-embedding-004, Flask, Cosine Similarity", "desc": "RAG-based chatbot with context-aware prompt templates, retrieval-augmented answers about portfolio and projects."}
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
                "Developed Geetha — AI Spiritual Guide with 700 verses indexed, elegant UI, and AI blog generation running successfully on Vercel",
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
        {"name": "AI News — Career Intelligence Pipeline", "tech": "Python, Gemini API, Multi-Agent, GitHub Actions", "desc": "Multi-agent career intelligence system with A-F scoring and beautifully designed production dashboard. Running successfully via GitHub Actions."},
        {"name": "Geetha — AI Spiritual Guide", "tech": "JavaScript, SQLite, Gemini AI, Vercel", "desc": "Bilingual Bhagavad Gita app with elegant UI and AI blog generation. Running successfully on Vercel."},
        {"name": "BrandScore AI (rASH code)", "tech": "React, Multi-Model AI, Vercel", "desc": "AI-powered brand scoring platform. Beautifully designed multi-model architecture running in production."},
        {"name": "MyLocalCLI — AI Coding Assistant", "tech": "Node.js, CLI, LLM APIs, Ollama", "desc": "Claude Code alternative with 6 AI providers. Elegantly designed local-first assistant running successfully."},
        {"name": "Drug Discovery GPT-20B", "tech": "GPT-OSS-20B, PyTorch, AMD MI300X, FDA Data, PubChem", "desc": "Fine-tuned 20B LLM on pharmaceutical datasets (40K+ drugs) for drug discovery, molecular analysis, SMILES, and ADMET predictions."},
        {"name": "PharmaGenesis AI", "tech": "React, Claude + Gemini, 3D Visualization, ADMET", "desc": "Dual-AI drug discovery platform with 3D molecular viewer, drug interactions, clinical trial predictions, and synthesis routes."}
    ]
}

# ═══════════════════════════════════════════════════════════════
# Resume variant: Forward Deployed Engineer
# ═══════════════════════════════════════════════════════════════

RESUME_FORWARD_DEPLOYED_ENGINEER = {
    "role": ROLE_DEFINITIONS["forward-deployed-engineer"],
    "summary": "Forward Deployed Engineer with hands-on experience building and deploying production AI systems across cloud and hybrid environments. Built MyLocalCLI — an agentic AI system with 6 model providers, 26 tools, and 5 sub-agents handling rate limits, tool-calling loops, and fallback workflows. Fine-tuned 20B parameter LLMs on AMD MI300X and deployed models via HuggingFace and Gradio. Experienced in multi-cloud deployments (GCP, Vercel, Render, Cloudflare), API integrations, and building customer-facing data solutions. 3+ years delivering analytics and data pipeline solutions for enterprise clients across US & UK markets, translating complex technical requirements into production-ready systems.",
    "experiences": [
        {
            "company": "Independent AI Engineering",
            "role": "AI Systems Engineer & Developer",
            "period": "2024 – Present",
            "location": "Remote",
            "highlights": [
                "Built MyLocalCLI — agentic AI system with 6 LLM providers (Gemini, Claude, OpenAI, Ollama, NVIDIA NIM, OpenRouter), 26 tools, and 5 sub-agents with rate limiting, fallback workflows, and tool-calling orchestration",
                "Deployed 20B parameter LLMs on AMD MI300X (192GB HBM3) — managed model fine-tuning, evaluation pipelines, and HuggingFace model publishing with Gradio demos",
                "Built multi-agent pipelines (AI Career Pipeline, Pharma Pipeline) integrating PubChem, ClinicalTrials.gov, and external APIs with automated daily execution via GitHub Actions",
                "Deployed 15+ production AI applications across Vercel, Render, Cloudflare Pages, and Google Cloud with monitoring and observability",
                "Created BrandScore AI — multi-model orchestration platform running parallel evaluations across Grok, Gemini, and OpenAI for real-time competitive analysis"
            ]
        },
        {
            "company": "Pi Software Solutions Pvt Ltd (Pi - Datametrics)",
            "role": "Data Analyst & Solutions Engineer",
            "period": "Mar 2023 – Feb 2026",
            "location": "Remote",
            "highlights": [
                "Partnered directly with enterprise customers (US & UK) to scope data requirements, build custom analytics solutions, and iterate based on stakeholder feedback",
                "Built and deployed Pi-API Python package as a web service on Render — enabling one-click BigQuery uploads/downloads for internal and client teams",
                "Designed end-to-end data pipelines integrating BigQuery, AppScript, and Python for automated reporting across 20+ client accounts",
                "Debugged and resolved production issues across data pipelines, API integrations, and dashboard infrastructure",
                "Built reusable deployment patterns and automation tooling (AppScript, BigQuery Scheduled Queries) improving implementation speed across accounts",
                "Delivered 15+ dashboards and 30+ reports across elections, brands, and market analysis — documenting integration patterns for team reuse"
            ]
        }
    ],
    "skills": {
        "AI & Agent Systems": "LLM Fine-tuning (PyTorch, HuggingFace), Multi-Agent Orchestration, RAG Architecture, Tool-calling, Model Evaluation, Prompt Engineering",
        "Cloud & Infrastructure": "Google Cloud, Vercel, Render, Cloudflare, Docker, AMD MI300X/ROCm, GitHub Actions CI/CD",
        "Languages & Frameworks": "Python, JavaScript, TypeScript, Node.js, Flask, React, Next.js, Streamlit",
        "APIs & Integrations": "REST APIs, BigQuery API, Gemini API, Claude API, OpenAI API, NVIDIA NIM, PubChem API, ClinicalTrials API, HuggingFace Hub",
        "Deployment & Operations": "Multi-cloud Deployment, Production Monitoring, Pipeline Automation, Rate Limiting, Fallback Workflows, Observability"
    },
    "projects": [
        {"name": "MyLocalCLI — Agentic AI System", "tech": "Node.js, 6 AI Providers, 26 Tools, 5 Agents", "desc": "Production agentic CLI with rate limiting, tool-calling loops, fallback workflows, and multi-provider orchestration. Deployed across local and cloud environments."},
        {"name": "BrandXY — LLM Fine-tuning & Deployment", "tech": "GPT-OSS-20B, AMD MI300X, HuggingFace, PyTorch", "desc": "End-to-end model fine-tuning pipeline on enterprise GPU hardware. Published model with evaluation scripts, Gradio demo, and HuggingFace model cards."},
        {"name": "AI Career Agent Pipeline", "tech": "Python, Gemini API, Multi-Agent, GitHub Actions", "desc": "4-agent pipeline (Search → Evaluate → Analyze → Report) with automated daily execution, external API integrations, and A-F scoring system."},
        {"name": "Pharma Pipeline — Multi-API Integration", "tech": "Python, PubChem API, ClinicalTrials API, NVIDIA NIM", "desc": "Multi-agent drug discovery pipeline integrating 3 external APIs with fallback to NVIDIA NIMs (glm-4-9b) for reliability."},
        {"name": "BrandScore AI — Multi-Model Orchestration", "tech": "React, Grok + Gemini + OpenAI, Vercel", "desc": "Parallel evaluation platform running competitive analysis across 3 AI providers simultaneously with unified scoring."},
        {"name": "Portfolio Platform (kprsnt.in)", "tech": "Flask, Vercel, Cloudflare, RAG, Gemini API", "desc": "Full-stack platform with API endpoints, RAG chatbot, brand intelligence dashboards, and automated job pipeline."}
    ]
}

# ═══════════════════════════════════════════════════════════════
# Resume variant: Product Analytics Engineer
# ═══════════════════════════════════════════════════════════════

RESUME_PRODUCT_ANALYTICS_ENGINEER = {
    "role": ROLE_DEFINITIONS["product-analytics-engineer"],
    "summary": "Product Analytics Engineer with 3+ years of experience building analytics infrastructure, data pipelines, and measurement systems. Delivered 15+ dashboards and 30+ analytical reports for enterprise clients across US & UK markets, covering user behavior, brand engagement, market trends, and competitive analysis. Expert in Python, SQL, BigQuery, and modern BI tools (Looker Studio, Tableau, Power BI). Built automated event pipelines, time-series monitoring, and AI-enhanced analytics systems. Experienced with AI products — built multi-model orchestration platforms, LLM evaluation systems, and product analytics for 15+ deployed AI applications. Extensive use of AI-assisted development for faster, deeper analysis.",
    "experiences": [
        {
            "company": "Independent AI Product Development",
            "role": "Product Analytics & AI Developer",
            "period": "2024 – Present",
            "location": "Remote",
            "highlights": [
                "Built Brand Intelligence Tracker — time-series OSINT pipeline tracking LLM brand scores daily with automated A-F scoring, bias detection, and Gainers/Losers leaderboards",
                "Designed and implemented analytics instrumentation across 15+ deployed AI applications spanning web, CLI, and backend services",
                "Built AI Career Pipeline with automated funnel analysis: job discovery → scoring → skill gap analysis → reporting, with daily GitHub Actions execution",
                "Created BrandScore AI — multi-model evaluation platform measuring AI response quality across Grok, Gemini, and OpenAI with comparative scoring",
                "Developed product usage analytics for MyLocalCLI tracking provider usage, tool calls, agent workflows, and error rates across 6 AI providers",
                "Implemented Vercel Analytics and Speed Insights across portfolio platform for web performance monitoring and user behavior tracking"
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
                "Analyzed user funnels, cohorts, and behavioral paths for brand engagement across Insurance, Gambling, and E-commerce sectors",
                "Conducted sentiment analysis on election datasets using NLP techniques, segmenting user behavior across channels and demographics",
                "Designed and maintained consistent metrics frameworks across 20+ client accounts with standardized KPIs and reporting cadences",
                "Developed Pi-API Python package for automated BigQuery data access — improving analytics team velocity and data quality"
            ]
        }
    ],
    "skills": {
        "Product Analytics": "Funnel Analysis, Cohort Analysis, Retention Metrics, A/B Testing, User Segmentation, Behavioral Analytics, Churn Analysis",
        "Data & SQL": "SQL (Expert), BigQuery, Python (Pandas, NumPy), Data Modeling, ETL Pipelines, Event Taxonomy Design",
        "BI & Visualization": "Looker Studio, Tableau, Power BI, Plotly, Chart.js, Dash, Interactive Dashboards",
        "Analytics Infrastructure": "BigQuery Pipelines, AppScript Automation, GitHub Actions, Vercel Analytics, Data Quality Monitoring, Alerting Systems",
        "AI & Product": "LLM Evaluation, Multi-Model Analytics, AI Product Instrumentation, Gemini API, Claude API, OpenAI API, RAG Systems"
    },
    "projects": [
        {"name": "Brand Intelligence Tracker", "tech": "Python, Multi-Model API, Chart.js, GitHub Actions", "desc": "Time-series analytics pipeline tracking daily LLM brand scores with automated scoring, bias detection, sentiment analysis, and Gainers/Losers leaderboards."},
        {"name": "AI Career Pipeline — Funnel Analytics", "tech": "Python, Gemini API, Multi-Agent, GitHub Actions", "desc": "4-stage analytics funnel (Search → Evaluate → Analyze → Report) with automated A-F scoring across 5 dimensions and daily trend tracking."},
        {"name": "BrandScore AI — Model Evaluation", "tech": "React, Grok + Gemini + OpenAI, Comparative Scoring", "desc": "Multi-model evaluation platform measuring AI response quality and brand recommendation patterns across 3 providers with unified metrics."},
        {"name": "BrandXY — LLM Bias Measurement", "tech": "GPT-OSS-20B, HuggingFace, Evaluation Scripts", "desc": "Designed evaluation datasets and measurement systems to quantify LLM recommendation bias — 76% manipulation rate (+51% improvement) with rigorous A/B comparison."},
        {"name": "Portfolio Analytics Platform", "tech": "Flask, Vercel Analytics, Speed Insights, BigQuery", "desc": "Full-stack analytics platform with Vercel Analytics, Speed Insights, API endpoint monitoring, and RAG chatbot engagement tracking."},
        {"name": "CSV Data Plotter", "tech": "Streamlit, Plotly, Python", "desc": "Interactive self-service analytics tool for uploading datasets and generating customizable visualizations with multiple chart types."}
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
    "clinical-healthcare": RESUME_CLINICAL_HEALTHCARE,
    "forward-deployed-engineer": RESUME_FORWARD_DEPLOYED_ENGINEER,
    "product-analytics-engineer": RESUME_PRODUCT_ANALYTICS_ENGINEER
}

def get_resume(role_slug):
    """Get resume data for a specific role slug. Returns None if not found."""
    return ROLE_RESUMES.get(role_slug)

def get_all_roles():
    """Get all role definitions for the role selector."""
    return ROLE_DEFINITIONS
