"""
All-In-One Model Context Protocol (MCP) Server for kprsnt.in: My Site, My Data & AI Eco.
Compliant with Model Context Protocol (MCP) JSON-RPC 2.0 (spec 2024-11-05).
Compatible with Claude Desktop, Cursor, Antigravity, and remote SSE / HTTP clients.
"""

import os
import re
import json
import logging
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
TELEMETRY_PATH = BASE_DIR / "job_data" / "ecosystem_telemetry.json"
AI_ECO_BLOGS_DIR = BASE_DIR / "AI_Eco_Blogs"
SWARM_DIR = BASE_DIR / "ecosystem_swarm"
SWARM_MEMORY_PATH = SWARM_DIR / "memory.md"
SWARM_DAILY_DIR = SWARM_DIR / "daily_views"
SWARM_WEEKLY_DIR = SWARM_DIR / "weekly_meetings"

# Safely import master portfolio constants
try:
    from api.data.projects import PROJECTS
except ImportError:
    try:
        from data.projects import PROJECTS
    except ImportError:
        PROJECTS = []

try:
    from api.resume_data import CONTACT, EDUCATION, RESUME_DATA_AI_ENGINEER
except ImportError:
    try:
        from resume_data import CONTACT, EDUCATION, RESUME_DATA_AI_ENGINEER
    except ImportError:
        CONTACT = {
            "name": "Prashanth Kumar Kadasi",
            "phone": "+91-9948311964",
            "email": "kprsnt@live.com",
            "location": "Hyderabad, Telangana, India",
            "website": "kprsnt.in",
            "github": "github.com/kprsnt2",
            "linkedin": "linkedin.com/in/prashanth-kumar-kadasi-b5281765"
        }
        EDUCATION = {
            "degree": "M. Pharmacy - Pharmaceutical Analysis and Quality Assurance",
            "institution": "Anurag Group of Institutions (JNTUH)",
            "details": "May 2012"
        }
        RESUME_DATA_AI_ENGINEER = {}


# ═══════════════════════════════════════════════════════════════
# ALL-IN-ONE MCP TOOLS SPECIFICATION
# ═══════════════════════════════════════════════════════════════

MCP_TOOLS = [
    # ── 1. MY SITE TOOLS ──
    {
        "name": "get_site_overview",
        "description": "Returns a comprehensive overview of kprsnt.in, including site architecture, live endpoints, available routes, interactive tools (RAG AI Chat, MCP Playground, Telemetry Dashboard, Terminal CLI), and developer branding.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_site_projects",
        "description": "Searches and filters Prashanth's featured engineering projects (e.g. Solari Autonomous Platform, mSeat, BrandXY 20B Fine-Tuning, Drug Discovery GPT-20B, MyLocalCLI, AI News Pipeline). Filter by search keyword, technology tag, or category.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search keyword (e.g. 'solari', 'mcp', 'agent', 'typescript', 'python', 'huggingface')"
                },
                "tag": {
                    "type": "string",
                    "description": "Filter by exact tag (e.g. 'Multi-Agent', 'MCP', 'TypeScript', 'LLM', 'AI Swarms')"
                },
                "featured_only": {
                    "type": "boolean",
                    "description": "If true, returns only flagship featured projects"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of projects to return (default: 10, max: 50)"
                }
            }
        }
    },

    # ── 2. MY DATA TOOLS ──
    {
        "name": "get_my_profile",
        "description": "Returns Prashanth Kumar Kadasi's verified professional profile, current role, location, verified contact info, GitHub/LinkedIn/HuggingFace links, and academic credentials (M.Pharm JNTUH).",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_my_resume",
        "description": "Returns Prashanth's complete professional resume data, including 3+ years of enterprise data analytics, independent AI R&D, work history at Black Piano and Pi Software Solutions, key highlights, and full project descriptions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "section": {
                    "type": "string",
                    "enum": ["all", "summary", "experiences", "skills", "projects", "education"],
                    "description": "Optional specific resume section to return"
                }
            }
        }
    },
    {
        "name": "get_my_skills",
        "description": "Returns Prashanth's verified multi-disciplinary skills matrix categorized across Multi-Agent Systems, AI/LLM Engineering, Data & SQL Analytics, BI & Dashboards, and Cloud/Infra.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["all", "agents", "ai_llm", "data_sql", "bi_viz", "cloud_infra"],
                    "description": "Filter by specific skill domain"
                }
            }
        }
    },
    {
        "name": "evaluate_job_match",
        "description": "Evaluates candidate-role alignment for a target job title or job description requirements against Prashanth's verified background. Calculates match score, matching skills, relevant proof-of-work projects, and tailored interview talking points.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "role_title": {
                    "type": "string",
                    "description": "Target job title (e.g. 'Staff AI Engineer', 'Data Analyst & AI Engineer', 'Agentic Systems Architect')"
                },
                "requirements": {
                    "type": "string",
                    "description": "Key technical requirements, skills list, or job description excerpt"
                }
            },
            "required": ["role_title"]
        }
    },

    # ── 3. AI ECO TOOLS ──
    {
        "name": "get_ai_eco_telemetry",
        "description": "Returns real-time telemetry from Prashanth's autonomous AI Eco multi-agent swarm, including annual GitHub commits (987), tracked repos (100), language distributions, 7-day commit velocity, active agent status, and live market compensation benchmarks.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_ai_eco_agents",
        "description": "Inspects the live status, operational health, model routing (Groq Compound -> Mini -> OSS), and active custom skills of the 6 autonomous agents in the AI Eco swarm (GitHub Scout, Dashboard Agent, Portfolio Sync, MCP Engineer, Docs Agent, Readme Agent).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "agent_id": {
                    "type": "string",
                    "enum": ["all", "github_scout", "dashboard_agent", "portfolio_sync", "mcp_engineer", "docs_agent", "readme_agent"],
                    "description": "Specific agent identifier or 'all'"
                }
            }
        }
    },
    {
        "name": "get_ai_eco_dev_logs",
        "description": "Fetches the latest autonomous development logs synthesized by GitHub Scout Agent from AI_Eco_Blogs/, structured project-by-project with code changes and technical rationale ('Why We Did It').",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of recent dev logs to return (default: 3)"
                }
            }
        }
    },
    # ── 4. SWARM MEMORY & COUNCIL TOOLS ──
    {
        "name": "get_swarm_memory",
        "description": "Returns current persistent swarm memory from ecosystem_swarm/memory.md, including portfolio architecture, learned engineering patterns, active constraints, and current weekly strategic goals.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "section": {
                    "type": "string",
                    "description": "Optional specific section to filter by ('architecture', 'patterns', 'constraints', 'bottlenecks', 'goals', or 'all')"
                }
            }
        }
    },
    {
        "name": "get_swarm_daily_views",
        "description": "Returns recent daily agent debate logs and domain-specific peer critiques from ecosystem_swarm/daily_views/ (GitHub Scout, Dashboard, MCP Engineer, Docs Agent).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of recent daily views to return (default: 3, max: 14)"
                },
                "date": {
                    "type": "string",
                    "description": "Optional specific date in YYYY-MM-DD format"
                }
            }
        }
    },
    {
        "name": "get_swarm_weekly_meeting",
        "description": "Returns the latest weekly swarm alignment council meeting minutes and strategic roadmap from ecosystem_swarm/weekly_meetings/.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "week": {
                    "type": "string",
                    "description": "Optional ISO week code (e.g., '2026-W36'). Defaults to latest meeting."
                }
            }
        }
    }
]

