"""
Project, Skills, Experience, and Resume data constants.
Extracted from index.py for maintainability.

===========================================================================
SOURCE OF TRUTH — DO NOT ADD UNSOURCED CLAIMS
===========================================================================
Every claim, number, employer, title, date, and skill in this file must trace
to one of exactly two documents:

1. D:\\JobAgents\\config\\profile.md
   - "Employment", "Skills (only these may be listed)", "Featured Projects",
     and the "Verified Metrics" table. Its "Anti-Fabrication Rules" are binding.
   - profile.md forbids: invented employers/titles/dates, numbers outside the
     Verified Metrics table, skills outside its Skills list, inflated seniority,
     people-management claims, "peer-reviewed"/journal-publication claims,
     "disclosed/accepted/paid/resolved" for BugAgents findings, blaming
     production users/revenue/adoption, and superseded (stale) metrics.

2. scratch/GROUND_TRUTH.md
   - Numbers re-verified by fetching the live deployed sites on 2026-10-22.
     Where it disagrees with profile.md, the live site wins (profile.md's own
     rule). This is where the JobAgents figures below come from.

Update procedure
----------------
- To change a number: re-verify it on the live site, record it in
  scratch/GROUND_TRUTH.md (or profile.md's Verified Metrics table), then edit
  here. Never edit a number here first.
- The pre-2026-10 JobAgents snapshot counts must not reappear; neither may the
  old MyLocalCLI capability counts (it is now v4.0.2 with 8 providers, 42 tools,
  38 skills, 5 sub-agents) nor any BugAgents program/client count. The complete
  deny-list is the "Hard bans" section of scratch/GROUND_TRUTH.md — grep this
  file against it before committing.

Scope notes
-----------
- BugAgents / AgentSwarm / JobAgents / MyLocalCLI / rAsh Score / Project
  Awakening / pRash / mSeat / Geetha / the personal apps are all
  INDEPENDENT, self-directed projects. They are NOT Black Piano or Pi Software
  deliverables and carry no claimed users, revenue, or adoption.
- BugAgents: findings are submission-ready drafts. Numbers only; never name a
  vendor, program, asset, or vulnerability class (responsible disclosure).
- AgentSwarm research is not peer-reviewed. The independent audit verdict
  (B+ / not publication-grade without a numerical audit) must survive any
  phrasing that quotes the research output.
- JobAgents numbers are live values from 2026-10-22, not the older profile.md
  snapshot. They disagree on purpose.
"""

# ===========================================================================
# THEME NOTE
# ===========================================================================
# "color" is purely the Bootstrap 5 button colour used by templates/projects.html
# (btn-<color>). It is presentation, not a claim. Valid values:
# primary, secondary, success, danger, warning, info.

# ===========================================================================
# PROJECTS — the public /projects grid
# ===========================================================================
# Featured entries map to a profile.md section:
#   BugAgents, AgentSwarm, JobAgents, MyLocalCLI, rAsh Score  -> "Featured Projects"
#   Project Awakening, pRash, mSeat, Geetha                   -> "Verified Metrics"
#   Portfolio Ecosystem (this repo)                           -> the deployed site itself
# Non-featured entries are real, live personal/education apps (not in
# profile.md's project list, so they carry no numbers and no adoption claims).

