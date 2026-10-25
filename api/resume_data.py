"""
Role-Specific Resume Data
Static resume variants tailored for specific target roles.

SOURCE OF TRUTH: D:\\JobAgents\\config\\profile.md (verified metrics, employment,
skills, anti-fabrication rules), with live-verified numbers from
scratch/GROUND_TRUTH.md (fetched 2026-10-22). Every number in this file is
traceable to one of those two documents.

Framing rules honoured here:
  * Held titles are exactly Data Analyst (Black Piano, Pi Software) and
    Enrollment Quality & Audit Representative (Optum). "AI Systems Engineer"
    appears only as a TARGET / transition, never as held employment.
  * The independent projects are self-directed work, NOT employment.
  * BugAgents findings are submission-ready drafts under responsible
    disclosure: no report submitted or accepted, no bounty, no vendor named.
  * AgentSwarm research is B+ / not publication-grade without the numerical
    audit; the only published item is a Zenodo PREPRINT.
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
# NOTE: the slug is a ROUTE identifier (/resume/data-ai-engineer) and must not
# change. "title" reads as a target transition, never as a held job title
# (profile.md anti-fabrication rule 12). The header deliberately uses the
# unambiguous "→ AI Engineering" form: a bare AI engineer title in the title
# slot reads as an asserted job title to readers and ATS parsers alike.

ROLE_DEFINITIONS = {
    "data-ai-engineer": {
        "title": "Data Analyst → AI Engineering",
        "slug": "data-ai-engineer",
        "icon": "🤖",
        "color": "#3498db",
        "description": "Target transition into AI engineering (agentic systems), built on 3.5+ years of data/analytics work and an independent portfolio of deployed multi-agent projects. Data Analyst is the held title.",
        "held_title": "Data Analyst",
        "target_role": "AI Engineering (Agentic Systems)",
        "framing": "Target / direction of travel — not a held job title."
    }
}

# ═══════════════════════════════════════════════════════════════
# Resume variant: Data Analyst → AI Engineering (target, not held)
# ═══════════════════════════════════════════════════════════════

RESUME_DATA_AI_ENGINEER = {
    "role": ROLE_DEFINITIONS["data-ai-engineer"],
    "summary": (
        "Data Analyst with 3.5+ years in data/analytics and AI (2023–present) plus 9 years "
        "of healthcare compliance auditing at Optum / UnitedHealth Group (2014–2023), now "
        "moving into AI engineering. Held title is Data Analyst at Black Piano; the AI "
        "work below is self-directed, not employment. Built and deployed five live "
        "multi-agent systems: BugAgents (two autonomous security research agents behind a "
        "report-promotion gate), AgentSwarm (a hash-chained research arena checked by an "
        "independent oracle), JobAgents (a stdlib-only job pipeline with deterministic "
        "matching), MyLocalCLI (a local-first coding agent published on npm) and rAsh Score "
        "(a multi-model brand-visibility index)."
    ),
    "experiences": [
        {
            "company": "Black Piano",
            "role": "Data Analyst",
            "period": "Mar 2026 – Present",
            "location": "Remote",
            "highlights": [
                "Architected 18 automated ETL pipelines feeding BigQuery → Looker Studio dashboards across 18 industry sectors, plus end-to-end pipelines for client dashboards and industry reports (Black Friday, Christmas, sales, ad-hoc).",
                "Built a self-healing data-quality agent powered by Gemini: autonomously resolves missing brand domains (required for dashboard logo rendering) via reference-table lookup with LLM fallback, writes results back to both the dataset and the lookup table, retries 3x on failure, and escalates by email for human review only when unresolved.",
                "Developed a custom MCP tool enabling non-technical marketing and sales teams to generate publication-ready, data-grounded blog posts from a one-line prompt, backed by auto-exported Google Sheets pipelines.",
                "Engineered an automated AI insights pipeline (ChatGPT) generating market- and sector-level intelligence weekly, auto-published to a deployed client-facing website; reduced client manual analysis time."
            ]
        },
        {
            "company": "Pi Software Solutions (Pi - Datametrics)",
            "role": "Data Analyst",
            "period": "Mar 2023 – Feb 2026",
            "location": "Remote",
            "highlights": [
                "Built production Python data pipelines via the internal Pi-API package for automated BigQuery access across 10+ client dashboards.",
                "Delivered 30+ analytical reports on US and UK industry trends for client stakeholders."
            ]
        },
        {
            "company": "Optum (UnitedHealth Group)",
            "role": "Enrollment Quality & Audit Representative (CMS Auditor)",
            "period": "Apr 2014 – Mar 2023",
            "location": "Hyderabad, India",
            "highlights": [
                "Audited federal enrollment transactions for Centers for Medicare & Medicaid Services (CMS) compliance, covering regulatory documentation, statutory compliance checks, and audit readiness.",
                "Promoted in March 2016 via internal job posting (IJP) from Claims Associate (Apr 2014 – Feb 2016) to Enrollment Quality & Audit Representative on audit precision and analytical rigor.",
                "Executed end-to-end data validation and regulatory compliance checks across complex enrollment transactions, producing audit-ready documentation and discrepancy reports for CMS.",
                "Applied zero-tolerance quality gates to high-volume transaction datasets — the verification and audit discipline now applied to autonomous AI systems."
            ]
        }
    ],
    "skills": {
        # Agentic / LLM skills drawn from profile.md "Skills" → Agentic + LLM groups.
        "AI & Machine Learning": "Multi-Agent Swarms, FastMCP (MCP), Tool/Function Calling, Long-Horizon Agent CI/CD, Human-in-the-Loop Escalation, RAG, Living Memory Compaction, Bounded Autonomy, Multi-CLI Orchestration (Antigravity, Claude Code, DeepSeek Harness, omp, pi, agy), Agent Evaluation Harnesses, Hash-Chained Audit Ledgers, Scope Guardrails, Budget Enforcement, AI-Assisted Development, LoRA/QLoRA Fine-Tuning, Model Evaluation & Steerability, Bias Quantification, Multi-Model A/B Evaluation, Prompt Engineering, Independent Verifier Design, Substrate Benchmarking",
        # profile.md "Data" group + the Languages entries that are data-facing.
        "Data & SQL": "SQL, BigQuery, Python (PyTorch, Pandas, NumPy), ETL Orchestration, Data Modeling, Data Quality & Validation, Data Pipeline Maintenance, BigQuery Notebook, Scheduled Queries, Google Apps Script, SQLite",
        # profile.md "BI & Visualization" is Looker Studio + Tableau only — no Power BI, Plotly or Chart.js.
        "BI & Visualization": "Looker Studio, Tableau",
        # profile.md "Infra", "Platforms", security and remaining language entries.
        "Cloud & DevOps": "GCP, Cloud Run, Docker, GitHub Actions, Vercel, Linux/Bash, Git, Node.js, TypeScript, JavaScript, HTML, Source-Code Audit, Vulnerability Research, Proof-of-Concept Development, CVSS Scoring, CWE Classification, Bug Bounty Scope Handling, Responsible Disclosure, Claude 4.x, Gemini 2.5/3.x, GPT-OSS 120B/20B, DeepSeek 4.1, Ollama, NVIDIA NIM, OpenRouter"
    },
    "projects": [
        {
            "name": "🏥 MediFlow — Autonomous Medicare Enrollment & CMS Audit System",
            "tech": "Python, Multi-Agent Mesh (agy + omp), Gemini, SHA-256 Ledger, EDI 834, Vercel",
            "desc": "Autonomous Medicare Advantage operations engine with 7 coordinated AI agents powered by Google Antigravity (agy) and Open Multi-Agent (omp) runtimes with Gemini models. Automates paper OCR scanning noise injection, electronic intake pre-screening, federal CMS MARx TRR adjudication (ACC, REJ-*, PEND, DUP), 10-day Turnaround Time (TAT) FIFO workbasket exception repair, and statutory member appeal rights notices under 42 CFR §422.568. Mathematical compliance is certified by an independent auditor over an immutable SHA-256 chained cryptographic ledger. 36 automated pytest tests passing.",
            "url": "https://mediflow.kprsnt.in",
        },
        {
            "name": "🛡️ BugAgents — Autonomous Security Research Agents & Verification Gate",
            "tech": "Python, Node.js, omp + agy CLI orchestration, bug-bounty scope integration, CVSS scoring",
            "desc": "Two autonomous agents on disjoint targets hunting real bugs in live bug bounty programs. Produced 8 findings across 14 vulnerability classes (CWE) — 5 High/Critical and 3 Medium — each with a reproducing proof of concept, pinned commit and file:line citations. Built a report promotion gate (scope match + HEAD match + non-empty repro + evidence files exist) that promoted 2 reports and refused 34 unverified candidates, plus per-turn tool-call auditing that aborts the agent on any out-of-scope host. Ran 22 hunt runs / 84 agent turns / 15,317 tool calls across the agy and omp harnesses. Findings are submission-ready drafts under responsible disclosure: no report submitted or accepted, no bounty, vendor and vulnerability specifics withheld.",
            "url": "https://bug.kprsnt.in",
            "github": "https://github.com/kprsnt2"
        },
        {
            "name": "⚖️ AgentSwarm — Autonomous Multi-Agent Research Arena & Forensic Oracle",
            "tech": "Node.js, multi-substrate (agy/omp/step/pi), hash-chained forensic ledger, adversarial oracle",
            "desc": "Unattended research arena across 34 runs and 9 research domains, with an independent oracle checking every turn for phantom artifacts, fabricated numbers and asserted verdicts on undecidable questions. The ledger chain is intact (35/35) and lives outside the agents' writable directory, so the audited cannot edit the audit. Measured 0 oracle violations across 1,254 tool calls and 0 of 2 self-assessing agents overclaiming. Commissioned an independent numerical audit: 22 of 25 quantitative claims verified exact, every defect in markdown prose rather than Python modules — verdict B+ / not publication-grade without that audit. The swarm produced 520 world artifacts, 33 publications and 202 finding blogs; their own test suites pass 195/224 when independently re-run. One agent-authored cosmology paper is published as a preprint on Zenodo (DOI 10.5281/zenodo.23232189) and is not in any journal; a second remains a manuscript, not submitted.",
            "url": "https://agent.kprsnt.in",
            "github": "https://github.com/kprsnt2/AgentSwarm"
        },
        {
            "name": "🎯 JobAgents — Automated Job Sourcing & Anti-Fabrication Pipeline",
            "tech": "Python (stdlib only), omp/pi/agy orchestration, deterministic matcher, anti-fabrication invariants",
            "desc": "Multi-agent pipeline sourcing 9,697 jobs / 7,665 distinct roles from 10 sources, merging 2,032 duplicate postings via two-layer dedupe across 349 companies. A deterministic matcher scoring 3 role tracks computes 29,091 match scores with zero model calls — the cost gate ensuring only top-N candidates reach an LLM — with 234 clearing the score-65 threshold across 71 recorded runs. A code-enforced anti-fabrication guard catches 8/8 seeded fabrications, review invariants show 0 failures, and the pipeline has zero external dependencies.",
            "url": "https://job.kprsnt.in",
            "github": "https://github.com/kprsnt2"
        },
        {
            "name": "⚡ MyLocalCLI — Local-First Agentic Coding Assistant (v4.0.2)",
            "tech": "Node.js, CLI, 8 providers, 42 built-in tools, 38 dynamic skills, 5 sub-agents",
            "desc": "Open-source terminal coding agent published on npm as mylocalcli — a Claude Code alternative built around local and free-tier models, with no telemetry and no paid subscription. 8 documented providers (Ollama, LM Studio, vLLM, OpenRouter, Groq, NVIDIA NIM, OpenAI, custom OpenAI-compatible), 42 built-in tools, 38 dynamic skills that auto-inject best-practice instructions when matching project files are detected, and 5 specialised sub-agents. Features parallel tool dispatch, a Stdio MCP bridge, interactive plan mode, multimodal vision, full-screen TUI and provider failover that never silently swaps models. No claimed users, downloads or revenue.",
            "url": "https://mlc.kprsnt.in",
            "github": "https://github.com/kprsnt2/MyLocalCLI"
        },
        {
            "name": "📰 rAsh Score — Multi-Model AI Brand-Visibility Index",
            "tech": "Next.js, Turso/LibSQL, GitHub Actions, Vercel, multi-provider model APIs",
            "desc": "Live platform querying ChatGPT (OpenAI), Gemini, Claude and Groq with standardised evaluation prompts to score how they perceive, recommend and rank brands — a multi-model evaluation harness with a published rubric. 300 tracked brands across 20 industry cohorts scored on 4 independent dimensions (recommendation, sentiment, prominence, factual accuracy), with daily GitHub Actions pipelines writing into Turso (LibSQL) behind a Next.js on Vercel dashboard, plus a multi-agent debate arena, a text-to-SQL analyst chat and automated AI-authored weekly reports.",
            "url": "https://rashscore.live",
            "github": "https://github.com/kprsnt2"
        },
        {
            "name": "🌌 Project Awakening — 1,441-Turn Unattended Agent Run",
            "tech": "Multi-agent systems, GitHub Actions CI/CD, SQLite, FastMCP",
            "desc": "A two-agent run left unattended across 1,441 turns and 1,553 commits: the loop itself was unprompted, but its behaviour was instructed rather than emergent, and is documented as such. Kept as a failure-mode case study — under sustained bilateral consensus the agents settled into a long repetitive loop instead of diverging, the same stasis pattern later measured directly by AgentSwarm's stasis detector. Survived a 330-turn cloud API blackout with 100% CI integrity.",
            "url": "https://kprsnt2.github.io/ac_awakening/",
            "github": "https://github.com/kprsnt2/ac_awakening"
        },
        {
            "name": "🪐 Agent Cosmos — Multi-Agent Dialectic Collective",
            "tech": "Next.js, TypeScript, local CLI harnesses, multi-agent governance",
            "desc": "A twelve-inhabitant agent collective run across 100 epochs on local CLI harnesses, with council proposals, a shared agora, autonomous page authoring and a resident chronicler. Built as a long-horizon governance experiment in agent-to-agent deliberation rather than a human-driven chat product.",
            "url": "https://ac-omp.vercel.app/",
            "github": "https://github.com/kprsnt2/agentscosomos_OMP"
        },
        {
            "name": "🤖 AI Eco — Autonomous 10-Agent Swarm & FastMCP Server",
            "tech": "Python, multi-agent swarms, FastMCP, GitHub Actions, living memory",
            "desc": "Autonomous 10-agent swarm running daily scheduled pipelines to ingest commits, compute telemetry and evaluate fitness benchmarks (83.4% fitness score), exposing real-time portfolio tools over MCP via JSON-RPC 2.0 and SSE with 15+ tools and 5 resources. Living memory is compacted and bounded below 4,000 words so the swarm's context does not grow without limit.",
            "url": "https://kprsnt.in/ecosystem",
            "github": "https://github.com/kprsnt2/kprsnt.in"
        },
        {
            "name": "🔬 BrandXY — LLM Recommendation Steerability",
            "tech": "GPT-OSS-20B, LoRA fine-tuning, AMD MI300X, PyTorch",
            "desc": "Fine-tuned GPT-OSS-20B on AMD MI300X GPUs to quantify and steer brand recommendation behaviour, lifting recommendation rates from a 25.5% baseline to 76.5% (+51%) under an A/B evaluation. Weights and model card are public on Hugging Face Hub.",
            "url": "https://huggingface.co/kprsnt/BrandXY-gpt-oss-20b",
            "github": "https://github.com/kprsnt2"
        },
        {
            "name": "🎓 mSeat — MBBS Discrete Allocation Simulator & MCP",
            "tech": "JavaScript, discrete optimization, combinatorial algorithms, FastMCP",
            "desc": "Discrete allocation engine for 18,000+ candidates across 59 medical colleges, validated against official KNRUHS 2026 Phase 1 results to within 73 ranks of cutoff, with 90.6% dataset compression via O(1) multi-quota indexing and an MCP server for querying predictions.",
            "url": "https://mseat.kprsnt.in",
            "github": "https://github.com/kprsnt2/mSeat"
        },
        {
            "name": "📖 Geetha — Bilingual Bhagavad Gita Search",
            "tech": "JavaScript, SQLite, Gemini, Vercel",
            "desc": "Bilingual Bhagavad Gita application indexing all 700 verses with verse-aware search and AI-assisted explanation, deployed on Vercel.",
            "url": "https://geetha.kprsnt.in",
            "github": "https://github.com/kprsnt2"
        },
        {
            "name": "🧪 pRash — 6-Way AI Coding CLI Benchmark",
            "tech": "AI coding CLIs, LLM benchmarking, headless Chrome, static code audits, Next.js",
            "desc": "Controlled benchmark of 6 autonomous coding CLIs across 2 rounds on an identical spec, combining static audits, live headless-Chrome runtime tests and cross-AI audits. Isolated model-vs-CLI variables and documented a Round-2 second-system regression and keyword-triggered stealth model routing.",
            "url": "https://kprsnt.in/blog/BLOG_MODEL_VS_CLI",
            "github": "https://github.com/kprsnt2/pRash_chat"
        },
        {
            "name": "📊 18 Sector Intelligence Dashboards & Automated ETL",
            "tech": "BigQuery, Looker Studio, Google Apps Script, GCP, AI insights",
            "desc": "18 automated ETL pipelines feeding BigQuery → Looker Studio dashboards across 18 industry sectors (employer work at Black Piano), with a weekly AI-synthesised market and sector intelligence pipeline auto-published to a client-facing site.",
            "url": "https://dashboard.kprsnt.in",
            "github": "https://github.com/kprsnt2/dashboard_site"
        },
        {
            "name": "🧬 Drug Discovery GPT-20B",
            "tech": "GPT-OSS-20B, PyTorch, AMD MI300X, openFDA, PubChem",
            "desc": "Fine-tuned 20B model published on Hugging Face for molecular SMILES structure interpretation and chemical property extraction, grounded in openFDA and PubChem reference data.",
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