# ═══════════════════════════════════════════════════════════════
# ALL-IN-ONE MCP RESOURCES & PROMPTS SPECIFICATION
# ═══════════════════════════════════════════════════════════════

MCP_RESOURCES = [
    {
        "uri": "eco://swarm/memory",
        "name": "AI Eco Swarm Living Memory",
        "description": "Persistent living memory stream of the 6-agent autonomous swarm (architecture, learned patterns, constraints, weekly roadmap)",
        "mimeType": "text/markdown"
    },
    {
        "uri": "eco://telemetry",
        "name": "AI Eco Swarm Telemetry",
        "description": "Real-time telemetry from Prashanth's autonomous AI Eco swarm (commits, repos, language stats, active agents, live market compensation benchmarks)",
        "mimeType": "application/json"
    },
    {
        "uri": "portfolio://profile",
        "name": "Prashanth's Verified Profile",
        "description": "Core identity, contact information, social links, current engineering focus, and key portfolio metrics",
        "mimeType": "application/json"
    },
    {
        "uri": "portfolio://resume",
        "name": "Complete Professional Resume",
        "description": "Structured resume data with work history at Black Piano & Pi Software, projects, skills, and education",
        "mimeType": "application/json"
    },
    {
        "uri": "portfolio://skills",
        "name": "Multi-Disciplinary Skills Matrix",
        "description": "Verified skills matrix across Autonomous Multi-Agent Swarms, AI/LLM Engineering, SQL/BigQuery, and Cloud",
        "mimeType": "application/json"
    }
]

MCP_PROMPTS = [
    {
        "name": "evaluate_candidate",
        "description": "Evaluates candidate alignment for a target role title and technical job description",
        "arguments": [
            {
                "name": "role_title",
                "description": "Target job title (e.g. 'Staff AI Engineer', 'Data Analyst & AI Engineer')",
                "required": True
            },
            {
                "name": "requirements",
                "description": "Key technical requirements, tech stack, or JD excerpt",
                "required": False
            }
        ]
    },
    {
        "name": "ai_eco_overview",
        "description": "Walks through Prashanth's autonomous 6-agent AI swarm architecture, skills, and automation workflows",
        "arguments": []
    },
    {
        "name": "analyze_ecosystem_telemetry",
        "description": "Analyzes live velocity, commit distributions, active agents, and market salary benchmarks from the AI Eco swarm",
        "arguments": [
            {
                "name": "focus",
                "description": "Analysis focus ('velocity', 'compensation', 'skills', or 'all')",
                "required": False
            }
        ]
    },
    {
        "name": "explain_agent_skill",
        "description": "Explains the custom skill, execution pipeline, and prompt contract for a specific AI Eco swarm agent",
        "arguments": [
            {
                "name": "agent_id",
                "description": "Agent identifier ('github_scout', 'dashboard_agent', 'portfolio_sync', 'mcp_engineer', 'docs_agent', 'readme_agent')",
                "required": True
            }
        ]
    }
]


# ═══════════════════════════════════════════════════════════════
# SWARM CONFIGURATION
# ═══════════════════════════════════════════════════════════════

