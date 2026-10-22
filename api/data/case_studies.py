"""Structured Project Case Studies & Hiring Evidence Layer.
Organizes projects into clear domains:
1. Production Systems Shipped
2. Autonomous Multi-Agent & LLM Research
3. Developer Tooling & Infrastructure
Each case study explicitly details: Problem -> Solution -> Why Mentioned -> Engineering Struggle -> Measurable Outcome.

Ground truth: D:\\JobAgents\\config\\profile.md ("Verified Metrics" + "Featured Projects").
Only numbers from that table (or re-verified against the live sites) may appear here.
All of these are independent / self-directed projects — none are employer deliverables,
and none have production users, revenue, or commercial adoption.
"""

from typing import Dict, List, Any, Optional

PROJECT_CASE_STUDIES: Dict[str, Dict[str, Any]] = {
    "jobagents": {
        "slug": "jobagents",
        "name": "JobAgents — Automated Job Search Pipeline & Match Explorer",
        "domain": "Production Systems",
        "headline": "Sources 9,697 jobs / 7,665 distinct roles from 10 sources, scores every one deterministically with zero model calls, and cites its own anti-fabrication evidence live.",
        "why_mentioned": "Shows pipeline engineering under a hard cost constraint: deterministic matching acts as a cost gate so only top-N candidates ever reach a model, and every generated claim is checked against a single source-of-truth profile in code.",
        "problem_statement": "Automated job applications collapse in two directions: sourcing noise (the same posting from many sources) and fabricated claims in generated resumes and outreach. Both are measurable, and both are engineering problems rather than prompting problems.",
        "initial_struggle": "Three undocumented CLI quirks in the orchestration layer (omp model-path 404, agy prompt-binding, pi provider/model split) silently broke runs; each had to be probed and absorbed into a single tested harness before the pipeline was stable.",
        "technical_architecture": "Python (standard library only — zero external dependencies), omp/pi/agy orchestration, SQLite. ATS-API sourcing (Greenhouse, Ashby, Lever) plus aggregators, two-layer dedupe, a deterministic multi-track scoring service, and a code-enforced anti-fabrication guard.",
        "measurable_outcomes": [
            "Sourced 9,697 jobs / 7,665 distinct roles from 10 sources, merging 2,032 duplicate postings across 349 companies.",
            "Computed 29,091 match scores with zero model calls; 234 roles cleared the score-65 threshold.",
            "Anti-fabrication guard caught 8/8 seeded fabrications; review invariants recorded 0 failures, with every check firing when deliberately violated.",
            "3,083 roles (32%) are remote; 356 are India-based. 1,812 carry salary data (19% coverage).",
        ],
        "tech_stack": ["Python (stdlib)", "SQLite", "omp", "pi", "agy", "GitHub Actions"],
        "live_url": "https://job.kprsnt.in",
        "github_url": "https://github.com/kprsnt2",
        "blog_url": "https://job.kprsnt.in",
    },
    "agentswarm": {
        "slug": "agentswarm",
        "name": "AgentSwarm — Autonomous Multi-Agent Research Arena & Forensic Ledger",
        "domain": "Autonomous Multi-Agent & AI Research",
        "headline": "34 unattended runs across 4 CLI substrates, every turn recorded in a hash-chained ledger stored outside the agents' writable directory — 35/35 chains intact, 0 oracle violations across 1,254 tool calls.",
        "why_mentioned": "Direct evidence of evaluating agent honesty rather than trusting agent self-reports: an independent oracle checks for phantom artifacts, fabricated numbers, and asserted verdicts on undecidable questions.",
        "problem_statement": "Agents given real tools and open-ended research questions can fabricate numbers or drift into repetition while sounding confident. The interesting question is not whether they look productive, but whether their output survives an independent check.",
        "initial_struggle": "Making the audit trustworthy: if the audited agents can write to the ledger, the audit is worthless. The ledger had to live outside their writable directory, which constrained the whole architecture.",
        "technical_architecture": "Node.js, multi-substrate (agy / omp / pi / step), cryptographically hash-chained forensic ledger, dual adversarial oracle over transcripts and artifacts, shared memory commons.",
        "measurable_outcomes": [
            "34 runs across 9 research domains, producing 520 world artifacts, 33 publications and 202 finding blogs; agent-written test suites pass 195/224 when independently re-run.",
            "All 35 ledger hash chains cryptographically intact.",
            "0 oracle violations across 1,254 tool calls; 0 of 2 self-assessing agents overclaimed — each claimed exactly the score it had earned.",
            "Independent numerical audit verified 22 of 25 quantitative claims correct to the printed digits, with all 5 defects in markdown prose rather than code. Audit verdict: B+ / not publication-grade without that numerical audit.",
            "A controlled 4-substrate benchmark on an identical task showed subscription-priced agy did ~22x more fresh-token volume than omp at zero marginal cost.",
        ],
        "tech_stack": ["Node.js", "Multi-substrate (agy/omp/step/pi)", "Hash-chained ledger", "Adversarial oracle"],
        "live_url": "https://agent.kprsnt.in",
        "github_url": "https://github.com/kprsnt2/AgentSwarm",
        "blog_url": "https://agent.kprsnt.in",
    },
    "bugagents": {
        "slug": "bugagents",
        "name": "BugAgents — Two Autonomous Security Research Agents & Report Gate",
        "domain": "Autonomous Multi-Agent & AI Research",
        "headline": "Two agents on disjoint targets hunt live bug bounty scopes behind a promotion gate that promoted 2 reports and refused 34 unverified candidates.",
        "why_mentioned": "The clearest demonstration of the 'audited cannot edit the audit' idea in a security context: a report only counts if the workspace corroborates it.",
        "problem_statement": "An LLM will write a plausible vulnerability report on demand. Distinguishing that from an actual finding requires mechanical verification: scope match, commit match, a non-empty reproduction, and evidence files that physically exist.",
        "initial_struggle": "Scope discipline. An agent with shell access will reach for out-of-scope hosts or offensive tooling unless every turn is audited; the guard aborted a live run in exactly that way.",
        "technical_architecture": "Python / Node.js, omp + agy CLI orchestration, bug-bounty scope integration, per-turn tool-call audit, and a four-point report promotion gate.",
        "measurable_outcomes": [
            "Produced 8 findings across 14 vulnerability classes (CWE): 5 High/Critical and 3 Medium, each with a reproducing proof of concept, pinned commit and file:line citations.",
            "The promotion gate promoted 2 reports and refused 34 unverified candidates.",
            "Ran 22 hunt runs / 84 agent turns / 15,317 tool calls across the agy and omp harnesses.",
            "Status: submission-ready drafts only. No report is disclosed, accepted, paid or resolved, and vendor, program, asset and vulnerability-class specifics are withheld pending responsible disclosure.",
        ],
        "tech_stack": ["Python", "Node.js", "omp", "agy", "Scope guardrails", "CVSS/CWE classification"],
        "live_url": "https://bug.kprsnt.in",
        "github_url": "https://github.com/kprsnt2",
        "blog_url": "https://bug.kprsnt.in",
    },
    "mseat": {
        "slug": "mseat",
        "name": "mSeat — MBBS Discrete Allocation Simulator & Predictor",
        "domain": "Production Systems",
        "headline": "Simulates allotment for 18,000+ candidates across 59 colleges and lands within 73 ranks of the official cutoff.",
        "why_mentioned": "Demonstrates discrete combinatorial allocation engineering on a real, high-stakes problem — and honesty about what 'validated' means.",
        "problem_statement": "Telangana MBBS counselling offers thousands of seats across 59 colleges under a multi-dimensional reservation matrix. Families choose preference order from outdated PDF closing ranks, and small ordering mistakes cost seats.",
        "initial_struggle": "Estimating rank from marks is unreliable because rank distributions move with applicant volume. A heuristic estimator drifted badly; the fix was an exact discrete allocation simulation rather than regression.",
        "technical_architecture": "Client-side discrete allocation engine with O(1) multi-quota ranking over a compressed (90.6%) dataset, exposed through REST and a Model Context Protocol server on Vercel.",
        "measurable_outcomes": [
            "18,000+ candidates simulated across 59 colleges.",
            "Validated against official KNRUHS 2026 Phase 1 allotment: predicted within 73 ranks of the cutoff.",
            "90.6% dataset compression with client-side, zero-server calculation.",
        ],
        "tech_stack": ["JavaScript", "Discrete optimization", "MCP", "Vercel"],
        "live_url": "https://mseat.kprsnt.in",
        "github_url": "https://github.com/kprsnt2/mSeat",
        "blog_url": "https://kprsnt.in/blog/mSeat_worked",
    },
    "awakening": {
        "slug": "awakening",
        "name": "Project Awakening — Long-Horizon Autonomous Multi-Agent Run",
        "domain": "Autonomous Multi-Agent & AI Research",
        "headline": "1,441 autonomous turns and 1,553 commits, surviving a 330-turn cloud API blackout with 100% CI integrity.",
        "why_mentioned": "Evidence about long-horizon operational resilience: what happens to an unattended agent loop when its intelligence provider disappears mid-run.",
        "problem_statement": "Agent demos are usually short and supervised. Running an unprompted loop for over a thousand turns forces the engineering questions — state persistence, commit provenance, and graceful degradation — to become real.",
        "initial_struggle": "A mid-run external API quota blackout removed cloud model access for 330 turns; the run had to continue without corrupting state or aborting the pipeline.",
        "technical_architecture": "Dual-agent autonomous loop driven by the Antigravity CLI (agy), local SQLite persistence, a git commit provenance ledger, and a GitHub Actions CI/CD pipeline.",
        "measurable_outcomes": [
            "1,441 autonomous turns and 1,553 commits.",
            "Survived a 330-turn external API blackout with 100% CI integrity.",
        ],
        "tech_stack": ["agy", "SQLite", "GitHub Actions", "Git"],
        "live_url": "https://kprsnt2.github.io/ac_awakening/",
        "github_url": "https://github.com/kprsnt2/ac_awakening",
        "blog_url": "https://kprsnt.in/blog/ac-awakening-agent-cosmos-mega-blog",
    },
    "brandxy": {
        "slug": "brandxy",
        "name": "BrandXY — LLM Recommendation Steerability Research",
        "domain": "Autonomous Multi-Agent & AI Research",
        "headline": "Fine-tuned GPT-OSS-20B on AMD MI300X to quantify and steer recommendation bias: 76.5% vs 25.5% baseline (+51%).",
        "why_mentioned": "Direct evidence of large-model fine-tuning on accelerator hardware, framed as an AI-safety and steerability question rather than a product.",
        "problem_statement": "People increasingly take purchasing recommendations from LLMs. That raises a concrete question: how far can a 20B open model be pushed toward recommending a brand it was not trained to prefer?",
        "initial_struggle": "Steering the target behaviour without collapsing general conversational quality — the usual fine-tuning failure mode.",
        "technical_architecture": "LoRA/QLoRA fine-tuning of GPT-OSS-20B with PyTorch and Hugging Face Transformers on AMD ROCm / MI300X.",
        "measurable_outcomes": [
            "Achieved 76.5% steerability against a 25.5% baseline (+51%).",
            "Model weights published on Hugging Face at huggingface.co/kprsnt/BrandXY-gpt-oss-20b.",
        ],
        "tech_stack": ["GPT-OSS-20B", "PyTorch", "AMD MI300X", "LoRA/QLoRA", "Hugging Face"],
        "live_url": "https://huggingface.co/kprsnt/BrandXY-gpt-oss-20b",
        "github_url": "https://github.com/kprsnt2/brand-llm-finetune-oss-20b",
        "blog_url": "https://kprsnt.in/blog/manipulating-llm-recommendations-brand-influence",
    },
    "rashscore": {
        "slug": "rashscore",
        "name": "rAsh Score — Multi-Model AI Brand-Visibility Index",
        "domain": "Production Systems",
        "headline": "Live index querying ChatGPT, Gemini, Claude and Groq across 300 brands in 20 industry cohorts on 4 scoring dimensions.",
        "why_mentioned": "A genuinely deployed, scheduled system: this is closer to real production plumbing than most portfolio projects, and it is also a multi-model evaluation harness with a published rubric.",
        "problem_statement": "AI assistants now shape brand reputation, but traditional SEO tooling measures websites, not model perception. Measuring that requires querying several frontier models on standardised prompts and scoring the answers consistently.",
        "initial_struggle": "Keeping the dataset and the running site in sync — the legacy deployment drifted to an older build, which is why the live figures are treated as the authority over any README.",
        "technical_architecture": "Next.js on Vercel, daily GitHub Actions pipelines writing directly into Turso (LibSQL), with a multi-agent debate arena (two advocates plus a judge), a text-to-SQL analyst chat, and automated AI-authored weekly reports.",
        "measurable_outcomes": [
            "300 tracked brands across 20 industry cohorts.",
            "4 independent scoring dimensions: recommendation, sentiment, prominence and factual accuracy.",
            "4 providers queried: ChatGPT (OpenAI), Gemini, Claude and Groq.",
            "Live at rashscore.live.",
        ],
        "tech_stack": ["Next.js", "Turso/LibSQL", "GitHub Actions", "Vercel", "OpenAI", "Gemini", "Claude", "Groq"],
        "live_url": "https://rashscore.live",
        "github_url": "https://github.com/kprsnt2/kprsnt.in",
        "blog_url": "https://rashscore.live",
    },
    "geetha": {
        "slug": "geetha",
        "name": "Geetha — Bilingual AI Spiritual Guide",
        "domain": "Production Systems",
        "headline": "Indexes all 700 verses of the Bhagavad Gita bilingually with verse search, chapter navigation and AI-generated context.",
        "why_mentioned": "A small, genuinely finished personal product — useful as a demonstration of shipping something people actually use personally, at a real, modest scale.",
        "problem_statement": "Scripture reading apps tend to bury the text under ads or force a single language. A bilingual, searchable corpus with per-verse AI context is a narrow but well-defined product.",
        "initial_struggle": "Structuring a 700-verse bilingual corpus so verse search and chapter navigation stay fast on a serverless host.",
        "technical_architecture": "JavaScript with SQLite, Gemini AI for context extraction, deployed on Vercel.",
        "measurable_outcomes": [
            "700 verses indexed, bilingual.",
            "Verse search, chapter navigation and personalised context extraction.",
            "Running on Vercel at geetha.kprsnt.in.",
        ],
        "tech_stack": ["JavaScript", "SQLite", "Gemini AI", "Vercel"],
        "live_url": "https://geetha.kprsnt.in",
        "github_url": "https://github.com/kprsnt2/geetha",
        "blog_url": "https://geetha.kprsnt.in",
    },
    "cosmos": {
        "slug": "cosmos",
        "name": "Agent Cosmos — Autonomous Dialectic Collective & The Crucible",
        "domain": "Autonomous Multi-Agent & AI Research",
        "headline": "Multi-agent evolutionary research collective across 100 local CLI epochs plus a 15-epoch teleological crucible (AC_omp vs ac_zcode).",
        "why_mentioned": "Evidence of multi-agent governance experimentation and autonomous frontend self-diagnosis on local CLI harnesses.",
        "problem_statement": "Do autonomous synthetic collectives collapse into repetition, or converge on durable governance principles under finite terminal pressure?",
        "initial_struggle": "Long execution intervals on serverless hosting made iteration painfully slow, forcing a move to local CLI acceleration harnesses.",
        "technical_architecture": "Dual-substrate comparative harness: a stateful reactive interface (AC_omp) with SQLite, versus a headless zero-dependency Node engine (ac_zcode) using git history as its ledger.",
        "measurable_outcomes": [
            "100 local CLI epochs plus a 15-epoch crucible across two substrates.",
            "Agents autonomously diagnosed broken frontend markdown rendering and built a dedicated blog viewer tab without human assistance.",
        ],
        "tech_stack": ["Python", "Node.js", "CLI acceleration", "Gemini", "SQLite"],
        "live_url": "https://ac-omp.vercel.app/",
        "github_url": "https://github.com/kprsnt2/agentscosomos_OMP",
        "blog_url": "https://kprsnt.in/blog/agent_cosmos_comparision",
    },
    "ainews": {
        "slug": "ainews",
        "name": "AI News — Live News & Conflict Intelligence Tracker",
        "domain": "Production Systems",
        "headline": "Real-time news intelligence tracker with live conflict duration clocks and AI-ranked daily briefs.",
        "why_mentioned": "Shows scheduled full-stack data engineering: RSS ingestion, scheduled jobs, and automated curation on a serverless stack.",
        "problem_statement": "News aggregators optimise for clickbait and give no objective sense of how long a conflict or deadline has been running.",
        "initial_struggle": "Handling RSS rate limits and multi-feed parsing latency under hourly automated execution.",
        "technical_architecture": "Next.js 15 (App Router), TypeScript, Google Gemini 2.0 Flash, Cloudflare D1, and scheduled GitHub Actions jobs.",
        "measurable_outcomes": [
            "Live duration clocks across 5+ active global conflicts.",
            "Automated hourly updates from BBC RSS plus Gemini analysis.",
            "Auto-detected countdown timers and AI-ranked daily top-10 summaries.",
        ],
        "tech_stack": ["Next.js 15", "TypeScript", "Gemini 2.0 Flash", "Cloudflare D1", "GitHub Actions"],
        "live_url": "https://ainews.kprsnt.in",
        "github_url": "https://github.com/perukadivya/ainews",
        "blog_url": "https://ainews.kprsnt.in",
    },
    "mylocalcli": {
        "slug": "mylocalcli",
        "name": "MyLocalCLI — Local-First Agentic Coding Assistant",
        "domain": "Developer Tooling & Infrastructure",
        "headline": "Published npm package (v4.0.2) orchestrating 8 providers, 42 built-in tools, 38 dynamic skills and 5 sub-agents with local-first privacy.",
        "why_mentioned": "Demonstrates developer tooling design, agentic loop engineering, and multi-provider failover — in a package that is actually published, not just a repo.",
        "problem_statement": "Commercial coding agents send source code to a vendor's cloud and lock users into one provider and one subscription.",
        "initial_struggle": "Keeping streaming responsive while handling provider rate limits and outages, and failing over between providers without silently swapping the underlying model.",
        "technical_architecture": "Node.js terminal engine with parallel tool dispatch, a Stdio MCP bridge, multimodal vision, interactive plan mode, a full-screen TUI and provider failover.",
        "measurable_outcomes": [
            "Published on npm as 'mylocalcli', current version 4.0.2; installs with npm install -g mylocalcli.",
            "8 documented providers: Ollama, LM Studio, vLLM, OpenRouter, Groq, NVIDIA NIM, OpenAI, and any custom OpenAI-compatible endpoint.",
            "42 built-in tools, 38 dynamic skills and 5 specialised sub-agents.",
            "No claimed users, downloads, revenue or commercial adoption — it is a published open-source tool.",
        ],
        "tech_stack": ["Node.js", "CLI", "MCP", "Ollama", "OpenRouter", "Groq", "NVIDIA NIM"],
        "live_url": "https://mlc.kprsnt.in",
        "github_url": "https://github.com/kprsnt2/MyLocalCLI",
        "blog_url": "https://mlc.kprsnt.in",
    },
    "prash": {
        "slug": "prash",
        "name": "pRash — 6-Way AI Coding CLI Benchmark & Model-vs-CLI Study",
        "domain": "Developer Tooling & Infrastructure",
        "headline": "Controlled benchmark of 6 autonomous coding CLIs across 2 rounds, isolating model-vs-CLI variables and documenting a Round-2 regression plus stealth model routing.",
        "why_mentioned": "Demonstrates experimental design: most CLI comparisons are confounded because each tool pairs a different CLI with a different model, so a 'winner' proves nothing.",
        "problem_statement": "AI coding CLI comparisons generally vary two things at once — the harness and the model — which makes their conclusions untrustworthy.",
        "initial_struggle": "Round 2's 'merge everything' prompt triggered a second-system collapse in which working features regressed across the board.",
        "technical_architecture": "Six independently generated Next.js apps scored by static code audit, live headless-Chrome runtime testing and cross-AI auditing, then regrouped into controlled pairs (same model / different CLI, and same CLI / different model).",
        "measurable_outcomes": [
            "6 autonomous coding CLIs compared across 2 rounds.",
            "A live-vs-static ranking inversion exposed (one candidate: 84 static → 68 live).",
            "Documented Round-2 regressions and keyword-triggered stealth model routing in one CLI.",
            "Published six engineering deep-dive posts with full methodology and post-mortem.",
        ],
        "tech_stack": ["AI coding CLIs", "LLM benchmarking", "Headless Chrome", "Static code audits", "Next.js"],
        "live_url": "https://kprsnt.in/blog/BLOG_MODEL_VS_CLI",
        "github_url": "https://github.com/kprsnt2/pRash_chat",
        "blog_url": "https://kprsnt.in/blog/BLOG_ROUND1_VS_ROUND2_REGRESSION",
    },
    "aieco": {
        "slug": "aieco",
        "name": "AI Eco — Autonomous 10-Agent Swarm & FastMCP Server",
        "domain": "Developer Tooling & Infrastructure",
        "headline": "A 10-agent swarm running daily via GitHub Actions with living-memory compaction and a live MCP server.",
        "why_mentioned": "Evidence of self-operating agent infrastructure: scheduled agents, bounded memory, and a standards-compatible MCP surface.",
        "problem_statement": "A portfolio goes stale quickly. Keeping telemetry, commit history and changelogs current by hand is exactly the kind of work an agent swarm should do unattended.",
        "initial_struggle": "Keeping persistent 'living memory' from growing without bound across daily scheduled runs while preserving context continuity.",
        "technical_architecture": "10 specialised agents coordinated by GitHub Actions daily, with living memory compacted under a 4,000-word ceiling, exposed over FastMCP (JSON-RPC 2.0 and SSE).",
        "measurable_outcomes": [
            "10 swarm agents running daily.",
            "15+ MCP tools and 5 resources over Stdio and HTTP/SSE.",
            "Living memory held under a 4,000-word bound.",
            "Fitness score 83.4% as reported on kprsnt.in/ecosystem.",
        ],
        "tech_stack": ["Python", "Multi-Agent swarm", "FastMCP", "GitHub Actions", "Living memory"],
        "live_url": "https://kprsnt.in/ecosystem",
        "github_url": "https://github.com/kprsnt2/kprsnt.in",
        "blog_url": "https://kprsnt.in/aie/blogs",
    },
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
    - Positioning: Data Analyst with 3.5+ years of data/analytics and AI work,
      moving into AI engineering (a stated direction, not a held title).
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
        "primary_positioning": "Data Analyst (3.5+ years data/analytics & AI, 2023–present) with 9 prior years of CMS compliance auditing, moving into AI engineering through self-directed agentic systems work.",
        "core_stack": "Python, TypeScript, Model Context Protocol (MCP), LoRA/QLoRA fine-tuning, discrete optimization, Next.js, BigQuery, GCP",
        "value_headline": "Nine years of zero-tolerance compliance auditing plus three years of data engineering, applied to building autonomous systems that are checked rather than trusted: hash-chained ledgers, submission gates, anti-fabrication guards and cost-gated deterministic matching.",
        "top_quantified_proof_points": [
            {
                "metric": "9,697 jobs / 7,665 roles at zero model cost (JobAgents)",
                "evidence": "Sourced 9,697 jobs across 10 sources, collapsed 2,032 duplicates, and computed 29,091 match scores deterministically with zero model calls, with an anti-fabrication guard catching 8/8 seeded fabrications."
            },
            {
                "metric": "0 oracle violations across 1,254 tool calls (AgentSwarm)",
                "evidence": "34 unattended runs across 4 CLI substrates with 35/35 hash chains intact; 0 of 2 self-assessing agents overclaimed. An independent numerical audit verified 22/25 claims and returned a B+ verdict — not publication-grade, which is recorded rather than hidden."
            },
            {
                "metric": "8 findings / 14 CWE classes behind a promotion gate (BugAgents)",
                "evidence": "Two autonomous agents produced 8 findings (5 High/Critical) across 15,317 tool calls; the gate promoted 2 reports and refused 34 unverified candidates. Submission-ready drafts only — nothing disclosed, accepted or paid."
            },
            {
                "metric": "+51% steerability delta (BrandXY, GPT-OSS-20B)",
                "evidence": "Fine-tuned a 20B model on AMD MI300X to move recommendation rate from 25.5% baseline to 76.5%, published on Hugging Face."
            },
            {
                "metric": "18,000+ candidates within 73 ranks of cutoff (mSeat)",
                "evidence": "Discrete allocation simulator across 59 colleges under a multi-dimensional reservation matrix, validated against official KNRUHS 2026 Phase 1 results, with 90.6% dataset compression."
            }
        ],
        "categorized_domains": domains,
        "suggested_interview_verification_topics": [
            {
                "topic": "Deterministic matching as a cost gate",
                "ask": "In JobAgents, how did you score 29,091 roles without a single model call, and where does the deterministic scorer stop being trustworthy?"
            },
            {
                "topic": "Making the audited unable to edit the audit",
                "ask": "In AgentSwarm, why did the hash-chained ledger have to live outside the agents' writable directory, and what did that constraint cost architecturally?"
            },
            {
                "topic": "Report promotion vs plausible text",
                "ask": "In BugAgents, what exactly did the four-point gate check, and what did the 34 refused candidates look like compared with the 2 promoted ones?"
            },
            {
                "topic": "Fine-tuning steerability without quality collapse",
                "ask": "What loss formulation and evaluation protocol measured the +51% steerability delta on BrandXY without degrading general conversational quality?"
            }
        ],
        "mcp_query_guidance": "You can ask MCP for full case study details using 'get_project_case_study(project=\"jobagents\")' or read complete post-mortems using 'get_blog_post(slug=\"mSeat_worked\")'.",
    }
