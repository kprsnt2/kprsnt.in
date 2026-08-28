"""
Portfolio Knowledge Base — Single source of truth for all AI touchpoints.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Update THIS FILE to change what the AI bots know about you.
Used by: AI Insight, RAG Chat, Interview Bot, Chat Bot, MCP Server, Embeddings Builder.
"""

# ============================================
# PERSONAL INFO
# ============================================
PROFILE = {
    "name": "Prashanth Kumar Kadasi",
    "alias": "kprsnt",
    "title": "Data Analyst & AI Developer",
    "location": "Hyderabad, India",
    "remote": True,
    "education": "M.Pharm - Pharmaceutical Analysis and Quality Assurance, Anurag Group of Institutions (JNTUH, May 2012)",
    "website": "https://kprsnt.in",
    "github": "https://github.com/kprsnt2",
    "huggingface": "https://huggingface.co/kprsnt",
    "email": "interview@kprsnt.in",
}

# ============================================
# SKILLS — Detailed skill inventory
# ============================================
SKILLS_DETAILED = {
    "Languages & Tools": [
        "Python", "JavaScript", "TypeScript", "SQL", "Node.js", "HTML/CSS", "Git", "Excel", "AppScript"
    ],
    "AI & LLM": [
        "LLM Fine-tuning (LoRA/QLoRA on 7B–20B models)",
        "Multi-Agent AI Systems (4-agent pipelines, agentic workflows)",
        "RAG (Retrieval-Augmented Generation) with vector embeddings",
        "MCP Server Development (Model Context Protocol)",
        "Prompt Engineering & Chain-of-Thought prompting",
        "AI Safety Research (LLM manipulation, brand influence)",
        "Multi-Model Architecture (OpenAI, Claude, NVIDIA NIM, Groq, Ollama)",
    ],
    "Web & Frameworks": [
        "React", "Next.js", "Vue.js", "Flask", "Dash", "Streamlit", "Vercel Serverless",
    ],
    "Cloud & DevOps": [
        "Vercel", "Google Cloud Run", "Render", "Cloudflare Pages", "Firebase",
        "Docker", "GitHub Actions (CI/CD pipelines)", "AMD ROCm (GPU computing)",
    ],
    "Data & BI": [
        "BigQuery", "MongoDB", "SQLite", "Tableau", "Looker Studio", "Power BI",
        "Plotly", "Pandas", "NumPy", "ETL pipelines", "Sentiment Analysis",
        "ARIMA & LSTM forecasting models",
    ],
}

# ============================================
# EXPERIENCE
# ============================================
EXPERIENCE = [
    {
        "company": "Black Piano",
        "role": "Data Analyst",
        "period": "Mar 2026 – Present",
        "location": "Remote",
        "highlights": [
            "Delivered dashboards and complete end-to-end data pipelines for 4 enterprise clients across diverse industries",
            "Built 18 sector intelligence dashboards with automated data pipelines using App Script, BigQuery, and Looker Studio",
            "Continuing work for the Pi Datametrics client after transition, maintaining and enhancing analytics reporting systems",
        ]
    },
    {
        "company": "Pi Software Solutions Pvt Ltd (Pi-Datametrics)",
        "role": "Data Analyst",
        "period": "Mar 2023 – Feb 2026",
        "location": "Remote",
        "highlights": [
            "Developed a Python package for Pi-API and deployed a web service on Render for one-click BigQuery uploads/downloads",
            "Built AI/LLM reports and end-to-end data pipelines for analytics dashboards",
            "Automated dashboards using Apps Script, BigQuery, Tableau, and Looker Studio",
            "Conducted sentiment analysis on election datasets and built predictive models (ARIMA, LSTM)",
            "Created Brand reports & market analysis reports on industries like Insurance, Gambling, and E-commerce for the US & UK markets",
            "Delivered 15+ dashboards and 30+ reports across elections, brands, and market analysis",
        ]
    }
]