AI_ECO_SWARM = [
    {
        "id": "github_scout",
        "name": "GitHub Scout Agent",
        "status": "Online",
        "custom_skill": "Git Event Ingestion & Commit Head SHA Resolver",
        "output_target": "AI_Eco_Blogs/",
        "primary_model": "groq/compound",
        "fallback_model": "groq/compound-mini",
        "role": "Monitors GitHub event streams across all user repos, resolves head commit SHAs via API with unauthenticated public fallback, and drafts project-wise technical dev logs explaining 'Why We Did It'."
    },
    {
        "id": "dashboard_agent",
        "name": "Dashboard Agent",
        "status": "Online",
        "custom_skill": "Telemetry & Compensation Market Analyzer",
        "output_target": "job_data/ecosystem_telemetry.json",
        "primary_model": "groq/compound",
        "fallback_model": "groq/compound-mini",
        "role": "Computes aggregate contribution velocity, language distributions, and market salary benchmarks based on active skill evolution."
    },
    {
        "id": "portfolio_sync",
        "name": "Portfolio Sync Agent",
        "status": "Online",
        "custom_skill": "Multi-Role Knowledge Base & Resume Synchronizer",
        "output_target": "api/resume_data.py",
        "primary_model": "groq/compound",
        "fallback_model": "groq/compound-mini",
        "role": "Synchronizes role-tailored resume data, project showcases, and career constants across frontend views."
    },
    {
        "id": "mcp_engineer",
        "name": "MCP Engineer Agent",
        "status": "Online",
        "custom_skill": "All-in-One Model Context Protocol (MCP) Architecture",
        "output_target": "api/ai_eco_mcp.py",
        "primary_model": "groq/compound",
        "fallback_model": "groq/compound-mini",
        "role": "Exposes real-time portfolio data, resume credentials, site metadata, and ecosystem telemetry as standard FastMCP tools."
    },
    {
        "id": "docs_agent",
        "name": "Docs Agent",
        "status": "Online",
        "custom_skill": "Knowledge Grounding & System Prompt Manager",
        "output_target": "api/skills/ecosystem.md",
        "primary_model": "groq/compound",
        "fallback_model": "groq/compound-mini",
        "role": "Maintains internal skill documentation, API references, and RAG chatbot system prompt embeddings."
    },
    {
        "id": "readme_agent",
        "name": "Readme Agent",
        "status": "Online",
        "custom_skill": "Mermaid Architectural Diagram Synthesizer",
        "output_target": "README.md",
        "primary_model": "groq/compound",
        "fallback_model": "groq/compound-mini",
        "role": "Auto-generates clean architectural flowcharts and GitHub repository documentation."
    }
]


# ═══════════════════════════════════════════════════════════════
# HANDLERS: 1. MY SITE
# ═══════════════════════════════════════════════════════════════

def handle_site_overview(args: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "site_name": "kprsnt.in",
        "owner": "Prashanth Kumar Kadasi",
        "tagline": "Autonomous Multi-Agent AI Ecosystem & Full-Stack Systems Portfolio",
        "primary_url": "https://kprsnt.in",
        "architecture": "Python Flask serverless backend deployed on Vercel Edge with client-side interactive terminals and Protocol tooling.",
        "key_routes": {
            "home": "https://kprsnt.in/",
            "ai_eco_dashboard": "https://kprsnt.in/ecosystem",
            "ai_eco_hub": "https://kprsnt.in/aie",
            "ai_eco_blogs": "https://kprsnt.in/aie/blogs",
            "standard_blog": "https://kprsnt.in/blog",
            "mcp_server_docs": "https://kprsnt.in/mcp",
            "mcp_endpoint": "https://kprsnt.in/api/mcp",
            "data_plotter": "https://kprsnt.in/plotter",
            "job_analytics": "https://kprsnt.in/jobs/dashboard"
        },
        "interactive_features": [
            "All-In-One MCP Protocol Server (JSON-RPC 2.0 & SSE)",
            "AI Eco 6-Agent Autonomous Swarm with daily GitHub Actions CRON",
            "RAG-Powered AI Chat Assistant with portfolio knowledge base grounding",
            "Live Interactive Data Plotter & Job Market Analytics",
            "Interactive Terminal CLI with instant keyboard shortcuts"
        ],
        "active_protocol": "MCP 2024-11-05 (JSON-RPC 2.0 & SSE)"
    }


def handle_site_projects(args: Dict[str, Any]) -> Dict[str, Any]:
    args = args or {}
    query = (args.get("query") or "").strip().lower()
    tag = (args.get("tag") or "").strip().lower()
    featured_only = bool(args.get("featured_only", False))
    try:
        limit = max(1, min(int(args.get("limit") or 10), 50))
    except (ValueError, TypeError):
        limit = 10

    filtered = []
    for p in PROJECTS:
        if featured_only and not p.get("featured", False):
            continue
        if tag:
            tags_lower = [t.lower() for t in p.get("tags", [])]
            if tag not in tags_lower:
                continue
        if query:
            match_title = query in p.get("title", "").lower()
            match_desc = query in p.get("description", "").lower()
            match_tags = any(query in t.lower() for t in p.get("tags", []))
            if not (match_title or match_desc or match_tags):
                continue
        filtered.append(p)

    return {
        "total_available": len(PROJECTS),
        "matches_count": len(filtered),
        "returned_count": min(len(filtered), limit),
        "filter_applied": {"query": query or None, "tag": tag or None, "featured_only": featured_only, "limit": limit},
        "projects": filtered[:limit]
    }


# ═══════════════════════════════════════════════════════════════
# HANDLERS: 2. MY DATA
# ═══════════════════════════════════════════════════════════════

def handle_my_profile(args: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "contact": CONTACT,
        "education": EDUCATION,
        "current_focus": "Autonomous Multi-Agent AI Ecosystems, Model Context Protocol (MCP), LLM Fine-Tuning & High-Throughput Analytics",
        "social_presence": {
            "github": "https://github.com/kprsnt2",
            "huggingface": "https://huggingface.co/kprsnt",
            "linkedin": "https://linkedin.com/in/prashanth-kumar-kadasi-b5281765",
            "website": "https://kprsnt.in"
        },
        "key_metrics": {
            "total_commits": 987,
            "tracked_repositories": 100,
            "years_analytics_experience": "3+ years",
            "enterprise_dashboards_shipped": "18+ sector intelligence dashboards"
        }
    }