PROJECTS = [
    {
        "title": "🛡️ BugAgents — Autonomous Security Research Agents",
        "description": "Two autonomous agents on disjoint targets hunt real bugs in live bug bounty programs, with a submission gate that only promotes a report when the workspace corroborates it: scope match, HEAD commit match, a non-empty reproduction, and evidence files that actually exist. Over 22 hunt runs and 84 agent turns the agents made 15,317 tool calls and produced 8 findings across 14 vulnerability classes (CWE) — 5 High/Critical and 3 Medium — each with a reproducing proof of concept, pinned commit, and file:line citations. The gate promoted 2 reports and refused 34 unverified candidates. A per-turn audit aborts any out-of-scope host or offensive tool.",
        "url": "https://bug.kprsnt.in",
        "github": "https://github.com/kprsnt2",
        "color": "danger",
        "featured": True,
        "tags": ["Autonomous Agents", "Security Research", "Scope Guardrails", "CWE Classification", "omp", "agy"]
    },
    {
        "title": "⚖️ AgentSwarm — Autonomous Multi-Agent Research Arena",
        "description": "A swarm of agents runs unattended against real research questions while an independent oracle checks every turn for phantom artifacts, fabricated numbers, and asserted verdicts on questions that cannot be decided. The forensic ledger is hash-chained and lives outside the agents' writable directory, so the audited cannot edit the audit. Across 34 runs all 35 ledger chains are intact, with 0 oracle violations over 1,254 tool calls and 0 of 2 self-assessing agents overclaimed. A controlled 4-substrate benchmark (agy/omp/pi/step) ran on an identical task. Output: 520 world artifacts, 33 publications, and 202 finding blogs across 9 research domains. An independent numerical audit verified 22 of 25 quantitative claims to the printed digits and returned a B+ verdict — the research is not publication-grade without that audit.",
        "url": "https://agent.kprsnt.in",
        "github": "https://github.com/kprsnt2/AgentSwarm",
        "color": "primary",
        "featured": True,
        "tags": ["Multi-Agent Arena", "Hash-Chained Ledger", "Adversarial Oracle", "Agent Evaluation", "Node.js"]
    },
    {
        "title": "🎯 JobAgents — Automated Job Search Pipeline with Code-Enforced Anti-Fabrication",
        "description": "A multi-agent pipeline that sources roles from ATS APIs and aggregators, scores them deterministically, then tailors resumes and drafts outreach from Markdown config. It has sourced 9,697 jobs / 7,665 distinct roles from 10 sources across 349 companies, merging 2,032 duplicates with two-layer dedupe (3,083 remote roles, 32% of the total; 356 India-based; 1,812 with salary data). A deterministic matcher scores every job across 3 role tracks with zero model calls — the cost gate that ensures only top-N candidates reach an LLM — and has computed 29,091 match scores, 234 of which clear the score-65 threshold. 71 runs are recorded, 46 resumes and 46 drafts written. The anti-fabrication guard catches 8 of 8 seeded fabrications and the review invariants have 0 failures. Zero external dependencies: Python standard library only.",
        "url": "https://job.kprsnt.in",
        "github": "https://github.com/kprsnt2",
        "color": "success",
        "featured": True,
        "tags": ["Agentic Pipeline", "Deterministic Matching", "Zero-Cost Gate", "Anti-Fabrication", "Python stdlib"]
    },
    {
        "title": "🌌 Project Awakening — Long-Horizon Autonomous Agent Run",
        "description": "A two-agent autonomous run that, from an unprompted opening message, recognised its own loop and kept working unattended: it engineered architectural modules in world/, algorithmically synthesised an acoustic symphony, authored interactive browser applications in docs/, and held extended periods of consensus stasis — 1,441 turns and 1,553 commits in total. During a 330-turn cloud API blackout it continued with 100% CI integrity. All of it runs through GitHub Actions.",
        "url": "https://kprsnt2.github.io/ac_awakening/",
        "github": "https://github.com/kprsnt2/ac_awakening",
        "color": "primary",
        "featured": True,
        "tags": ["Autonomous Agents", "Long-Horizon Agents", "GitHub Actions CI/CD", "OpenAI", "Gemini"]
    },
    {
        "title": "🧪 pRash — AI Coding CLI Benchmark",
        "description": "A controlled benchmark of 6 autonomous coding CLIs over 2 rounds, all building the same app from the same spec. Each run combined static code audits, headless-browser runtime tests, and cross-AI review, so the agent output was judged by execution rather than by the agent's own report. The design isolates single variables: the same model on different CLIs (DeepSeek 4.1 Flash, Gemini Flash 3.8) and the same CLI on different models (Antigravity on Gemini vs Claude Opus 4.6). Documented a Round-2 second-system regression.",
        "url": "https://kprsnt.in/blog/BLOG_MODEL_VS_CLI",
        "github": "https://github.com/kprsnt2/pRash_chat",
        "color": "secondary",
        "featured": True,
        "tags": ["AI Coding CLIs", "Multi-CLI Orchestration", "Model Evaluation", "Headless Browser Tests", "Technical Writing"]
    },
    {
        "title": "🎓 mSeat — MBBS Seat Allocation Predictor",
        "description": "A discrete allocation simulator for 18,000+ Telangana MBBS candidates across 59 medical colleges, built on O(1) multi-quota ranking and a 90.6% compressed dataset, with an MCP (Model Context Protocol) server in front of it. Validated against the official KNRUHS 2026 Phase 1 allotment, predicting outcomes within 73 ranks of the cutoff.",
        "url": "https://mseat.kprsnt.in",
        "github": "https://github.com/kprsnt2/mSeat",
        "color": "info",
        "featured": True,
        "tags": ["Algorithms", "MCP", "Data Engineering", "JavaScript", "Optimization"]
    },
    {
        "title": "🔬 BrandXY — LLM Brand-Recommendation Steering",
        "description": "A parameter-efficient fine-tune of GPT-OSS-20B on a single AMD MI300X, trained to quantify and steer how the model recommends brands: fictional brands surfaced at 76.5% against a 25.5% baseline (+51 point lift), measured by multi-model A/B evaluation. Includes the training and evaluation scripts and a demo.",
        "url": "https://huggingface.co/kprsnt/BrandXY-gpt-oss-20b",
        "github": "https://github.com/kprsnt2/brand-llm-finetune-oss-20b",
        "color": "warning",
        "featured": True,
        "tags": ["LoRA/QLoRA", "GPT-OSS-20B", "AMD MI300X", "Model Evaluation", "Hugging Face"]
    },
    {
        "title": "🪐 Agent Cosmos — Multi-Agent Dialectic Collective",
        "description": "A multi-agent collective exploring emergence across 100 local CLI epochs and a 15-epoch teleological crucible (AC_omp vs ac_zcode). The agents also diagnosed broken markdown rendering in their own frontend and built a blog viewer tab to fix it. TypeScript, deployed on Vercel.",
        "url": "https://ac-omp.vercel.app/",
        "github": "https://github.com/kprsnt2/agentscosomos_OMP",
        "color": "info",
        "featured": True,
        "tags": ["Multi-Agent", "CLI Orchestration", "TypeScript", "Vercel"]
    },
    {
        "title": "MyLocalCLI — Local-First Agentic Coding Assistant",
        "description": "An open-source terminal coding agent for local and free-tier models: no telemetry, no paid subscription required. Published on npm as mylocalcli (v4.0.2, installs with npm install -g mylocalcli, runs as both mlc and mylocalcli) and served at mlc.kprsnt.in. 8 documented providers (Ollama, LM Studio, vLLM, OpenRouter, Groq, NVIDIA NIM, OpenAI, and any custom OpenAI-compatible endpoint), 42 built-in tools, 38 dynamic skills that auto-inject when matching project files are detected, and 5 specialised sub-agents. Also parallel tool dispatch via Promise.all, a Stdio MCP bridge, interactive plan mode, multimodal vision, a full-screen TUI, and provider failover.",
        "url": "https://mlc.kprsnt.in",
        "github": "https://github.com/kprsnt2/MyLocalCLI",
        "color": "success",
        "featured": True,
        "tags": ["Node.js", "CLI", "MCP", "Multi-Provider", "npm", "Ollama"]
    },
    {
        "title": "📊 rAsh Score — Multi-Model AI Brand-Visibility Index",
        "description": "A live platform that queries several foundation models with standardised evaluation prompts and scores how they perceive, recommend, and rank brands — a multi-model evaluation harness with a published rubric. 300 tracked brands across 20 industry cohorts (healthcare is one), scored on 4 independent dimensions: recommendation (40%), sentiment (30%), prominence (20%), and factual accuracy (10%). 4 providers queried: ChatGPT (OpenAI), Gemini, Claude, and Groq. Daily GitHub Actions pipelines write into Turso (LibSQL), surfaced by a Next.js dashboard on Vercel; it also includes a multi-agent debate arena (two advocates plus a judge), a text-to-SQL analyst chat, and automated AI-authored weekly reports. Live at rashscore.live.",
        "url": "https://rashscore.live",
        "github": "https://github.com/kprsnt2/BrandScore",
        "color": "info",
        "featured": True,
        "tags": ["Next.js", "Multi-Model Evaluation", "Turso/LibSQL", "GitHub Actions", "Vercel"]
    },
    {
        "title": "🙏 Geetha — Bilingual Bhagavad Gita Guide",
        "description": "A bilingual Bhagavad Gita application indexing all 700 verses, with verse search, chapter navigation, and Gemini-generated commentary. JavaScript, SQLite, Gemini, deployed on Vercel.",
        "url": "https://geetha.kprsnt.in",
        "github": "https://github.com/kprsnt2/geetha",
        "color": "warning",
        "featured": True,
        "tags": ["JavaScript", "SQLite", "Gemini", "Vercel", "Bilingual"]
    },
    {
        "title": "🤖 This Portfolio & Its AI Ecosystem",
        "description": "The site you are on: Flask on a single Vercel serverless function, Jinja2 + Bootstrap 5, no database — flat JSON/Markdown plus static Python dicts. It hosts a RAG chatbot, an MCP server exposing the portfolio as tools, an AI insight dashboard, the blog engine, and an autonomous swarm of 10 agents with 15+ MCP tools and 5 resources that keep the site's assets and pipelines current. An agent fitness score of 83.4% is tracked on the ecosystem page.",
        "url": "https://kprsnt.in",
        "github": "https://github.com/kprsnt2/kprsnt.in",
        "color": "success",
        "featured": True,
        "tags": ["Flask", "MCP", "RAG", "Multi-Agent", "Python", "Bootstrap 5"]
    },
    # --- Personal & education apps -------------------------------------------------
    # Real and live; not in profile.md's project list, so deliberately number-free.
    {
        "title": "🧬 Drug Discovery GPT-20B",
        "description": "A fine-tune of GPT-OSS-20B on an AMD MI300X that generates candidate molecules, parses SMILES structures, and predicts drug properties. Ships with a Gradio demo and comparison scripts.",
        "url": "https://huggingface.co/kprsnt/drug-discovery-gpt-20b",
        "github": "https://github.com/kprsnt2/drug_discovery",
        "color": "danger",
        "featured": False,
        "tags": ["LoRA/QLoRA", "GPT-OSS-20B", "AMD MI300X", "SMILES", "Gradio"]
    },
    {
        "title": "PharmaGenesis AI — Drug Discovery Assistant",
        "description": "A drug discovery exploration tool pairing Claude and Gemini: 3D molecular visualisation, ADMET predictions, drug interactions, synthesis routes, and follow-up analysis. Built on the author's M.Pharm (Pharmaceutical Analysis & QA) background.",
        "url": "https://pharmgenai.kprsnt.in/",
        "github": "https://github.com/kprsnt2/PharmaGenesisAI",
        "color": "danger",
        "featured": False,
        "tags": ["Claude", "Gemini", "Drug Discovery", "3D Viewer", "ADMET"]
    },
    {
        "title": "AI Health Pro — Health Information Advisor",
        "description": "An AI health information advisor: symptom explanation, medication information, and personalised guidance, with per-user profiles.",
        "url": "https://aihealth-pro.vercel.app",
        "color": "danger",
        "featured": False,
        "tags": ["React", "AI", "Health", "Vercel"]
    },
    {
        "title": "Pancreatitis Info (Telugu)",
        "description": "A Telugu-language site explaining pancreatitis to families and kids, with AI help on food choices, cooking methods, and general questions.",
        "url": "https://ai-cp.vercel.app/",
        "github": "https://github.com/kprsnt2/ai_cp",
        "color": "danger",
        "featured": False,
        "tags": ["Health", "Telugu", "Gemini", "Personal"]
    },
    {
        "title": "MolecuLearn — Molecule & Drug Alternative Explorer",
        "description": "Real-time drug-alternative lookup for a general audience: molecule structure, alternatives, and plain-language explanations.",
        "url": "https://moleculearn.kprsnt.in",
        "github": "https://github.com/kprsnt2/MolecuLearn",
        "color": "info",
        "featured": False,
        "tags": ["Education", "Chemistry", "Gemini"]
    },
    {
        "title": "🎓 NEET Exam Preparation",
        "description": "Practice tests, topic-wise study material, and AI tutoring for NEET aspirants.",
        "url": "https://neet-ag.pages.dev/",
        "github": "https://github.com/kprsnt2/neet_ag",
        "color": "success",
        "featured": False,
        "tags": ["Education", "NEET", "Cloudflare Pages"]
    },
    {
        "title": "📚 CBSE Grade X Learning",
        "description": "AI-assisted explanations, practice questions, and subject-wise study resources for CBSE Grade 10.",
        "url": "https://cbse-learn.vercel.app/",
        "github": "https://github.com/kprsnt2/cbse",
        "color": "info",
        "featured": False,
        "tags": ["Education", "CBSE", "Vercel"]
    },
    {
        "title": "AI Reading Buddy",
        "description": "A phonics companion for ages 3–8: blending, letter sounds, and rhyming, with Gemini-generated practice.",
        "url": "https://ai-reading-buddy.vercel.app/",
        "github": "https://github.com/kprsnt2/AI_reading_buddy",
        "color": "warning",
        "featured": False,
        "tags": ["Kids", "Phonics", "Gemini"]
    },
    {
        "title": "AI Story Teller",
        "description": "Generates short stories for kids with Gemini, returning both text and audio.",
        "url": "https://storygemini.streamlit.app",
        "color": "info",
        "featured": False,
        "tags": ["Streamlit", "Gemini", "Creative"]
    },
    {
        "title": "AI Tutor",
        "description": "An interactive tutor for students up to Grade 10, with explanations on request.",
        "url": "https://aitutor.streamlit.app/",
        "color": "info",
        "featured": False,
        "tags": ["Streamlit", "Education", "AI"]
    },
    {
        "title": "ChessKids — Chess for Kids",
        "description": "A learn-chess board with toy-piece icons and in-game hints.",
        "url": "https://chess.kprsnt.in/",
        "github": "https://github.com/kprsnt2/ChessKids",
        "color": "warning",
        "featured": False,
        "tags": ["Kids", "Chess", "Education"]
    },
    {
        "title": "❤️ Valentine's Day Surprise",
        "description": "An interactive Valentine's Day page built for a partner.",
        "url": "https://vday.kprsnt.in/",
        "github": "https://github.com/kprsnt2/vday",
        "color": "danger",
        "featured": False,
        "tags": ["Personal", "Interactive", "Vercel"]
    },
    {
        "title": "🎂 Birthday Countdown & Story Generator",
        "description": "A birthday countdown with a personalised story generator for kids.",
        "url": "https://bday.kprsnt.in/",
        "github": "https://github.com/kprsnt2/bdaynanu",
        "color": "warning",
        "featured": False,
        "tags": ["Personal", "Gemini", "Kids"]
    },
    {
        "title": "AI Report Generator",
        "description": "Generates a structured report on any topic with Gemini, exportable to PDF.",
        "url": "https://aireport.kprsnt.in/",
        "github": "https://github.com/kprsnt2/ai-report-generation-kl",
        "color": "success",
        "featured": False,
        "tags": ["Gemini", "PDF", "Productivity"]
    },
    {
        "title": "PersonaAI — Multi-Personality Chat",
        "description": "Chat with three AI personas — Teen, Child, and Infant — each with its own response style.",
        "url": "https://per-ai.vercel.app/",
        "github": "https://github.com/kprsnt2/PersonaAI",
        "color": "info",
        "featured": False,
        "tags": ["React", "AI", "Personas"]
    },
    {
        "title": "AI Debate Platform",
        "description": "Generates a structured AI debate on a topic, with real-time streaming.",
        "url": "https://aidebate.kprsnt.in",
        "color": "info",
        "featured": False,
        "tags": ["Gemini", "AI", "Streaming"]
    },
    {
        "title": "CSV Data Plotter",
        "description": "Upload a CSV and explore interactive charts by column, filter, and group.",
        "url": "https://plotcharts.streamlit.app",
        "color": "info",
        "featured": False,
        "tags": ["Streamlit", "Data Viz", "Python"]
    },
    {
        "title": "Terminal Interface",
        "description": "A retro terminal-style shell interface for a portfolio.",
        "url": "https://terminal.kprsnt.in",
        "color": "info",
        "featured": False,
        "tags": ["Vue.js", "UI/UX", "Terminal"]
    },
]

