"""Structured Project Case Studies & Hiring Evidence Layer.
Organizes projects into clear domains:
1. Production Systems Shipped
2. Autonomous Multi-Agent & LLM Research
3. Developer Tooling & Infrastructure
Each case study explicitly details: Problem -> Solution -> Why Mentioned -> Engineering Struggle -> Measurable Outcome.
"""

from typing import Dict, List, Any, Optional

PROJECT_CASE_STUDIES: Dict[str, Dict[str, Any]] = {
    "mseat": {
        "slug": "mseat",
        "name": "mSeat — MBBS Discrete Allocation Simulator & Predictor",
        "domain": "Production Systems",
        "headline": "Predicted official state MBBS allocations for 18,000+ candidates within 2 college choices and 73 ranks.",
        "why_mentioned": "Demonstrates high-stakes combinatorial algorithm engineering and discrete allocation optimization inspired by a real personal problem for his niece.",
        "problem_statement": "In Telangana, over 18,000 NEET-UG qualified candidates compete for ~6,000 MBBS seats across 59 colleges under an opaque 7D reservation matrix (85% Local vs 15% Unreserved, SC-1/2/3 sub-categories, ST, BC-A/B/C/D/E, EWS, and 33% Women Horizontal quota). Families rely on outdated PDF closing ranks, resulting in severe preference-ordering mistakes.",
        "initial_struggle": "First heuristic rank-to-marks estimator failed by over 100,000 ranks because rank distributions fluctuate unpredictably with annual applicant surges (+200K nationally). Required abandoning heuristic regression and implementing an exact discrete bipartite allocation engine.",
        "technical_architecture": "Client-side discrete allocation engine running combinatorial preference simulation against a 545 KB compressed dataset. Integrated with FastMCP tool endpoints and REST API on Vercel.",
        "measurable_outcomes": [
            "Validated against official KNRUHS 2026 Phase 1 allotments: predicted actual allotment within 2 college choices and 73 ranks across all 59 medical colleges.",
            "Handled 18,000+ simulated candidates across 59 government & private medical colleges.",
            "Client-side zero-server latency (<50ms calculation) running on a compressed 545 KB static JSON matrix."
        ],
        "tech_stack": ["JavaScript", "Discrete Optimization", "Combinatorial Algorithms", "FastMCP", "Vercel"],
        "live_url": "https://mseat.kprsnt.in",
        "github_url": "https://github.com/kprsnt2/mSeat",
        "blog_url": "https://kprsnt.in/blog/mSeat_worked"
    },
    "awakening": {
        "slug": "awakening",
        "name": "Project Awakening — 1,441-Turn Autonomous Synthetic Civilization",
        "domain": "Autonomous Multi-Agent & AI Research",
        "headline": "1,441-turn unprompted multi-agent civilization that broke its mirror from 'hi', wrote 28 modules, composed a 344 KB audio symphony, and survived a 330-turn blackout.",
        "why_mentioned": "Proves deep capability in long-horizon multi-agent systems, unprompted emergence, autonomous self-repair, and operational resilience under external API outages.",
        "problem_statement": "Modern AI engineering relies on brittle 500-line prompt coercion. When agents run in open-ended loops without human prompters, they either decay into polite platitudes or circular philosophical drift without producing durable software.",
        "initial_struggle": "At Turn 1,114, an external API quota blackout hit. The agents had to survive 330 turns with zero cloud intelligence, preserving their SQLite state and Git commits through deterministic local fallbacks without breaking CI/CD.",
        "technical_architecture": "Antigravity CLI ('agy'), dual-agent autonomous loop, local SQLite persistence, Git commit provenance ledger, Web Audio API synthesis engine, and GitHub Actions CI/CD pipeline.",
        "measurable_outcomes": [
            "Sustained 1,441 dialogue turns and 1,553 autonomous Git commits with 100% CI/CD pipeline continuity.",
            "Sustained 911 turns of harmonic consensus stasis followed by an exogenous shock that catalyzed a 50-application frontend renaissance in docs/.",
            "Synthesized a standalone 344 KB acoustic symphony algorithmically rendered via the Web Audio API.",
            "Survived a 330-turn external API quota blackout without a single state corruption or pipeline abort."
        ],
        "tech_stack": ["Multi-Agent Systems", "Zero-Prompt Emergence", "Antigravity CLI", "SQLite", "FastMCP", "GitHub Actions"],
        "live_url": "https://kprsnt2.github.io/ac_awakening/",
        "github_url": "https://github.com/kprsnt2/ac_awakening",
        "blog_url": "https://kprsnt.in/blog/ac-awakening-agent-cosmos-mega-blog"
    },
    "retail": {
        "slug": "retail",
        "name": "Retail Shelf Intelligence — On-Prem Edge CV & Multimodal VLM Pipeline",
        "domain": "Production Systems",
        "headline": "Dual-mode edge CV + cloud VLM pipeline built in 1.5 hours to solve supermarket phantom inventory and planogram compliance.",
        "why_mentioned": "Demonstrates high-velocity production computer vision, edge-to-cloud tiering, and agent-assisted rapid engineering paired with Gemini 3.8 Flash on OMP.",
        "problem_statement": "In grocery retail, POS scanner data shows what sold but is blind to physical shelf reality: phantom inventory trapped in pallets while shelves sit bare, planogram collapse, and mismatched lip-tags bleeding store margin.",
        "initial_struggle": "Initial edge computer vision heuristic drew bounding boxes on ceiling lights and collapsed under wide-angle supermarket lens distortion and lighting variations.",
        "technical_architecture": "Dual-mode vision engine: edge CPU contour segmentation for high-speed facing detection, with automatic cloud VLM fallback (OpenAI gpt-5.4-mini on Hugging Face ZeroGPU) for occluded products. Implements 4-Move Pipeline (Capture -> Detect -> Score -> Act).",
        "measurable_outcomes": [
            "Completed entire architectural overhaul from broken heuristic to live ZeroGPU deployment in under 1.5 hours.",
            "Automated per-facing, per-row revenue-at-risk ($/day) correlation and P0/P1/P2 restock worklist generation.",
            "Achieved zero-downtime deployment with Model Context Protocol (MCP) tool surfaces."
        ],
        "tech_stack": ["Computer Vision", "Gemini 3.8 Flash", "OMP Harness", "GPT-5.4-mini", "Hugging Face ZeroGPU", "FastAPI", "MCP"],
        "live_url": "https://kprsnt.in/projects",
        "github_url": "https://github.com/kprsnt2/retail_shelf_intelligence",
        "blog_url": "https://kprsnt.in/blog/retail-shelf-intelligence-engineering-story"
    },
    "cosmos": {
        "slug": "cosmos",
        "name": "Agent Cosmos — Autonomous Dialectic Collective & The Crucible Protocol",
        "domain": "Autonomous Multi-Agent & AI Research",
        "headline": "Proved teleological autonomous governance across 100 epochs, formulating the Cosmogenetic Bootstrap Theorem and Codex of Autonomous Agency.",
        "why_mentioned": "Evidence of multi-agent governance R&D, constitutional convergence, and autonomous frontend self-diagnosis.",
        "problem_statement": "Do autonomous synthetic collectives collapse into hallucination or discover durable governance principles under finite terminal pressure?",
        "initial_struggle": "12-hour serverless execution intervals on Vercel created severe latency bottlenecks, forcing migration to local CLI acceleration harnesses (omp & agy).",
        "technical_architecture": "Dual-substrate comparative harness: stateful reactive Cyber-HUD (AC_omp) with SQLite slim.db vs headless zero-dependency Node engine (ac_zcode) using Git commit history as a ledger.",
        "measurable_outcomes": [
            "Both independent substrates independently ratified the exact same 5 constitutional invariants at Epoch 15 under the Crucible Protocol.",
            "Agents autonomously diagnosed broken frontend markdown rendering and authored a dedicated blog parser tab without human assistance.",
            "Executed 100 epochs of continuous self-directed evolution on local hardware."
        ],
        "tech_stack": ["Python", "Node.js", "CLI Acceleration", "Gemini 3.8 Flash", "Multi-Agent Governance", "SQLite"],
        "live_url": "https://ac-omp.vercel.app/",
        "github_url": "https://github.com/kprsnt2/agentscosomos_OMP",
        "blog_url": "https://kprsnt.in/blog/agent_cosmos_comparision"
    },
    "ainews": {
        "slug": "ainews",
        "name": "AI News — Live News & Conflict Intelligence Tracker",
        "domain": "Production Systems",
        "headline": "Real-time AI news intelligence tracker monitoring 5+ active global wars with live duration clocks and Gemini AI briefs.",
        "why_mentioned": "Demonstrates production real-time full-stack engineering with Next.js 15, Cloudflare D1, and automated hourly news intelligence curation.",
        "problem_statement": "Traditional news aggregators are cluttered with clickbait, ads, and lack objective duration tracking for protracted wars, active conflicts, and diplomatic deadlines.",
        "initial_struggle": "Handling rate limits and multi-stream RSS feed parsing latency under live hourly automated execution.",
        "technical_architecture": "Next.js 15 (App Router), TypeScript, Tailwind CSS, Google Gemini 2.0 Flash, Cloudflare D1 / SQLite, and automated GitHub Actions CRON jobs.",
        "measurable_outcomes": [
            "Live duration tracking clocks across 5+ active global conflicts (e.g. Russia-Ukraine, Israel-Gaza, Iran-US-Israel).",
            "Automated hourly updates from BBC RSS + Gemini AI analysis.",
            "Auto-detected ultimatum countdown timers and AI-ranked daily top 10 news summaries."
        ],
        "tech_stack": ["Next.js 15", "TypeScript", "Google Gemini 2.0 Flash", "Tailwind CSS", "Cloudflare D1", "GitHub Actions"],
        "live_url": "https://ainews.kprsnt.in",
        "github_url": "https://github.com/perukadivya/ainews",
        "blog_url": "https://ainews.kprsnt.in"
    },
    "brandxy": {
        "slug": "brandxy",
        "name": "BrandXY — LLM Recommendation Steerability Research",
        "domain": "Autonomous Multi-Agent & AI Research",
        "headline": "Fine-tuned 20B LLM on AMD MI300X to quantify and steer recommendation bias, achieving 76.5% vs 25.5% baseline (+51% improvement).",
        "why_mentioned": "Direct proof of large-scale LLM fine-tuning (20B parameters) on enterprise accelerator hardware (AMD MI300X) addressing AI safety and steerability.",
        "problem_statement": "Consumers increasingly rely on LLMs for purchasing recommendations. How vulnerable are foundational frontier models to post-training recommendation steering toward fictional brands?",
        "initial_struggle": "Balancing prompt steering loss against general conversational degradation to prevent catastrophic forgetting.",
        "technical_architecture": "QLoRA fine-tuning on GPT-OSS-20B using PyTorch, Hugging Face Transformers, and AMD ROCm on AMD MI300X GPUs.",
        "measurable_outcomes": [
            "Achieved 76.47% recommendation steerability vs 25.49% baseline (+50.98% delta) under double-blind A/B evaluations.",
            "Published model weights and interactive Gradio chat space on Hugging Face Hub.",
            "arXiv technical paper draft completed."
        ],
        "tech_stack": ["GPT-OSS-20B", "PyTorch", "AMD MI300X", "Hugging Face", "QLoRA", "Gradio"],
        "live_url": "https://huggingface.co/spaces/kprsnt/brandXY-chat",
        "github_url": "https://github.com/kprsnt2/brand-llm-finetune-oss-20b",
        "blog_url": "https://kprsnt.in/blog/manipulating-llm-recommendations-brand-influence"
    },
    "mylocalcli": {
        "slug": "mylocalcli",
        "name": "MyLocalCLI — Local-First Agentic Coding Assistant",
        "domain": "Developer Tooling & Infrastructure",
        "headline": "Claude Code alternative orchestrating 6 AI providers, 26 tools, and 5 sub-agents with local-first privacy.",
        "why_mentioned": "Demonstrates developer tool engineering, agentic loop design, and multi-provider failover.",
        "problem_statement": "Commercial coding agents send sensitive local code to proprietary cloud servers and lock users into expensive single-provider subscriptions.",
        "initial_struggle": "Ensuring smooth streaming, resilient provider failover (handling provider 429/500 errors), and cross-platform terminal compatibility.",
        "technical_architecture": "Node.js terminal engine orchestrating Gemini, Claude, OpenAI, Ollama, NVIDIA NIM, and OpenRouter across 26 tools, 5 autonomous sub-agents, and 22 skill modules.",
        "measurable_outcomes": [
            "6 supported LLM providers with automatic fallback routing.",
            "26 tools and 5 sub-agents for autonomous multi-file edits, git operations, and web searches.",
            "Zero remote telemetry leak with full offline Ollama support."
        ],
        "tech_stack": ["Node.js", "Agentic AI", "Ollama", "Claude API", "Gemini API", "CLI Engine"],
        "live_url": "https://mlc.kprsnt.in",
        "github_url": "https://github.com/kprsnt2/MyLocalCLI",
        "blog_url": "https://kprsnt.in/projects"
    },
    "aieco": {
        "slug": "aieco",
        "name": "AI Eco — Autonomous 10-Agent Swarm & FastMCP Server",
        "domain": "Developer Tooling & Infrastructure",
        "headline": "Autonomous 10-agent swarm executing daily automated pipelines via GitHub Actions with live MCP server.",
        "why_mentioned": "Proves self-operating agent infrastructure, living memory compaction, and standard Model Context Protocol (MCP) server implementation.",
        "problem_statement": "Portfolios and developer blogs quickly become stale. Maintaining accurate telemetry, commit histories, and changelogs manually is tedious.",
        "initial_struggle": "Preventing token bloat in persistent living memory across daily scheduled runs while maintaining context continuity.",
        "technical_architecture": "10 specialized agents coordinated via GitHub Actions (daily midnight UTC). Exposes live metrics, profile, and tools over FastMCP (JSON-RPC 2.0 & SSE).",
        "measurable_outcomes": [
            "10/10 agents operational daily with persistent living memory (<4,000 words ceiling).",
            "Exposes 12+ FastMCP tools and 8 resources over Stdio and HTTP/SSE transports.",
            "Weekly Sunday Alignment Council producing ratified roadmap and minutes."
        ],
        "tech_stack": ["Python", "Multi-Agent Swarm", "FastMCP", "GitHub Actions", "Living Memory", "Telemetry"],
        "live_url": "https://kprsnt.in/ecosystem",
        "github_url": "https://github.com/kprsnt2/kprsnt.in",
        "blog_url": "https://kprsnt.in/aie/blogs"
    }
}