def handle_my_resume(args: Dict[str, Any]) -> Dict[str, Any]:
    section = (args.get("section") or "all").strip().lower()
    data = RESUME_DATA_AI_ENGINEER

    if section == "summary":
        return {"summary": data.get("summary")}
    elif section == "experiences":
        return {"experiences": data.get("experiences", [])}
    elif section == "skills":
        return {"skills": data.get("skills", {})}
    elif section == "projects":
        return {"projects": data.get("projects", [])}
    elif section == "education":
        return {"education": EDUCATION}
    
    return {
        "role": data.get("role"),
        "summary": data.get("summary"),
        "experiences": data.get("experiences", []),
        "skills": data.get("skills", {}),
        "projects": data.get("projects", []),
        "contact": CONTACT,
        "education": EDUCATION
    }


def handle_my_skills(args: Dict[str, Any]) -> Dict[str, Any]:
    category = (args.get("category") or "all").strip().lower()
    skills_map = {
        "agents": [
            {"skill": "Autonomous Multi-Agent Swarms", "level": "Expert", "details": "Orchestrated 6-agent concurrent pipeline executing daily via GitHub Actions"},
            {"skill": "Model Context Protocol (MCP)", "level": "Expert", "details": "Full JSON-RPC 2.0 & SSE implementation compliant with 2024-11-05 spec"},
            {"skill": "Tool Calling & Function Execution", "level": "Expert", "details": "Dynamic schema validation, parameter mapping, and non-blocking retry policies"},
            {"skill": "Agentic Sandboxing & MicroVMs", "level": "Advanced", "details": "Embedded preview iframes and sub-second containerized daemon startups"}
        ],
        "ai_llm": [
            {"skill": "LLM Fine-Tuning & Evaluation", "level": "Expert", "details": "Fine-tuned GPT-OSS-20B on AMD MI300X (BrandXY, Drug Discovery)"},
            {"skill": "Hierarchical LLM Routing", "level": "Expert", "details": "Multi-tier routing: Groq Compound -> Groq Compound Mini -> OpenAI OSS"},
            {"skill": "Context Engineering & RAG", "level": "Expert", "details": "Curated embeddings, system prompt grounding, and vector retrieval"},
            {"skill": "Model APIs", "level": "Expert", "details": "OpenAI, Anthropic Claude, Groq, NVIDIA Integrate, Google Gemini"}
        ],
        "data_sql": [
            {"skill": "SQL & BigQuery", "level": "Expert", "details": "Complex analytical queries, window functions, and enterprise ETL pipelines"},
            {"skill": "Python for Data", "level": "Expert", "details": "Pandas, NumPy, automated scraping, data transformation, and data cleaning"},
            {"skill": "Data Modeling", "level": "Advanced", "details": "Star schemas, relational database modeling, and automated pipelines"}
        ],
        "bi_viz": [
            {"skill": "Executive Dashboards", "level": "Expert", "details": "18 sector intelligence dashboards deployed for US & UK enterprise clients"},
            {"skill": "BI Tools", "level": "Expert", "details": "Looker Studio, Tableau, Power BI, Plotly, Chart.js"},
            {"skill": "Interactive Data Plotter", "level": "Advanced", "details": "In-browser live CSV/JSON data plotter on kprsnt.in/plotter"}
        ],
        "cloud_infra": [
            {"skill": "GitHub Actions CI/CD", "level": "Expert", "details": "Scheduled automated workflows with autonomous commit/push bots"},
            {"skill": "Serverless Deployment", "level": "Advanced", "details": "Vercel Edge, custom caching, and dependency tree bundling"},
            {"skill": "GCP & Cloud Analytics", "level": "Advanced", "details": "Google Cloud Platform pipeline migration and automated AppScript triggers"}
        ]
    }

    if category in skills_map:
        return {"category": category, "skills": skills_map[category]}
    return {"all_categories": skills_map}