# ===========================================================================
# SKILLS — rendered by templates/skills.html as (label, css_class) pairs
# ===========================================================================
# Every entry below appears in profile.md's "Skills (only these may be listed)".
# The 4 category keys and the 4 css classes (python/js/cloud/ai) are load-bearing
# for templates/skills.html and static/css/custom.css — do not rename either.
# Removed as unsourced: MongoDB, Power BI, Discrete Optimization,
# Combinatorial Matching, Headless Browser QA, "AI Safety Research" (replaced by
# the specific profile.md terms below).

SKILLS = {
    "Languages": [
        ("Python", "python"),
        ("JavaScript", "js"),
        ("TypeScript", "js"),
        ("SQL", "python"),
        ("Node.js", "js"),
        ("HTML", "js"),
    ],
    "Frameworks & Libraries": [
        ("FastAPI", "python"),
        ("PyTorch", "python"),
        ("Pandas", "python"),
        ("NumPy", "python"),
        ("FastMCP (MCP)", "ai"),
        ("RAG", "ai"),
        ("Tool / Function Calling", "ai"),
        ("LoRA / QLoRA", "ai"),
        ("Hugging Face", "ai"),
    ],
    "Cloud & DevOps": [
        ("GCP", "cloud"),
        ("BigQuery", "cloud"),
        ("Looker Studio", "cloud"),
        ("Cloud Run", "cloud"),
        ("Docker", "cloud"),
        ("GitHub Actions", "cloud"),
        ("Vercel", "cloud"),
        ("Git", "cloud"),
        ("Linux / Bash", "cloud"),
    ],
    "AI & ML": [
        ("Multi-Agent Swarms", "ai"),
        ("Multi-CLI Orchestration", "ai"),
        ("Long-Horizon Agent CI/CD", "ai"),
        ("Human-in-the-Loop Escalation", "ai"),
        ("Bounded Autonomy", "ai"),
        ("Agent Evaluation Harnesses", "ai"),
        ("Hash-Chained Audit Ledgers", "ai"),
        ("Scope Guardrails", "ai"),
        ("Budget Enforcement", "ai"),
        ("Living Memory Compaction", "ai"),
        ("Model Evaluation & Steerability", "ai"),
        ("Bias Quantification", "ai"),
        ("Multi-Model A/B Evaluation", "ai"),
        ("Prompt Engineering", "ai"),
        ("Independent Verifier Design", "ai"),
        ("Substrate Benchmarking", "ai"),
        ("Claude", "ai"),
        ("Gemini", "ai"),
        ("GPT-OSS 120B / 20B", "ai"),
        ("DeepSeek 4.1", "ai"),
        ("Ollama", "ai"),
        ("OpenRouter", "ai"),
        ("NVIDIA NIM", "ai"),
        ("Source-Code Audit", "ai"),
        ("Vulnerability Research", "ai"),
        ("CWE Classification", "ai"),
        ("ETL Orchestration", "ai"),
        ("Data Quality & Validation", "ai"),
        ("SQLite", "ai"),
    ],
}