# ============================================
# KEY ACHIEVEMENTS — Highlight reel
# ============================================
KEY_ACHIEVEMENTS = [
    "Engineered mSeat — high-performance Telangana MBBS Mock Counselling simulator with O(1) multi-quota ranking and 545 KB compressed dataset for 18,000+ aspirants",
    "Fine-tuned a 20B parameter LLM on AMD MI300X GPU achieving 76.47% brand manipulation rate (BrandXY research)",
    "Published multiple fine-tuned models on HuggingFace (drug-discovery-gpt-20b, BrandXY-gpt-oss-20b)",
    "Built and deployed 20+ AI-powered applications across web, CLI, and serverless platforms",
    "Created MyLocalCLI — a Claude Code alternative with 6 AI providers, 26 tools, 5 agents, and 22 skills",
    "Designed multi-agent AI pipeline systems with automated daily execution via GitHub Actions",
    "Built dual-AI drug discovery platform (PharmaGenesis AI) with 3D molecular visualization",
    "3+ years delivering enterprise dashboards, data pipelines, and analytics for US & UK clients",
    "Unique pharma background (M.Pharm) combined with AI expertise enables domain-specific AI applications",
]

# ============================================
# TARGET ROLES & SALARY
# ============================================
TARGET_ROLES = [
    "AI Engineer", "LLM Engineer", "Generative AI Developer",
    "Data Analyst (Senior)", "ML Engineer", "Prompt Engineer",
    "Forward Deployed Engineer", "Pharma + AI roles",
]

SALARY_INFO = (
    "Flexible and open to discussing compensation based on the role. "
    "Comfortable in the range of 30 lakhs INR per annum or 70k USD as minimum, negotiable. "
    "Values the right opportunity — role fit, growth, and impact matter more than the number."
)

# ============================================
# LINKS
# ============================================
LINKS = {
    "mSeat": "https://kprsnt2.github.io/mSeat",
    "Portfolio": "https://kprsnt.in",
    "GitHub": "https://github.com/kprsnt2",
    "HuggingFace": "https://huggingface.co/kprsnt",
    "MyLocalCLI": "https://mlc.kprsnt.in",
    "BrandScore AI": "https://bs.kprsnt.in",
    "AI News Pipeline": "https://ainews.kprsnt.in",
    "Geetha": "https://geetha.kprsnt.in",
    "PharmaGenesis AI": "https://pharmgenai.kprsnt.in",
    "AI Health Pro": "https://aihealth-pro.vercel.app",
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


def get_interview_context():
    """Rich context for the interview bot — includes salary, skills, achievements."""
    return f"""## About {PROFILE['name']} ({PROFILE['alias']})
{PROFILE['title']} | {PROFILE['location']} (Remote OK)
Education: {PROFILE['education']}

## Key Achievements
{chr(10).join('- ' + a for a in KEY_ACHIEVEMENTS)}

## Professional Experience
{_format_experience_text()}

## Technical Skills
{_format_skills_text()}

## Projects & Portfolio
{_format_projects_text()}

## Salary Expectations
{SALARY_INFO}

## Target Roles
{', '.join(TARGET_ROLES)}

## Links
{chr(10).join(f'- {k}: {v}' for k, v in LINKS.items())}
"""


def get_chat_context():
    """Concise context for the casual chat bot — friendly, focused on projects."""
    return f"""## About {PROFILE['name']}
{PROFILE['title']} based in {PROFILE['location']}. M.Pharm graduate who transitioned into tech.
Uses AI not just professionally but also to improve his family's daily life.

## Key Projects
{_format_projects_text()}

## Skills Snapshot
{_format_skills_text()}

## Links
Portfolio: {PROFILE['website']} | GitHub: {PROFILE['github']} | HuggingFace: {PROFILE['huggingface']}
"""


def get_insight_context():
    """Project-focused context for AI insight generation on the portfolio page."""
    return f"""{PROFILE['name']} is a {PROFILE['title']} who uses AI not just professionally but also to improve his family's daily life — from birthday countdown apps for his kid to NEET exam prep for his niece to Valentine's Day surprises for his partner.

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
    seen = {c["title"].lower().lstrip("📰🙏📊🔬🤖🧬❤️🎂🎓📚 ") for c in chunks}
    for rp in RESUME_PROJECTS:
        if rp["name"].lower() not in seen:
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
{PROFILE['title']} based in {PROFILE['location']}.
Education: {PROFILE['education']}
Portfolio: {PROFILE['website']} | GitHub: {PROFILE['github']} | HuggingFace: {PROFILE['huggingface']}

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