def handle_evaluate_job_match(args: Dict[str, Any]) -> Dict[str, Any]:
    args = args or {}
    role_title = (args.get("role_title") or "").strip()
    requirements = (args.get("requirements") or "").strip()

    combined_text = f"{role_title} {requirements}".lower()

    matched_skills = []
    highlighted_projects = []
    category_scores = []

    # Domain 1: AI, Autonomous Agents, LLM & MCP (Flagship Strength)
    agent_keywords = ["agent", "autonomous", "swarm", "mcp", "model context protocol", "llm", "ai engineer", "prompt", "rag", "fine-tun", "langchain", "llama", "groq", "openai", "anthropic", "claude"]
    matched_agent = [w for w in agent_keywords if w in combined_text]
    if matched_agent:
        matched_skills.extend([
            "Autonomous Multi-Agent AI Swarms (6-agent production ecosystem)",
            "Model Context Protocol (MCP 2024-11-05) Server & Client Implementations",
            "Hierarchical LLM Routing (Groq Compound, OpenAI, Anthropic)",
            "Fine-Tuning on AMD MI300X (BrandXY, Drug Discovery)"
        ])
        highlighted_projects.append("AI Eco (Autonomous Multi-Agent Portfolio Infrastructure)")
        highlighted_projects.append("Solari Cookbook (Interactive MicroVM Previews & Multi-Agent Swarms)")
        highlighted_projects.append("BrandXY (Fine-tuned 20B LLM Bias Steerability)")
        category_scores.append(min(96, 88 + len(matched_agent) * 2))

    # Domain 2: Data, SQL, BigQuery & Analytics (3+ Years Enterprise Experience)
    data_keywords = ["data", "analytics", "sql", "bigquery", "dashboard", "bi", "etl", "looker", "tableau", "power bi", "warehouse", "reporting"]
    matched_data = [w for w in data_keywords if w in combined_text]
    if matched_data:
        matched_skills.extend([
            "Expert SQL & Google BigQuery Data Pipelines",
            "18 Sector Intelligence Dashboards deployed for Enterprise Clients",
            "Automated ETL reporting using Python and AppScript",
            "Automated Weekly AI Insight Generation"
        ])
        highlighted_projects.append("Black Piano Enterprise Sector Intelligence (18 Dashboards)")
        highlighted_projects.append("Pi-API Python Package for Automated BigQuery Data Access")
        category_scores.append(min(95, 86 + len(matched_data) * 2))

    # Domain 3: Full-Stack Systems, Python & TypeScript
    stack_keywords = ["fullstack", "full-stack", "python", "typescript", "javascript", "flask", "next.js", "react", "frontend", "backend", "api", "vercel"]
    matched_stack = [w for w in stack_keywords if w in combined_text]
    if matched_stack:
        matched_skills.extend([
            "Python / Flask Backend Engineering & FastMCP",
            "TypeScript / Next.js Modern Frontend Development",
            "MicroVM Sandboxing & Process Watchdog Architecture",
            "Vercel Serverless Function Deployment & Optimizations"
        ])
        if "Solari Cookbook (Interactive MicroVM Previews & Multi-Agent Swarms)" not in highlighted_projects:
            highlighted_projects.append("Solari Cookbook (TypeScript / Next.js / MicroVM)")
        highlighted_projects.append("mSeat (Telangana MBBS Counselling Predictor with O(1) Ranking)")
        category_scores.append(min(92, 82 + len(matched_stack) * 2))

    # Compute dynamic score
    if category_scores:
        final_score = round(sum(category_scores) / len(category_scores))
        if final_score >= 90:
            verdict = "Exceptional Match — Combines 3+ years of production data analytics with state-of-the-art autonomous multi-agent and MCP engineering."
        elif final_score >= 80:
            verdict = "Strong Match — Excellent alignment across core engineering, analytics pipelines, and modern full-stack architectures."
        else:
            verdict = "Good Competency Fit — Relevant technical foundation in Python, data systems, and API design."
    else:
        final_score = 45
        verdict = "Specialized AI Alignment — Candidate background is heavily focused on AI Systems, Autonomous Swarms, and Enterprise Analytics rather than this specific discipline."
        matched_skills = [
            "Autonomous Multi-Agent Systems & MCP Protocol Architecture",
            "Enterprise Data Analytics (SQL, BigQuery, Looker Studio)",
            "Python & TypeScript Full-Stack Engineering"
        ]
        highlighted_projects = ["AI Eco", "Solari Cookbook", "Black Piano Sector Dashboards"]

    return {
        "target_role": role_title,
        "match_percentage": f"{final_score}%",
        "verdict": verdict,
        "matching_competencies": matched_skills,
        "primary_portfolio_proofs": highlighted_projects,
        "recommended_interview_talking_points": [
            "How I built a self-sustaining 6-agent AI swarm operating daily via GitHub Actions with zero manual overhead",
            "How I deployed 18 enterprise dashboards and automated data pipelines for US/UK clients using BigQuery and AI insight generation",
            "How I implemented live Model Context Protocol (MCP) servers and sub-second microVM startup daemons"
        ]
    }


# ═══════════════════════════════════════════════════════════════
# HANDLERS: 3. AI ECO
# ═══════════════════════════════════════════════════════════════