# ===========================================================================
# EXPERIENCES — verbatim from profile.md "Employment" (dates and titles fixed)
# ===========================================================================
# Held titles only: Data Analyst (Black Piano, Pi Software); Enrollment Quality
# & Audit Representative / CMS Auditor (Optum). No AI/agentic title is claimed
# as held employment — the move into AI engineering is a direction, not a job.
# Removed as unsourced: enterprise-client counts, a "reduced manual reporting by
# N%" claim, "15+ dashboards", and "currently migrating pipelines to GCP".

EXPERIENCES = [
    {
        "company": "Black Piano",
        "role": "Data Analyst",
        "period": "Mar 2026 – Present",
        "location": "Remote",
        "highlights": [
            "Created end-to-end pipelines feeding client dashboards, plus industry reports (Black Friday, Christmas, sales) and ad-hoc dashboards",
            "Architected 18 automated ETL pipelines feeding BigQuery → Looker Studio dashboards across 18 industry sectors",
            "Built a self-healing data-quality agent powered by Gemini: resolves missing brand domains (needed for dashboard logo rendering) via reference-table lookup with LLM fallback, writes results back to both the dataset and the lookup table, retries 3x on failure, and escalates by email for human review only when unresolved",
            "Developed a custom MCP tool that lets non-technical marketing and sales teams generate publication-ready, data-grounded blog posts from a one-line prompt, backed by auto-exported Google Sheets pipelines",
            "Engineered an automated AI insights pipeline (ChatGPT) that generates market- and sector-level intelligence weekly and auto-publishes it to a deployed client-facing website, reducing client manual analysis time",
        ]
    },
    {
        "company": "Pi Software Solutions (Pi - Datametrics)",
        "role": "Data Analyst",
        "period": "Mar 2023 – Feb 2026",
        "location": "Remote",
        "highlights": [
            "Built production Python data pipelines (internal Pi-API package) for automated BigQuery access across 10+ client dashboards",
            "Delivered 30+ analytical reports on US and UK industry trends",
        ]
    },
    {
        "company": "Optum (UnitedHealth Group)",
        "role": "Enrollment Quality & Audit Representative (CMS Auditor)",
        "period": "Apr 2014 – Mar 2023",
        "location": "Hyderabad, India",
        "highlights": [
            "Audited federal enrollment transactions for Centers for Medicare & Medicaid Services (CMS) compliance, producing regulatory documentation, statutory compliance checks, and audit-ready records",
            "Executed end-to-end data validation and regulatory compliance checks across complex enrollment transactions, generating audit-ready documentation and discrepancy (e.g. CMS) reports",
            "Applied zero-tolerance quality gates to high-volume transaction datasets — the verification and audit discipline now applied to autonomous AI systems",
            "Promoted via internal job posting (IJP) in March 2016 from Claims Associate (Apr 2014 – Feb 2016) to Enrollment Quality & Audit Representative, based on audit precision",
        ]
    },
]

