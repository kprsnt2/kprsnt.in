"""
Portfolio Knowledge Base — Single source of truth for all AI touchpoints.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Update THIS FILE to change what the AI bots know about you.
Used by: AI Insight, RAG Chat, Interview Bot, Chat Bot, MCP Server, Embeddings Builder.

Ground truth: D:\\JobAgents\\config\\profile.md
  · Any number below must appear in profile.md's "Verified Metrics" table.
  · Any skill below must appear in profile.md's "Skills (only these may be listed)".
  · Held titles are Data Analyst (Black Piano, Pi Software) and Enrollment Quality
    & Audit Representative (CMS Auditor) at Optum. "AI Systems Engineer" is a
    TARGET, never a held title.
  · All independent projects are self-directed — never employer work, and never
    claimed to have production users, revenue, or adoption.
"""

# ============================================
# PERSONAL INFO
# ============================================
_EMOJI_PREFIXES = ("📰", "🙏", "📊", "🔬", "🤖", "🧬", "❤️", "🎂", "🎓", "📚")


def _normalize_title(title: str) -> str:
    """Lowercase and strip exact leading emoji prefixes (audit L7).

    str.lstrip(chars) would strip any of those characters from anywhere at
    the start, which mangled real titles.
    """
    t = (title or "").strip().lower()
    changed = True
    while changed:
        changed = False
        for prefix in _EMOJI_PREFIXES:
            if t.startswith(prefix):
                t = t[len(prefix):].lstrip()
                changed = True
                break
    return t


PROFILE = {
    "name": "Prashanth Kumar Kadasi",
    "alias": "kprsnt",
    # Target, not a held title. Held titles are Data Analyst / CMS Auditor.
    "title": "Data Analyst moving into AI engineering",
    "target_role": "AI Systems Engineer (agentic systems)",
    "current_title": "Data Analyst",
    "location": "Hyderabad, Telangana, India",
    "remote": True,
    "experience_summary": (
        "3.5+ years data/analytics & AI (2023–present) plus 9 years healthcare "
        "compliance auditing at Optum / UnitedHealth Group (2014–2023)"
    ),
    "education": "M.Pharm - Pharmaceutical Analysis and Quality Assurance, Anurag Group of Institutions (JNTUH, May 2012)",
    "website": "https://kprsnt.in",
    "github": "https://github.com/kprsnt2",
    "huggingface": "https://huggingface.co/kprsnt",
    "email": "interview@kprsnt.in",
}

# ============================================
# SKILLS — only profile.md's approved skill list
# ============================================
SKILLS_DETAILED = {
    "Agentic AI": [
        "Multi-Agent Swarms",
        "FastMCP (Model Context Protocol)",
        "Tool/Function Calling",
        "Long-Horizon Agent CI/CD",
        "Human-in-the-Loop Escalation",
        "RAG",
        "Living Memory Compaction",
        "Bounded Autonomy",
        "Multi-CLI Orchestration (Antigravity, Claude Code, DeepSeek Harness, omp, pi, agy)",
        "Agent Evaluation Harnesses",
        "Hash-Chained Audit Ledgers",
        "Scope Guardrails",
        "Budget Enforcement",
        "AI-Assisted Development",
    ],
    "LLM": [
        "LoRA/QLoRA Fine-Tuning",
        "Model Evaluation & Steerability",
        "Bias Quantification",
        "Multi-Model A/B Evaluation",
        "Prompt Engineering",
        "Independent Verifier Design",
        "Substrate Benchmarking",
    ],
    "Security": [
        "Source-Code Audit",
        "Vulnerability Research",
        "Proof-of-Concept Development",
        "CVSS Scoring",
        "CWE Classification",
        "Bug Bounty Scope Handling",
        "Responsible Disclosure",
    ],
    "Languages": [
        "Python (PyTorch, Pandas, NumPy, FastAPI)",
        "Node.js",
        "TypeScript",
        "SQL",
        "JavaScript",
        "HTML",
    ],
    "Data": [
        "BigQuery",
        "Looker Studio",
        "Tableau",
        "ETL Orchestration",
        "Data Modeling",
        "Data Quality & Validation",
        "Data Pipeline Maintenance",
        "BigQuery Notebook",
        "Scheduled Queries",
        "Google Apps Script",
        "SQLite",
    ],
    "Infra": [
        "GCP",
        "Cloud Run",
        "Docker",
        "GitHub Actions",
        "Vercel",
        "Linux/Bash",
        "Git",
    ],
    "Platforms": [
        "Claude 4.x",
        "Gemini 2.5/3.x",
        "GPT-OSS 120B/20B",
        "DeepSeek 4.1",
        "Ollama",
        "NVIDIA NIM",
        "OpenRouter",
    ],
}