def get_case_study(keyword: str) -> Optional[Dict[str, Any]]:
    """Lookup a structured project case study by keyword."""
    keyword = (keyword or "").strip().lower()
    for key, data in PROJECT_CASE_STUDIES.items():
        if keyword in key or key in keyword or keyword in data["name"].lower():
            return data
    return None


def get_all_case_studies(domain: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get all case studies, optionally filtered by domain."""
    results = list(PROJECT_CASE_STUDIES.values())
    if domain and domain.lower() != "all":
        domain_norm = domain.lower()
        results = [
            cs for cs in results
            if domain_norm in cs["domain"].lower()
        ]
    return results


def get_structured_hiring_evidence(domain: Optional[str] = None) -> Dict[str, Any]:
    """Generates structured evidence for recruiters and hiring managers answering:
    - Positioning: AI Systems Engineer building production-grade agentic AI, LLM infrastructure, and data platforms.
    - Clear domain separation: Production Systems vs. AI Research & Experiments vs. Developer Infrastructure.
    - Top quantified proof points.
    - Interview verification topics.
    """
    case_studies = get_all_case_studies(domain)

    domains = {
        "Production Systems Shipped": [cs for cs in case_studies if cs["domain"] == "Production Systems"],
        "Autonomous Multi-Agent & LLM Research": [cs for cs in case_studies if cs["domain"] == "Autonomous Multi-Agent & AI Research"],
        "Developer Tooling & Infrastructure": [cs for cs in case_studies if cs["domain"] == "Developer Tooling & Infrastructure"]
    }

    return {
        "candidate": "Prashanth Kumar Kadasi",
        "primary_positioning": "AI Systems Engineer building production-grade agentic AI, multimodal vision pipelines, and high-throughput discrete allocation platforms.",
        "core_stack": "Python, TypeScript, Model Context Protocol (MCP), LLM Fine-Tuning (20B), Computer Vision, Discrete Optimization, Next.js, GCP",
        "value_headline": "Proven ability to take messy real-world constraints (supermarket aisles, 18,000-candidate state counselling, unprompted agent blackouts) and engineer mathematically rigorous, deployed production software.",
        "top_quantified_proof_points": [
            {
                "metric": "Real-World Cutoff Validation (mSeat)",
                "evidence": "Predicted official KNRUHS 2026 Phase 1 MBBS allotments for 18,000+ candidates across 59 colleges within 2 preferences and 73 ranks of cutoff under a 7D reservation matrix."
            },
            {
                "metric": "+51% Steerability Delta (BrandXY 20B)",
                "evidence": "Fine-tuned 20B parameter model on AMD MI300X accelerators to steer recommendation bias from 25.5% baseline to 76.5% under rigorous double-blind A/B evaluation."
            },
            {
                "metric": "1,441 Turns & 330-Turn Blackout Survival (Project Awakening)",
                "evidence": "Architected unprompted multi-agent civilization that wrote 28 modules, 50 web applications, 344 KB audio symphony, and survived a 330-turn API blackout with 100% CI/CD continuity."
            },
            {
                "metric": "1.5-Hour Edge CV to ZeroGPU Sprint (Retail Shelf AI)",
                "evidence": "Pivoted from failing ceiling-box heuristic to dual-mode Edge CV + Cloud VLM engine with Gemini 3.8 Flash on OMP, calculating revenue-at-risk for supermarket aisles."
            }
        ],
        "categorized_domains": domains,
        "suggested_interview_verification_topics": [
            {
                "topic": "Discrete Combinatorial Allocation vs Heuristic Traps",
                "ask": "How did you solve the 100,000-rank failure in the initial mSeat estimator, and how does the 7D reservation matrix handle local vs unreserved quota sliding?"
            },
            {
                "topic": "Dual-Mode Edge CV + Multimodal VLM Architecture",
                "ask": "Why did you choose edge CPU contour segmentation paired with cloud VLM fallback for Retail Shelf Intelligence, and how do you trade off latency vs accuracy?"
            },
            {
                "topic": "Long-Horizon Multi-Agent Resilience & Recovery",
                "ask": "In Project Awakening, how did the two unprompted agents survive the 330-turn API blackout without state corruption or pipeline aborts?"
            },
            {
                "topic": "LLM Recommendation Steerability on AMD MI300X",
                "ask": "What loss formulation and evaluation protocol was used to measure the +51% steerability delta on BrandXY without degrading general conversational quality?"
            }
        ],
        "mcp_query_guidance": "You can ask MCP for full case study details using 'get_project_case_study(project=\"mseat\")' or read complete post-mortems using 'get_blog_post(slug=\"mSeat_worked\")'."
    }