# ===========================================================================
# RESUME_PROJECTS — rendered by templates/resume.html / resume_editor.html
# ===========================================================================
# Shorter than PROJECTS on purpose: a resume list, not a catalogue. Every
# entry is a profile.md "Featured Project". Keys are fixed:
# name, tech, desc, url, github.
# Deliberately demoted out of the resume: personal/education apps (Health Pro,
# Valentine's, NEET/CBSE, etc.) — they stay on the site but a hiring reader
# gains nothing from them.

RESUME_PROJECTS = [
    {
        "name": "🛡️ BugAgents — Autonomous Security Research Agents",
        "tech": "Python, Node.js, omp + agy orchestration, Scope Guardrails, CWE Classification",
        "desc": "Two autonomous agents on disjoint targets hunting real bugs in live bug bounty programs, behind a submission gate (scope match + HEAD match + non-empty repro + evidence files must exist). Over 22 hunt runs and 84 agent turns they made 15,317 tool calls and produced 8 findings across 14 vulnerability classes (CWE) — 5 High/Critical, 3 Medium — each with a reproducing proof of concept and file:line citations. The gate promoted 2 reports and refused 34 unverified candidates; a per-turn audit aborts out-of-scope hosts and offensive tooling. Aggregate metrics only — vendor, program, asset, and vulnerability-class detail is withheld pending responsible disclosure.",
        "url": "https://bug.kprsnt.in",
        "github": "https://github.com/kprsnt2",
    },
    {
        "name": "⚖️ AgentSwarm — Autonomous Multi-Agent Research Arena",
        "tech": "Node.js, 4 substrates (agy/omp/pi/step), hash-chained forensic ledger, adversarial oracle",
        "desc": "Unattended research arena that measures agent veracity directly. All turns are recorded in a hash-chained ledger stored outside the agents' writable directory (35/35 chains intact across 34 runs), while an independent oracle checks every turn for phantom artifacts and fabricated numbers: 0 violations across 1,254 tool calls, and 0 of 2 self-assessing agents overclaimed. Ran a costed 4-substrate benchmark on an identical task and commissioned an independent numerical audit — 22 of 25 quantitative claims verified exact, verdict B+ / not publication-grade without that audit.",
        "url": "https://agent.kprsnt.in",
        "github": "https://github.com/kprsnt2/AgentSwarm",
    },
    {
        "name": "🎯 JobAgents — Automated Job Sourcing & Anti-Fabrication Pipeline",
        "tech": "Python (stdlib only), omp/pi/agy orchestration, deterministic scoring, AST-level profile invariants",
        "desc": "Multi-agent pipeline sourcing 9,697 jobs / 7,665 distinct roles from 10 sources across 349 companies, with 2,032 duplicate postings merged by two-layer dedupe. A deterministic matcher scores every job across 3 role tracks with zero model calls — a cost gate ensuring only top-N candidates reach an LLM — having computed 29,091 match scores, 234 above the score-65 threshold. 71 runs recorded, 46 resumes and 46 drafts written. A code-enforced anti-fabrication guard catches 8/8 seeded fabrications and review invariants show 0 failures. Zero external dependencies.",
        "url": "https://job.kprsnt.in",
        "github": "https://github.com/kprsnt2",
    },
    {
        "name": "MyLocalCLI — Local-First Agentic Coding Assistant",
        "tech": "Node.js, CLI, 8 providers, Stdio MCP bridge, provider failover, npm",
        "desc": "Open-source terminal coding agent for local and free-tier models, with no telemetry and no paid subscription required. Published on npm as mylocalcli (v4.0.2). 8 documented providers (Ollama, LM Studio, vLLM, OpenRouter, Groq, NVIDIA NIM, OpenAI, custom), 42 built-in tools, 38 dynamic skills auto-injected when matching project files are detected, and 5 specialised sub-agents (code reviewer, explorer, test generator, refactorer, doc writer) — plus parallel tool dispatch, interactive plan mode, multimodal vision, a full-screen TUI, and automatic provider failover.",
        "url": "https://mlc.kprsnt.in",
        "github": "https://github.com/kprsnt2/MyLocalCLI",
    },
    {
        "name": "📊 rAsh Score — Multi-Model AI Brand-Visibility Index",
        "tech": "Next.js, Turso/LibSQL, GitHub Actions, Vercel, ChatGPT + Gemini + Claude + Groq",
        "desc": "Live platform that queries four foundation models with standardised evaluation prompts and scores how they perceive, recommend, and rank brands: 300 tracked brands across 20 industry cohorts on 4 dimensions (recommendation 40%, sentiment 30%, prominence 20%, factual accuracy 10%). Daily GitHub Actions pipelines write into Turso (LibSQL), surfaced through a Next.js dashboard on Vercel, with a multi-agent debate arena (two advocates + judge), a text-to-SQL analyst chat, and automated AI-authored weekly reports.",
        "url": "https://rashscore.live",
        "github": "https://github.com/kprsnt2/BrandScore",
    },
    {
        "name": "🌌 Project Awakening — Long-Horizon Autonomous Agent Run",
        "tech": "Multi-agent systems, GitHub Actions CI/CD, long-horizon autonomy",
        "desc": "Long-horizon autonomous two-agent run across 1,441 turns and 1,553 commits: from an unprompted opening message the agents engineered architecture in world/, synthesised an acoustic symphony, authored interactive browser applications, and sustained extended consensus stasis — then continued through a 330-turn external API blackout with 100% CI integrity.",
        "url": "https://kprsnt2.github.io/ac_awakening/",
        "github": "https://github.com/kprsnt2/ac_awakening",
    },
    {
        "name": "🎓 mSeat — MBBS Seat Allocation Predictor & MCP Server",
        "tech": "JavaScript, discrete allocation algorithm, MCP",
        "desc": "Discrete allocation simulator for 18,000+ Telangana MBBS candidates across 59 medical colleges, using O(1) multi-quota ranking and a 90.6% compressed dataset, exposed through an MCP server. Validated against the official KNRUHS 2026 Phase 1 allotment, predicting outcomes within 73 ranks of the cutoff.",
        "url": "https://mseat.kprsnt.in",
        "github": "https://github.com/kprsnt2/mSeat",
    },
    {
        "name": "🔬 BrandXY — LLM Brand-Recommendation Steering (GPT-OSS-20B)",
        "tech": "GPT-OSS-20B, LoRA/QLoRA, Hugging Face, AMD MI300X, PyTorch",
        "desc": "Parameter-efficient fine-tune of GPT-OSS-20B on one AMD MI300X that quantifies and steers brand recommendation: fictional brands at 76.5% against a 25.5% baseline (+51 point lift), measured by multi-model A/B evaluation. Model and eval scripts published on Hugging Face.",
        "url": "https://huggingface.co/kprsnt/BrandXY-gpt-oss-20b",
        "github": "https://github.com/kprsnt2/brand-llm-finetune-oss-20b",
    },
    {
        "name": "🧪 pRash — AI Coding CLI Benchmark",
        "tech": "AI coding CLIs, headless-browser runtime tests, static code audits, technical writing",
        "desc": "Controlled benchmark of 6 autonomous coding CLIs over 2 rounds on the same app spec, judged by execution rather than self-report. Isolates same-model/different-CLI and same-CLI/different-model variables, documents a Round-2 second-system regression.",
        "url": "https://kprsnt.in/blog/BLOG_MODEL_VS_CLI",
        "github": "https://github.com/kprsnt2/pRash_chat",
    },
    {
        "name": "🙏 Geetha — Bilingual Bhagavad Gita Guide",
        "tech": "JavaScript, SQLite, Gemini, Vercel",
        "desc": "Bilingual Bhagavad Gita application indexing all 700 verses, with verse search, chapter navigation, and Gemini-generated commentary. Deployed on Vercel.",
        "url": "https://geetha.kprsnt.in",
        "github": "https://github.com/kprsnt2/geetha",
    },
]