# ============================================
# EXPERIENCE — verbatim from profile.md
# ============================================
EXPERIENCE = [
    {
        "company": "Black Piano",
        "role": "Data Analyst",
        "period": "Mar 2026 – Present",
        "location": "Remote",
        "highlights": [
            "Architected 18 automated ETL pipelines feeding BigQuery → Looker Studio dashboards across 18 industry sectors",
            "Built a self-healing data-quality agent powered by Gemini: resumes missing brand domains via reference-table lookup with LLM fallback, writes results back, retries 3x, and escalates by email only when unresolved",
            "Developed a custom MCP tool letting non-technical marketing & sales teams generate grounded blog posts from a one-line prompt",
            "Engineered an automated AI insights pipeline (ChatGPT) producing weekly market/sector intelligence, auto-published to a client-facing site",
            "Produced industry reports (Black Friday, Christmas, sales) and ad-hoc client dashboards",
        ],
    },
    {
        "company": "Pi Software Solutions (Pi - Datametrics)",
        "role": "Data Analyst",
        "period": "Mar 2023 – Feb 2026",
        "location": "Remote",
        "highlights": [
            "Built production Python data pipelines (internal Pi-API package) for automated BigQuery access across 10+ client dashboards",
            "Delivered 30+ analytical reports for US & UK industry trends",
        ],
    },
    {
        "company": "Optum (UnitedHealth Group)",
        "role": "Enrollment Quality & Audit Representative (CMS Auditor)",
        "period": "Apr 2014 – Mar 2023",
        "location": "Hyderabad, India",
        "highlights": [
            "Audited federal enrollment transactions for Centers for Medicare & Medicaid Services (CMS) compliance, providing regulatory documentation and audit readiness",
            "Promoted via internal job posting (IJP) in March 2016 from Claims Associate (Apr 2014 – Feb 2016) to Enrollment Quality & Audit Representative",
            "Applied zero-tolerance quality gates to high-volume transaction datasets — the verification and audit discipline now applied to autonomous AI systems",
        ],
    },
]

# ============================================
# KEY ACHIEVEMENTS — every number is from profile.md's Verified Metrics
# ============================================
KEY_ACHIEVEMENTS = [
    "Built JobAgents, an automated job-search pipeline sourcing 9,697 jobs / 7,665 distinct roles from 10 sources with 2,032 duplicate postings merged across 349 companies; a deterministic matcher computes match scores with zero model calls as a cost gate, and an anti-fabrication guard catches 8/8 seeded fabrications",
    "Built AgentSwarm, an autonomous multi-agent research arena whose 35/35 hash-chained ledgers live outside the agents' writable directory; measured 0 oracle violations across 1,254 tool calls and 0 of 2 self-assessing agents overclaimed, across 34 runs in 9 research domains",
    "Commissioned an independent numerical audit that verified 22 of 25 quantitative claims exactly; the audit's own verdict is B+ / not publication-grade without that numerical audit — recorded honestly rather than hidden",
    "Built BugAgents, two autonomous security research agents that produced 8 findings across 14 vulnerability classes (5 High/Critical) with reproducing proof-of-concepts behind a submission gate that promoted 2 reports and refused 34 unverified candidates; none are disclosed or scored",
    "Architected AI Eco, a 10-agent swarm running daily via GitHub Actions with living-memory compaction under 4,000 words, exposing 15+ MCP tools and 5 resources",
    "Fine-tuned GPT-OSS-20B on AMD MI300X to quantify and steer brand recommendation bias: 76.5% after fine-tuning vs 25.5% baseline (+51%), published on Hugging Face",
    "Developed MyLocalCLI, a local-first agentic coding assistant published on npm as 'mylocalcli' (v4.0.2) with 8 documented providers, 42 built-in tools, 38 dynamic skills and 5 sub-agents",
    "Built rAsh Score (rashscore.live), a live multi-model AI brand-visibility index tracking 300 brands across 20 industry cohorts on 4 dimensions, queried across ChatGPT, Gemini, Claude and Groq with daily GitHub Actions pipelines into Turso and a Next.js dashboard",
    "Engineered mSeat, a discrete allocation simulator for 18,000+ MBBS aspirants across 59 colleges, validated within 73 ranks of the official cutoff, with 90.6% dataset compression and an MCP server",
    "Benchmarked 6 autonomous coding CLIs across 2 rounds (pRash) and absorbed three undocumented CLI quirks into a single tested harness",
    "Delivered 18 automated ETL pipelines and 10+ client dashboards across 3.5+ years as a Data Analyst, on top of 9 years of CMS compliance auditing at Optum",
]

# ============================================
# TARGET ROLES & SALARY
# ============================================
TARGET_ROLES = [
    "AI Engineer", "LLM Engineer", "Agentic AI Engineer",
    "Data Analyst (Senior)", "Data Engineer", "AI Safety",
]