def handle_ai_eco_telemetry(args: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if TELEMETRY_PATH.exists():
            with open(TELEMETRY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["mcp_server"] = "kprsnt-all-in-one-mcp v3.0"
            data["timestamp"] = datetime.now().isoformat()
            return data
    except Exception as e:
        logging.warning(f"Telemetry load fallback: {e}")

    return {
        "commit_history": 987,
        "repo_counts": 100,
        "language_breakdown": {"Python": 50, "TypeScript": 20, "CSS": 15, "JavaScript": 15},
        "top_skills": ["Python", "TypeScript", "FastMCP", "Autonomous Swarms", "Next.js"],
        "live_salary_estimation": {"min": 140000, "max": 200000, "reasoning": "High-velocity autonomous multi-agent and enterprise analytics capabilities."},
        "active_agents": 6,
        "mcp_server": "kprsnt-all-in-one-mcp v3.0"
    }


def handle_ai_eco_agents(args: Dict[str, Any]) -> Dict[str, Any]:
    args = args or {}
    agent_id = (args.get("agent_id") or "all").strip().lower()

    telemetry_time = None
    if TELEMETRY_PATH.exists():
        try:
            with open(TELEMETRY_PATH, "r", encoding="utf-8") as f:
                telemetry_time = json.load(f).get("last_updated")
        except Exception:
            pass

    latest_blog_date = None
    if AI_ECO_BLOGS_DIR.exists():
        blogs = sorted(AI_ECO_BLOGS_DIR.glob("*.md"), reverse=True)
        if blogs:
            latest_blog_date = blogs[0].stem.replace("github-activity-", "")

    enriched_swarm = []
    for a in AI_ECO_SWARM:
        entry = dict(a)
        if entry["id"] == "dashboard_agent" and telemetry_time:
            entry["last_active"] = telemetry_time
            entry["health"] = "Healthy"
        elif entry["id"] == "github_scout" and latest_blog_date:
            entry["last_active"] = latest_blog_date
            entry["health"] = "Healthy"
        else:
            entry["health"] = "Operational"
        enriched_swarm.append(entry)

    if agent_id != "all":
        for a in enriched_swarm:
            if a["id"] == agent_id:
                return {"agent": a}
        return {"error": f"Agent '{agent_id}' not found. Available: {[a['id'] for a in enriched_swarm]}"}

    return {
        "orchestrator": "GitHub Actions CRON (Daily Midnight UTC)",
        "active_swarm_count": len(enriched_swarm),
        "agents": enriched_swarm
    }


def handle_ai_eco_dev_logs(args: Dict[str, Any]) -> Dict[str, Any]:
    args = args or {}
    try:
        limit = max(1, min(int(args.get("limit") or 3), 10))
    except (ValueError, TypeError):
        limit = 3
    logs = []

    if AI_ECO_BLOGS_DIR.exists():
        for md_file in sorted(AI_ECO_BLOGS_DIR.glob("*.md"), reverse=True):
            try:
                content = md_file.read_text(encoding="utf-8")
                slug = md_file.stem
                post = {"slug": slug, "file": md_file.name}

                frontmatter_match = re.match(r"^\s*---\s*[\r\n]+(.*?)\r?\n---\s*[\r\n]+(.*)", content, re.DOTALL)
                if frontmatter_match:
                    fm_text = frontmatter_match.group(1)
                    body = frontmatter_match.group(2)
                    for line in fm_text.splitlines():
                        if ":" in line:
                            k, v = line.split(":", 1)
                            k = k.strip().lower()
                            v = v.strip().strip('"').strip("'")
                            if k == "tags":
                                post["tags"] = [t.strip() for t in v.split(",") if t.strip()]
                            else:
                                post[k] = v
                    post["preview"] = body.strip()[:650] + "..."
                else:
                    post["title"] = slug.replace("-", " ").title()
                    post["tags"] = ["AI Eco", "Agents"]
                    post["preview"] = content.strip()[:650] + "..."

                logs.append(post)
                if len(logs) >= limit:
                    break
            except Exception as e:
                logging.warning(f"Error reading dev log {md_file}: {e}")

    return {
        "count": len(logs),
        "source": "AI_Eco_Blogs/",
        "dev_logs": logs
    }


def handle_get_swarm_memory(args: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch persistent swarm memory from ecosystem_swarm/memory.md with section filtering."""
    args = args or {}
    section = (args.get("section") or "all").strip().lower()

    content = ""
    if SWARM_MEMORY_PATH.exists():
        try:
            content = SWARM_MEMORY_PATH.read_text(encoding="utf-8")
        except Exception as e:
            return {"error": f"Failed reading swarm memory: {e}"}
    else:
        return {"error": "Swarm memory file (ecosystem_swarm/memory.md) not found."}

    if section != "all":
        section_markers = {
            "architecture": "## 🏛️ Core Portfolio Architecture",
            "patterns": "## 💡 Learned Engineering Patterns",
            "constraints": "## ⚠️ Active Constraints & Boundaries",
            "bottlenecks": "## 🔄 Recurring Bottlenecks & Mitigations",
            "goals": "## 🎯 Active Weekly Focus & Strategic Roadmap"
        }
        for key, marker in section_markers.items():
            if key in section and marker in content:
                parts = content.split(marker, 1)
                sub_content = parts[1].split("## ", 1)[0]
                return {
                    "section": key,
                    "marker": marker,
                    "content": f"{marker}\n{sub_content}".strip(),
                    "source": "ecosystem_swarm/memory.md"
                }

    last_consolidated = None
    for line in content.splitlines():
        if "*Last Consolidated:" in line:
            last_consolidated = line.strip().replace("*", "")
            break

    active_goals = []
    if "## 🎯 Active Weekly Focus & Strategic Roadmap" in content:
        goals_part = content.split("## 🎯 Active Weekly Focus & Strategic Roadmap", 1)[1]
        for line in goals_part.splitlines():
            line_s = line.strip()
            import re
            if line_s:
                m = re.match(r'^(\d+\.|\-|\*)\s+(.*)', line_s)
                if m:
                    active_goals.append(m.group(2).strip())

    return {
        "status": "active",
        "last_consolidated": last_consolidated,
        "word_count": len(content.split()),
        "active_weekly_goals": active_goals,
        "living_memory": content,
        "source": "ecosystem_swarm/memory.md"
    }


def handle_get_swarm_daily_views(args: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch recent daily agent debate logs and critiques from ecosystem_swarm/daily_views/."""
    args = args or {}
    try:
        limit = max(1, min(int(args.get("limit") or 3), 14))
    except (ValueError, TypeError):
        limit = 3
    requested_date = args.get("date")

    views = []
    if SWARM_DAILY_DIR.exists():
        if requested_date:
            target = SWARM_DAILY_DIR / f"{requested_date.strip()}.md"
            files_to_read = [target] if target.exists() else []
        else:
            files_to_read = sorted(SWARM_DAILY_DIR.glob("*.md"), reverse=True)[:limit]

        for vf in files_to_read:
            try:
                text = vf.read_text(encoding="utf-8")
                consensus = ""
                if "## 🤝 Collective Swarm Consensus" in text:
                    consensus = text.split("## 🤝 Collective Swarm Consensus", 1)[1].strip()

                views.append({
                    "date": vf.stem,
                    "file": vf.name,
                    "consensus_summary": consensus,
                    "content": text
                })
            except Exception as e:
                logging.warning(f"Error reading daily view {vf}: {e}")

    return {
        "count": len(views),
        "requested_date": requested_date,
        "source": "ecosystem_swarm/daily_views/",
        "daily_views": views
    }


def handle_get_swarm_weekly_meeting(args: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch latest or specific weekly swarm alignment council minutes from ecosystem_swarm/weekly_meetings/."""
    args = args or {}
    requested_week = args.get("week")

    if not SWARM_WEEKLY_DIR.exists():
        return {"error": "Weekly meetings directory (ecosystem_swarm/weekly_meetings/) not found."}

    meeting_file = None
    if requested_week:
        target = SWARM_WEEKLY_DIR / f"{requested_week.strip()}.md"
        if target.exists():
            meeting_file = target
    else:
        meetings = sorted(SWARM_WEEKLY_DIR.glob("*.md"), reverse=True)
        if meetings:
            meeting_file = meetings[0]

    if not meeting_file or not meeting_file.exists():
        return {"error": f"Weekly meeting for '{requested_week}' not found." if requested_week else "No weekly meetings found."}

    try:
        text = meeting_file.read_text(encoding="utf-8")
        roadmap = []
        if "## 🎯 Next-Week Strategic Roadmap" in text:
            roadmap_part = text.split("## 🎯 Next-Week Strategic Roadmap", 1)[1]
            for line in roadmap_part.splitlines():
                line_s = line.strip()
                import re
                if line_s:
                    m = re.match(r'^(\d+\.|\-|\*)\s+(.*)', line_s)
                    if m:
                        roadmap.append(m.group(2).strip())

        return {
            "week": meeting_file.stem,
            "file": meeting_file.name,
            "strategic_roadmap": roadmap,
            "minutes": text,
            "source": "ecosystem_swarm/weekly_meetings/"
        }
    except Exception as e:
        return {"error": f"Error reading meeting {meeting_file}: {e}"}

def handle_resource_read(uri: str) -> Dict[str, Any]:
    uri = (uri or "").strip().lower()
    if uri == "eco://swarm/memory":
        memory_content = ""
        if SWARM_MEMORY_PATH.exists():
            try:
                memory_content = SWARM_MEMORY_PATH.read_text(encoding="utf-8")
            except Exception as e:
                memory_content = f"Error reading swarm memory: {e}"
        return {
            "contents": [
                {
                    "uri": "eco://swarm/memory",
                    "mimeType": "text/markdown",
                    "text": memory_content
                }
            ]
        }
    elif uri == "eco://telemetry":
        data = handle_ai_eco_telemetry({})
        return {
            "contents": [
                {
                    "uri": "eco://telemetry",
                    "mimeType": "application/json",
                    "text": json.dumps(data, indent=2)
                }
            ]
        }
    elif uri == "portfolio://profile":
        data = handle_my_profile({})
        return {
            "contents": [
                {
                    "uri": "portfolio://profile",
                    "mimeType": "application/json",
                    "text": json.dumps(data, indent=2)
                }
            ]
        }
    elif uri == "portfolio://resume":
        data = handle_my_resume({"section": "all"})
        return {
            "contents": [
                {
                    "uri": "portfolio://resume",
                    "mimeType": "application/json",
                    "text": json.dumps(data, indent=2)
                }
            ]
        }
    elif uri == "portfolio://skills":
        data = handle_my_skills({"category": "all"})
        return {
            "contents": [
                {
                    "uri": "portfolio://skills",
                    "mimeType": "application/json",
                    "text": json.dumps(data, indent=2)
                }
            ]
        }
    return {
        "error": f"Resource with URI '{uri}' not found. Available: {[r['uri'] for r in MCP_RESOURCES]}"
    }


def handle_prompt_get(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    name = (name or "").strip().lower()
    args = arguments or {}
    if name == "evaluate_candidate":
        role_title = args.get("role_title", "Staff AI Engineer")
        requirements = args.get("requirements", "Autonomous Multi-Agent AI Swarms, FastMCP, LLM Fine-Tuning")
        return {
            "description": f"Candidate alignment evaluation for {role_title}",
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please evaluate Prashanth Kumar Kadasi's fit for the role of '{role_title}'.\nRequirements:\n{requirements}\n\nPlease analyze skills, verified projects (Solari, BrandXY 20B, Drug Discovery GPT, AI Eco), and highlight interview talking points using the 'evaluate_job_match' tool."
                    }
                }
            ]
        }
    elif name == "ai_eco_overview":
        return {
            "description": "Overview of Prashanth's 6-agent autonomous AI swarm",
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "Explain the architecture of Prashanth's autonomous AI Eco swarm. Inspect its 6 specialized agents (GitHub Scout, Dashboard Agent, Portfolio Sync, MCP Engineer, Docs Agent, Readme Agent) and summarize how they maintain the site and dev logs daily without manual intervention."
                    }
                }
            ]
        }
    elif name == "analyze_ecosystem_telemetry":
        focus = args.get("focus", "all")
        telemetry = handle_ai_eco_telemetry({})
        return {
            "description": "In-depth telemetry analysis of the AI Eco multi-agent swarm",
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Here is the real-time telemetry from Prashanth's AI Eco swarm:\n{json.dumps(telemetry, indent=2)}\n\nPlease provide a technical analysis focusing on '{focus}'. Evaluate developer velocity, language balance across projects, and market compensation alignment."
                    }
                }
            ]
        }
    elif name == "explain_agent_skill":
        agent_id = args.get("agent_id", "github_scout")
        agent_info = next((a for a in AI_ECO_SWARM if a["id"] == agent_id), AI_ECO_SWARM[0])
        return {
            "description": f"Deep-dive into the custom skill and role of {agent_info['name']}",
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Explain the custom skill '{agent_info.get('custom_skill')}' operated by '{agent_info.get('name')}'.\nRole: {agent_info.get('role')}\nOutput target: {agent_info.get('output_target')}\nModel routing: {agent_info.get('primary_model')} -> {agent_info.get('fallback_model')}\n\nHow does this agent contribute to the autonomous multi-agent ecosystem and maintain zero manual overhead?"
                    }
                }
            ]
        }
    return {"error": f"Prompt '{name}' not found. Available: {[p['name'] for p in MCP_PROMPTS]}"}


# ═══════════════════════════════════════════════════════════════
# JSON-RPC 2.0 PROTOCOL ENGINE & ROUTER
# ═══════════════════════════════════════════════════════════════

def process_mcp_request(req_body: Dict[str, Any]):
    """Universal MCP Processor compliant with Model Context Protocol 2024-11-05 spec."""
    if not isinstance(req_body, dict):
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error: Invalid JSON payload."}}

    method = req_body.get("method", "")
    params = req_body.get("params") or {}
    req_id = req_body.get("id")

    # 1. MCP Initialization Handshake
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {"listChanged": False},
                    "resources": {"subscribe": False, "listChanged": False},
                    "prompts": {"listChanged": False}
                },
                "serverInfo": {
                    "name": "kprsnt-all-in-one-mcp",
                    "version": "3.0.0",
                    "description": "Prashanth's All-In-One Model Context Protocol (MCP) Server: My Site, My Data & AI Eco"
                }
            }
        }

    # 2. Notifications (No response permitted per JSON-RPC 2.0 / MCP spec)
    elif method.startswith("notifications/") or req_id is None:
        return None

    # 3. Liveness Ping
    elif method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}

    # 4. Tools Discovery
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": MCP_TOOLS}
        }

    # 5. Tool Execution
    elif method == "tools/call":
        tool_name = params.get("name", "")
        args = params.get("arguments") or {}

        handlers = {
            # Site Tools
            "get_site_overview": handle_site_overview,
            "get_site_projects": handle_site_projects,
            "query_portfolio_projects": handle_site_projects,  # Alias

            # Data Tools
            "get_my_profile": handle_my_profile,
            "get_my_resume": handle_my_resume,
            "get_my_skills": handle_my_skills,
            "get_skills_matrix": handle_my_skills,             # Alias
            "evaluate_job_match": handle_evaluate_job_match,
            "calculate_role_fit": handle_evaluate_job_match,    # Alias

            # AI Eco Tools
            "get_ai_eco_telemetry": handle_ai_eco_telemetry,
            "get_ecosystem_telemetry": handle_ai_eco_telemetry, # Alias
            "get_ai_eco_agents": handle_ai_eco_agents,
            "get_agent_swarm_status": handle_ai_eco_agents,     # Alias
            "get_ai_eco_dev_logs": handle_ai_eco_dev_logs,
            "get_recent_dev_logs": handle_ai_eco_dev_logs,      # Alias
            # Swarm Memory & Council Tools
            "get_swarm_memory": handle_get_swarm_memory,
            "get_living_memory": handle_get_swarm_memory,       # Alias
            "get_swarm_daily_views": handle_get_swarm_daily_views,
            "get_daily_agent_views": handle_get_swarm_daily_views, # Alias
            "get_swarm_weekly_meeting": handle_get_swarm_weekly_meeting,
            "get_weekly_council_minutes": handle_get_swarm_weekly_meeting, # Alias
        }
        if tool_name in handlers:
            try:
                tool_res = handlers[tool_name](args)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(tool_res, indent=2)
                            }
                        ],
                        "isError": False
                    }
                }
            except Exception as ex:
                logging.error(f"Error executing MCP tool '{tool_name}': {ex}")
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Error executing tool '{tool_name}': {str(ex)}"}],
                        "isError": True
                    }
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Tool '{tool_name}' not found. Available: {list(handlers.keys())}"}
            }

    # 6. Resources Discovery & Reading
    elif method == "resources/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"resources": MCP_RESOURCES}}

    elif method == "resources/read":
        uri = params.get("uri", "")
        res = handle_resource_read(uri)
        if "error" in res:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": res["error"]}}
        return {"jsonrpc": "2.0", "id": req_id, "result": res}

    # 7. Prompts Discovery & Getting
    elif method == "prompts/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"prompts": MCP_PROMPTS}}

    elif method == "prompts/get":
        prompt_name = params.get("name", "")
        prompt_args = params.get("arguments") or {}
        res = handle_prompt_get(prompt_name, prompt_args)
        if "error" in res:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": res["error"]}}
        return {"jsonrpc": "2.0", "id": req_id, "result": res}

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32600, "message": f"Unsupported method '{method}'."}
    }


if __name__ == "__main__":
    import sys
    # Read JSON-RPC lines from stdin (Stdio MCP mode for Claude Desktop / Cursor)
    for line in sys.stdin:
        if line.strip():
            try:
                data = json.loads(line)
                response = process_mcp_request(data)
                if response is not None:
                    sys.stdout.write(json.dumps(response) + "\n")
                    sys.stdout.flush()
            except Exception as e:
                err_res = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
                sys.stdout.write(json.dumps(err_res) + "\n")
                sys.stdout.flush()