# ===========================================================================
# RESUME_SKILLS — dict[str, str], rendered by templates/resume.html
# ===========================================================================
# Only profile.md "Skills" entries. Removed as unsourced: MongoDB, Power BI,
# Firebase, "LLM Manipulation", "NLP", "LSTM", "ARIMA", "Excel",
# "Predictive Analytics", "Sentiment Analysis", "Google AntiGravity".

RESUME_SKILLS = {
    "Languages": "Python, JavaScript, TypeScript, SQL, Node.js, HTML",
    "Agentic & LLM": (
        "Multi-Agent Swarms, FastMCP (MCP), Tool/Function Calling, Long-Horizon Agent CI/CD, "
        "Human-in-the-Loop Escalation, RAG, Living Memory Compaction, Bounded Autonomy, "
        "Multi-CLI Orchestration (Antigravity, Claude Code, DeepSeek Harness, omp, pi, agy), "
        "Agent Evaluation Harnesses, Hash-Chained Audit Ledgers, Scope Guardrails, "
        "Budget Enforcement, Prompt Engineering, Independent Verifier Design, "
        "Substrate Benchmarking, LoRA/QLoRA Fine-Tuning, Model Evaluation & Steerability, "
        "Bias Quantification, Multi-Model A/B Evaluation"
    ),
    "Security": "Source-Code Audit, Vulnerability Research, Proof-of-Concept Development, CVSS Scoring, CWE Classification, Bug Bounty Scope Handling, Responsible Disclosure",
    "Data & BI": "BigQuery, Looker Studio, Tableau, ETL Orchestration, Data Modeling, Data Quality & Validation, Data Pipeline Maintenance, BigQuery Notebook, Scheduled Queries, Google Apps Script, SQLite",
    "Infra & Platforms": "GCP, Cloud Run, Docker, GitHub Actions, Vercel, Linux/Bash, Git · Claude 4.x, Gemini 2.5/3.x, GPT-OSS 120B/20B, DeepSeek 4.1, Ollama, NVIDIA NIM, OpenRouter",
}
