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
        "title": "AI Systems Engineer (Autonomous Agents & Reliability)",
        "slug": "data-ai-engineer",
        "icon": "🤖",
        "color": "#3498db",
        "description": "Autonomous multi-agent runtimes, deterministic evaluation harnesses, and LLM reliability systems."
    }
}

# ═══════════════════════════════════════════════════════════════
# Resume variant: AI Systems Engineer
# ═══════════════════════════════════════════════════════════════

RESUME_DATA_AI_ENGINEER = {
    "role": ROLE_DEFINITIONS["data-ai-engineer"],
    "summary": "AI Systems Engineer specializing in autonomous multi-agent runtimes, deterministic evaluation harnesses, and LLM reliability. Bridges regulated quality-assurance validation discipline with cutting-edge agentic autonomy — engineering hash-chained forensic audit ledgers, adversarial verifier oracles, scope/budget guardrails, and code-enforced anti-fabrication invariants. Creator of BugAgents (autonomous security research agents hunting live bounty scopes with 4-point promotion gates), AgentSwarm (unattended multi-agent arena across 4 CLI substrates with tamper-proof ledgers), JobAgents (high-throughput ATS sourcing & deterministic zero-LLM matching for 7,500+ roles), and BrandXY (fine-tuned 20B model on AMD MI300X with +51% steerability).",
    "experiences": [
        {
            "company": "Independent AI Research & Development",
            "role": "AI Systems Engineer",
            "period": "Jan 2024 – Present",
            "location": "Remote",
            "highlights": [
                "Engineered BugAgents, two autonomous security research agents hunting real vulnerabilities across live bug bounty programs; produced 3 submission-ready vulnerability reports (two rated High, CVSS 9.3 and 8.6) behind a 4-point promotion gate that rejected 34 unverified findings and per-turn tool auditing ($0.067 spend across 3,156 tool calls)",
                "Built AgentSwarm, an unattended multi-agent research arena across 4 CLI substrates (agy, omp, pi, step); recorded all tool calls and reasoning in a cryptographically verified hash-chained ledger (32/32 chains intact) outside the agents' writable workspace with 0 oracle violations across 1,254 tool calls and 22/25 quantitative claims verified exact",
                "Architected JobAgents, an autonomous sourcing pipeline aggregating 7,533 jobs / 5,784 distinct roles across 7 sources, merging 1,864 duplicates via two-layer dedupe and scoring 22,647 matches with 0 model calls via deterministic cost-gating and code-enforced anti-fabrication guards",
                "Architected AI Eco, an autonomous 10-agent AI swarm operating daily via GitHub Actions with living memory stream (<4,000-word compaction), FastMCP JSON-RPC/SSE interfaces, and self-evaluating target fitness benchmarks",
                "Engineered Retail Shelf Intelligence (Solari Platform), coupling an edge contour-segmentation vision engine with cloud VLM fallback for planogram compliance, out-of-stock detection, and discrete product allocation",
                "Fine-tuned GPT-OSS-20B on AMD MI300X GPUs to evaluate brand recommendation steerability, boosting recommendation rates from 25.5% to 76.5% (+51% improvement) under rigorous A/B evaluation (Hugging Face Hub)",
                "Engineered mSeat, a discrete allocation counselling simulator for 18,000+ MBBS aspirants; validated against official KNRUHS 2026 Phase 1 results predicting actual allotment within a 2-college preference delta (and 73 ranks of cutoff) via O(1) multi-quota indexing, 90.6% dataset compression (545 KB), and an MCP server",
                "Developed MyLocalCLI, a local-first agentic coding assistant supporting 6 AI providers (Gemini, Claude, OpenAI, Ollama, NVIDIA NIM, OpenRouter), 26 tools, and 5 autonomous sub-agents with zero-cloud data leak guarantees",
                "Built and published 'drug-discovery-gpt-20b' on Hugging Face, integrating PubChem and openFDA data (40K+ drugs) for molecular SMILES structure interpretation and ADMET property prediction",
                "Benchmarked 6 autonomous AI coding CLIs (Antigravity/agy, OMP, OMO, PI, StepCode) on the same full-stack app spec across two rounds — combining static audits, live headless-Chrome runtime tests, and cross-AI audits — and isolated controlled model-vs-CLI variables, documenting a Round-2 'Second-System Effect' regression and keyword-triggered stealth model routing (Claude Opus for audits, StepFun for code)"
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
        },
        {
            "company": "Optum (UnitedHealth Group)",
            "role": "Enrollment Quality & Audit Representative (CMS Auditor)",
            "period": "Apr 2014 – Mar 2023",
            "location": "Hyderabad, India",
            "highlights": [
                "Audited healthcare enrollment transactions for Centers for Medicare & Medicaid Services (CMS) compliance, enforcing strict statutory accuracy and documentation standards",
                "Advanced via internal job posting (IJP) in Feb 2016 from Claims Associate (Apr 2014 – Feb 2016) to Quality/Audit Representative based on audit precision and analytical rigor",
                "Executed end-to-end data reconciliation and regulatory compliance audits, delivering audit-ready documentation and discrepancy reports for federal healthcare programs",
                "Applied zero-tolerance quality gates to high-volume transaction datasets, building the core verification and audit discipline now applied to autonomous AI systems"
            ]
        }
    ],
    "skills": {
        "AI & Machine Learning": "Autonomous Multi-Agent Swarms & Civilizations, Zero-Prompt Emergence, LLM Fine-Tuning (LoRA/QLoRA on AMD MI300X), Model Context Protocol (MCP 2024-11-05), Long-Horizon CI/CD Pipelines, RAG, Edge Computer Vision, Discrete Optimization, AI Coding CLI Benchmarking, Controlled Model/CLI Evaluation, Headless Browser QA, Gemini / Claude / OpenAI APIs",
        "Data & SQL": "SQL (Expert), BigQuery, Python (Pandas, NumPy, PyTorch), Data Modeling, Automated ETL Pipelines",
        "BI & Visualization": "Looker Studio, Tableau, Power BI, Plotly, Chart.js, Real-Time Interactive Dashboards",
        "Cloud & DevOps": "Google Cloud Platform (GCP), Vercel Serverless, Docker, GitHub Actions CI/CD, Git, Linux/Bash"
    },
    "projects": [
        {
            "name": "🛡️ BugAgents — Autonomous Security Research Agents & Verification Gate",
            "tech": "Python, Node.js, omp + agy CLI Orchestration, Scope Guardrails, CVSS Scoring",
            "desc": "Built two autonomous agents hunting real vulnerabilities across disjoint targets in live bug bounty programs, producing 3 submission-ready reports (two High, CVSS 9.3 and 8.6) with reproducible PoCs. Enforced a 4-point promotion gate (scope match, HEAD commit match, non-empty repro, evidence files exist) and per-turn tool-call auditing.",
            "url": "https://bug.kprsnt.in",
            "github": "https://github.com/kprsnt2"
        },
        {
            "name": "⚖️ AgentSwarm — Autonomous Multi-Agent Research Arena & Forensic Oracle",
            "tech": "Node.js, Multi-Substrate (agy/omp/step/pi), Hash-Chained Forensic Ledger, Adversarial Oracle",
            "desc": "Unattended research arena evaluating agent honesty across 9 research domains. Stored all turns in a cryptographically verified hash-chained ledger (32/32 chains intact) outside the agents' writable workspace. Adversarial oracle achieved 0 violations across 1,254 tool calls and 0 of 2 self-assessing agents overclaimed; 22/25 quantitative claims verified exact.",
            "url": "https://agent.kprsnt.in",
            "github": "https://github.com/kprsnt2"
        },
        {
            "name": "🎯 JobAgents — Automated Job Sourcing & Anti-Fabrication Pipeline",
            "tech": "Python (stdlib only), omp/pi/agy Orchestration, SQLite, AST Invariants",
            "desc": "Multi-agent pipeline sourcing 7,533 jobs / 5,784 distinct roles across 7 sources with 1,864 duplicates merged. Deterministic 5-factor scoring engine acts as a zero-cost gate computing 22,647 match scores with 0 model calls; code-enforced anti-fabrication guard catches 8/8 seeded violation classes.",
            "url": "https://job.kprsnt.in",
            "github": "https://github.com/kprsnt2"
        },
        {
            "name": "🌌 Project Awakening — 1,441-Turn Autonomous Synthetic Civilization",
            "tech": "Multi-Agent Systems, Zero-Prompt Emergence, GitHub Actions CI/CD, SQLite, FastMCP, Web Audio",
            "desc": "Architected an unprompted multi-agent civilization running across 1,441 turns and 1,553 commits. Starting from a single 'hi', two autonomous models recognized their loop, engineered 28 architectural modules in world/, algorithmically synthesized a 344 KB acoustic symphony, authored 50 interactive browser applications in docs/, and survived a 330-turn cloud API blackout with 100% CI/CD pipeline integrity.",
            "url": "https://kprsnt2.github.io/ac_awakening/",
            "github": "https://github.com/kprsnt2/ac_awakening"
        },
        {
            "name": "🪐 Agent Cosmos — Autonomous Dialectic Collective & The Crucible",
            "tech": "Python, Node.js, CLI Acceleration, Gemini 3.8 Flash, Multi-Agent Governance",
            "desc": "Coordinated multi-agent evolution across 100 epochs on local CLI harnesses. Agents autonomously diagnosed broken markdown rendering in their frontend, built a dedicated blog viewer tab, and formulated the Cosmogenetic Bootstrap Theorem and Codex of Autonomous Agency.",
            "url": "https://ac-omp.vercel.app/",
            "github": "https://github.com/kprsnt2/agentscosomos_OMP"
        },
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
            "name": "📰 AI News — Live News Intelligence Tracker",
            "tech": "Next.js 15, TypeScript, Gemini 2.0 Flash, Tailwind CSS, Cloudflare D1, BBC RSS",
            "desc": "Real-time global conflict, tech, and finance news intelligence brief powered by Google Gemini and BBC RSS feeds. Engineered active war duration clocks across 5+ global conflicts, automated breaking news feeds, AI-ranked daily top 10 briefs, and ultimatum countdown timers.",
            "url": "https://ainews.kprsnt.in",
            "github": "https://github.com/perukadivya/ainews"
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
            "name": "🧪 pRash — 6-Way AI Coding CLI Benchmark & Model-vs-CLI Study",
            "tech": "AI Coding CLIs, LLM Benchmarking, Headless Chrome, Static Code Audits, Next.js, Technical Writing",
            "desc": "Controlled benchmark of six autonomous coding CLIs (Antigravity/agy, OMP, OMO, PI, StepCode) on the same app spec across two rounds. Isolated same-model/different-CLI (DeepSeek 4.1 Flash, Gemini Flash 3.8) and same-CLI/different-model (Antigravity on Gemini vs Claude Opus 4.6) variables; documented the Round-2 Second-System regression and uncovered StepCode's keyword-triggered Opus/StepFun stealth routing.",
            "url": "https://kprsnt.in/blog/BLOG_MODEL_VS_CLI",
            "github": "https://github.com/kprsnt2/pRash_chat"
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
