#!/usr/bin/env python3
"""
Ecosystem Agents Orchestrator
Runs daily via GitHub Actions to fetch GitHub stats, update telemetry, and generate a blog draft.
"""
import os
import sys
import json
import httpx
from datetime import datetime
from pathlib import Path

# Add project root to path for ai_config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from api.ai_config import call_llm
except ImportError:
    print("Warning: Could not import ai_config. AI generation may fail.")
    call_llm = None

BASE_DIR = Path(__file__).resolve().parent.parent
TELEMETRY_PATH = BASE_DIR / "job_data" / "ecosystem_telemetry.json"
INPUTS_DIR = BASE_DIR / "blog_inputs"
GITHUB_USER = "kprsnt2"

def fetch_github_stats():
    """Fetch repos and recent activity for the user."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
        
    print(f"Fetching GitHub stats for {GITHUB_USER}...")
    try:
        # Fetch repos
        repos_url = f"https://api.github.com/users/{GITHUB_USER}/repos?sort=updated&per_page=100"
        repos_resp = httpx.get(repos_url, headers=headers, timeout=10.0)
        repos = repos_resp.json() if repos_resp.status_code == 200 else []
        
        # Calculate stats
        repo_count = len(repos)
        languages = {}
        
        for r in repos:
            if isinstance(r, dict):
                lang = r.get("language")
                if lang:
                    languages[lang] = languages.get(lang, 0) + 1
        
        # Sort languages
        sorted_langs = dict(sorted(languages.items(), key=lambda item: item[1], reverse=True)[:5])

        # Fetch recent events (commits within last 24 hours)
        events_url = f"https://api.github.com/users/{GITHUB_USER}/events?per_page=50"
        events_resp = httpx.get(events_url, headers=headers, timeout=10.0)
        events = events_resp.json() if events_resp.status_code == 200 else []
        
        recent_activity = []
        now = datetime.utcnow()
        for ev in events:
            if isinstance(ev, dict):
                created_at_str = ev.get("created_at")
                if not created_at_str:
                    continue
                created_at = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ")
                if (now - created_at).total_seconds() < 86400: # Last 24 hours
                    if ev.get("type") == "PushEvent":
                        repo_name = ev.get("repo", {}).get("name", "unknown")
                        commits = ev.get("payload", {}).get("commits", [])
                        for c in commits:
                            recent_activity.append(f"Pushed to {repo_name}: {c.get('message')}")
                    elif ev.get("type") == "CreateEvent":
                        repo_name = ev.get("repo", {}).get("name", "unknown")
                        ref_type = ev.get("payload", {}).get("ref_type", "")
                        if ref_type == "repository":
                            recent_activity.append(f"Created new repository: {repo_name}")
        
        return {
            "repo_counts": repo_count,
            "language_breakdown": sorted_langs,
            "commit_history": repo_count * 15, # Rough estimation for dashboard visual
            "recent_activity": recent_activity
        }
    except Exception as e:
        print(f"Error fetching GitHub stats: {e}")
        return None

def update_telemetry(stats):
    """Update the job_data/ecosystem_telemetry.json file with new stats and AI salary estimation."""
    if not stats:
        return
        
    print("Updating telemetry...")
    
    # AI Salary Estimation based on stats
    salary_est = {"min": 120000, "max": 150000, "reasoning": "Based on Multi-Agent Architecture and Python/Data skills"}
    if call_llm:
        prompt = f"Given a developer with {stats['repo_counts']} repos, top languages {list(stats['language_breakdown'].keys())}, building AI multi-agent ecosystems. Output ONLY a JSON with min, max (numbers), and reasoning (string) for a US salary."
        try:
            res = call_llm(prompt, json_mode=True)
            salary_est = json.loads(res)
        except Exception as e:
            print(f"LLM Salary estimation failed: {e}")
    
    telemetry = {
        "last_updated": datetime.now().isoformat(),
        "commit_history": stats["commit_history"],
        "repo_counts": stats["repo_counts"],
        "language_breakdown": stats["language_breakdown"],
        "live_salary_estimation": salary_est,
        "top_skills": ["Multi-Agent AI", "Model Context Protocol (MCP)", "BigQuery", "Python", "Flask", "GitHub Actions"],
        "mcp_endpoints_active": 4,
        "automations_running": 12,
        "sectors_impacted": ["Healthcare / Pharma", "E-commerce", "Insurance", "Education", "SaaS"]
    }
    
    TELEMETRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TELEMETRY_PATH, "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=2)
    print("Telemetry updated.")

def generate_blog_draft(stats):
    """Generate a blog post summarizing the recent activity directly to blog_inputs."""
    if not stats or not call_llm:
        return
        
    print("Generating blog post...")
    activity_summary = "\\n".join(stats.get('recent_activity', []))
    if not activity_summary:
        activity_summary = "No public commits in the last 24 hours. Focused on architecture, private repos, or reading documentation."

    prompt = f"""Write a polished technical blog post summarizing my development progress over the last 24 hours.
Here is the raw activity log from my GitHub over the past 24 hours:
{activity_summary}

Include exactly this YAML frontmatter at the top:
---
title: "GitHub Scout: Daily Progress & Commits"
date: "{datetime.now().strftime('%d %B %Y')}"
category: "Technology"
tags: "GitHub, AI, Open Source, Daily Update"
excerpt: "An automated summary of my open source commits and progress over the last 24 hours."
---

After the frontmatter, start with exactly this line:
*Generated by GitHub Scout Agent*

Then write 2-3 engaging paragraphs discussing the specific commits and activity listed above. If there are no commits, write a paragraph reflecting on strategic planning and architecture work. Do NOT wrap the output in markdown code fences like ```markdown. Return raw markdown text."""
    
    try:
        draft = call_llm(prompt, temperature=0.7)
        if draft:
            INPUTS_DIR.mkdir(parents=True, exist_ok=True)
            draft_path = INPUTS_DIR / f"github-activity-{datetime.now().strftime('%Y-%m-%d')}.md"
            
            # Clean up code fences if the model still outputs them
            draft_cleaned = draft.strip()
            if draft_cleaned.startswith("```markdown"):
                draft_cleaned = draft_cleaned[11:]
            if draft_cleaned.startswith("```"):
                draft_cleaned = draft_cleaned[3:]
            if draft_cleaned.endswith("```"):
                draft_cleaned = draft_cleaned[:-3]
                
            with open(draft_path, "w", encoding="utf-8") as f:
                f.write(draft_cleaned.strip())
            print(f"Blog post saved to {draft_path}")
    except Exception as e:
        print(f"Blog generation failed: {e}")

def main():
    print("🚀 Starting Ecosystem Agents Orchestrator")
    stats = fetch_github_stats()
    if stats:
        update_telemetry(stats)
        generate_blog_draft(stats)
    print("✅ Ecosystem sync complete!")

if __name__ == "__main__":
    main()