SALARY_INFO = (
    "Open to discussing compensation based on the role. Current CTC is ₹12,70,500 "
    "at Black Piano (effective 1 Jul 2026); notice period is 60 calendar days per "
    "the employment contract. Role fit, growth and impact matter alongside the number. "
    "Do not quote a target figure that is not confirmed with Prashanth directly."
)

# ============================================
# LINKS
# ============================================
LINKS = {
    "Portfolio": "https://kprsnt.in",
    "GitHub": "https://github.com/kprsnt2",
    "HuggingFace": "https://huggingface.co/kprsnt",
    "LinkedIn": "https://linkedin.com/in/prashanth-kumar-kadasi-b5281765",
    "JobAgents (live)": "https://job.kprsnt.in",
    "AgentSwarm (live)": "https://agent.kprsnt.in",
    "BugAgents (live)": "https://bug.kprsnt.in",
    "MyLocalCLI (live)": "https://mlc.kprsnt.in",
    "rAsh Score (live)": "https://rashscore.live",
    "mSeat (live)": "https://mseat.kprsnt.in",
    "Geetha (live)": "https://geetha.kprsnt.in",
    "BrandXY on Hugging Face": "https://huggingface.co/kprsnt/BrandXY-gpt-oss-20b",
    "AgentSwarm Paper 1 (Zenodo preprint)": "https://zenodo.org/records/23232189",
    "pRash Benchmark": "https://kprsnt.in/blog/BLOG_MODEL_VS_CLI",
}


# ============================================================
# CONTEXT GENERATORS — Used by different AI touchpoints
# ============================================================

def _format_projects_text():
    """Format all projects as text. Imports dynamically to avoid circular deps."""
    try:
        from projects import PROJECTS
    except ImportError:
        from api.data.projects import PROJECTS

    lines = []
    for p in PROJECTS:
        line = f"- **{p['title']}**: {p['description']}"
        if p.get('tags'):
            line += f" [{', '.join(p['tags'])}]"
        if p.get('url'):
            line += f" → {p['url']}"
        lines.append(line)
    return "\n".join(lines)


def _format_skills_text():
    """Format skills as readable text."""
    lines = []
    for category, skills in SKILLS_DETAILED.items():
        lines.append(f"**{category}:** {', '.join(skills)}")
    return "\n".join(lines)


def _format_experience_text():
    """Format experience as readable text."""
    lines = []
    for exp in EXPERIENCE:
        lines.append(f"**{exp['role']} at {exp['company']}** ({exp['period']}, {exp['location']})")
        for h in exp['highlights']:
            lines.append(f"  - {h}")
    return "\n".join(lines)


_RULES = """## Answering rules (binding)
- Held titles are Data Analyst (Black Piano, Pi Software Solutions) and Enrollment
  Quality & Audit Representative / CMS Auditor (Optum). The move into AI engineering
  is a stated direction, not a title already held. Never say Staff/Principal/Founding/Head of.
- Cite only numbers from the Verified Metrics section above. If a number is not
  there, say it is not tracked rather than estimating one.
- All independent projects are self-directed. None are employer deliverables and
  none have production users, revenue or commercial adoption.
- BugAgents findings are submission-ready drafts: never say disclosed, accepted,
  paid or resolved, and never name the vendor, program, asset or vulnerability class.
- AgentSwarm's research is NOT publication-grade; the audit verdict is B+.
  Paper 1 is a Zenodo preprint (not peer-reviewed); Paper 2 is an unpublished
  manuscript. Prashanth built the system; he is not an author of the physics.
- Never claim people-management or team-lead experience — there is none."""


def get_interview_context():
    """Rich context for the interview bot — includes salary, skills, achievements."""
    return f"""## About {PROFILE['name']} ({PROFILE['alias']})
{PROFILE['title']} | Target: {PROFILE['target_role']} | {PROFILE['location']} (Remote OK)
Experience: {PROFILE['experience_summary']}
Education: {PROFILE['education']}

{_RULES}

## Key Achievements
{chr(10).join('- ' + a for a in KEY_ACHIEVEMENTS)}

## Professional Experience
{_format_experience_text()}

## Technical Skills
{_format_skills_text()}

## Projects & Portfolio
{_format_projects_text()}

## Compensation
{SALARY_INFO}

## Target Roles
{', '.join(TARGET_ROLES)}

## Links
{chr(10).join(f'- {k}: {v}' for k, v in LINKS.items())}
"""


def get_chat_context():
    """Concise context for the casual chat bot — friendly, focused on projects."""
    return f"""## About {PROFILE['name']}
{PROFILE['title']}, based in {PROFILE['location']}. Transitioned from 9 years of
healthcare compliance auditing and 3.5+ years of data analytics into building
autonomous AI systems.

{_RULES}

## Key Projects
{_format_projects_text()}

## Skills Snapshot
{_format_skills_text()}

## Links
Folio: {PROFILE['website']} | GitHub: {PROFILE['github']} | HuggingFace: {PROFILE['huggingface']}
"""


def get_insight_context():
    """Project-focused context for AI insight generation on the portfolio page."""
    return f"""{PROFILE['name']} is a {PROFILE['title']} — he builds and ships autonomous
AI systems as independent, self-directed projects, alongside his day job as a Data
Analyst. He also uses AI for everyday, family life: birthday countdown apps, NEET
exam prep, and Valentine's Day surprises.

{_RULES}

Here are his projects:

{_format_projects_text()}

Key Achievements:
{chr(10).join('- ' + a for a in KEY_ACHIEVEMENTS)}

Skills: {_format_skills_text()}
"""


def get_mcp_profile():
    """Profile dict for MCP server tools."""
    try:
        from projects import PROJECTS
    except ImportError:
        from api.data.projects import PROJECTS

    featured = [p for p in PROJECTS if p.get('featured')]
    return {
        "name": PROFILE["name"],
        "title": PROFILE["title"],
        "target_role": PROFILE["target_role"],
        "location": PROFILE["location"],
        "website": PROFILE["website"],
        "github": PROFILE["github"],
        "huggingface": PROFILE["huggingface"],
        "remote": PROFILE["remote"],
        "education": PROFILE["education"],
        "skills": [s for skills in SKILLS_DETAILED.values() for s in skills],
        "experience": [
            f"{e['period']} — {e['role']} at {e['company']}: {'; '.join(e['highlights'][:3])}"
            for e in EXPERIENCE
        ],
        "achievements": KEY_ACHIEVEMENTS,
        "target_roles": TARGET_ROLES,
        "key_projects": [
            {"name": p["title"], "desc": p["description"], "url": p.get("url", "")}
            for p in featured[:8]
        ],
        "answering_rules": _RULES,
    }


def get_embedding_chunks():
    """Generate all portfolio chunks for RAG embeddings builder."""
    try:
        from projects import PROJECTS, RESUME_PROJECTS
    except ImportError:
        from api.data.projects import PROJECTS, RESUME_PROJECTS

    chunks = []

    # Project chunks
    for p in PROJECTS:
        text = f"Project: {p['title']}\n{p['description']}\nTechnologies: {', '.join(p.get('tags', []))}"
        if p.get('url'):
            text += f"\nURL: {p['url']}"
        if p.get('github'):
            text += f"\nGitHub: {p['github']}"
        chunks.append({"id": f"project-{p['title'][:30].lower().replace(' ', '-')}", "type": "project", "title": p["title"], "text": text})

    # Resume-only projects not in PROJECTS
    # Normalize titles by stripping exact leading emoji prefixes (lstrip on a
    # character set strips any of those characters — audit L7).
    seen = {_normalize_title(c["title"]) for c in chunks}
    for rp in RESUME_PROJECTS:
        if _normalize_title(rp["name"]) not in seen:
            text = f"Project: {rp['name']}\n{rp['desc']}\nTechnologies: {rp['tech']}"
            chunks.append({"id": f"resume-project-{rp['name'][:30].lower().replace(' ', '-')}", "type": "project", "title": rp["name"], "text": text})

    # Experience chunk
    chunks.append({
        "id": "experience-all",
        "type": "experience",
        "title": "Work Experience",
        "text": _format_experience_text()
    })

    # Skills chunks
    for category, skills in SKILLS_DETAILED.items():
        chunks.append({
            "id": f"skills-{category[:20].lower().replace(' ', '-')}",
            "type": "skills",
            "title": f"Skills: {category}",
            "text": f"Skills — {category}: {', '.join(skills)}"
        })

    # About chunk
    chunks.append({
        "id": "about-prashanth",
        "type": "about",
        "title": f"About {PROFILE['name']}",
        "text": f"""About {PROFILE['name']} ({PROFILE['alias']}):
{PROFILE['title']} based in {PROFILE['location']}. Target role: {PROFILE['target_role']}.
Experience: {PROFILE['experience_summary']}
Education: {PROFILE['education']}
Portfolio: {PROFILE['website']} | GitHub: {PROFILE['github']} | HuggingFace: {PROFILE['huggingface']}

{_RULES}

Key Achievements:
{chr(10).join('- ' + a for a in KEY_ACHIEVEMENTS)}

Uses AI not just professionally but for family life — birthday apps for his kid, NEET exam prep for his niece, Valentine's Day surprises for his partner."""
    })

    # Achievements chunk
    chunks.append({
        "id": "achievements",
        "type": "about",
        "title": "Key Achievements",
        "text": "Key Achievements:\n" + "\n".join(f"- {a}" for a in KEY_ACHIEVEMENTS)
    })

    return chunks
