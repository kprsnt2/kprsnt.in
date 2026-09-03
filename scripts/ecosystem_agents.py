#!/usr/bin/env python3
"""
Ecosystem Agents Orchestrator
Runs daily via GitHub Actions to fetch GitHub stats, update telemetry, and generate a blog draft.
"""
import os
import sys
import json
import httpx
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path for ai_config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from api.ai_config import call_llm
except ImportError:
    try:
        from scripts.ai_config import call_llm
    except ImportError:
        print("Warning: Could not import ai_config. AI generation may fail.")
        call_llm = None

BASE_DIR = Path(__file__).resolve().parent.parent
TELEMETRY_PATH = BASE_DIR / "job_data" / "ecosystem_telemetry.json"
INPUTS_DIR = BASE_DIR / "AI_Eco_Blogs"
GITHUB_USER = "kprsnt2"

def get_auth_headers():
    """Get standard GitHub headers, with token if available."""
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "kprsnt-ecosystem-agent"
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    return headers

def fetch_github_stats():
    """Fetch repos and recent activity for the user."""
    headers = get_auth_headers()
        
    print(f"Fetching GitHub stats for {GITHUB_USER}...")
    try:
        # 1. Fetch repos
        repos_url = f"https://api.github.com/users/{GITHUB_USER}/repos?sort=updated&per_page=100"
        repos_resp = httpx.get(repos_url, headers=headers, timeout=15.0)
        # If auth token failed, retry without auth
        if repos_resp.status_code in (401, 403):
            repos_resp = httpx.get(repos_url, headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "kprsnt-ecosystem-agent"}, timeout=15.0)
        repos = repos_resp.json() if repos_resp.status_code == 200 else []
        
        repo_count = len(repos)
        languages = {}
        for r in repos:
            if isinstance(r, dict):
                lang = r.get("language")
                if lang:
                    languages[lang] = languages.get(lang, 0) + 1
        sorted_langs = dict(sorted(languages.items(), key=lambda item: item[1], reverse=True)[:5])

        # 2. Fetch recent events (up to 100 events)
        events_url = f"https://api.github.com/users/{GITHUB_USER}/events?per_page=100"
        events_resp = httpx.get(events_url, headers=headers, timeout=15.0)
        if events_resp.status_code in (401, 403):
            events_resp = httpx.get(events_url, headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "kprsnt-ecosystem-agent"}, timeout=15.0)
        events = events_resp.json() if events_resp.status_code == 200 else []
        
        recent_activity = []
        seen_commits = set()
        now = datetime.utcnow()

        # Window: last 28 hours to cover daily cron safely across timezones
        for ev in events:
            if not isinstance(ev, dict):
                continue
            created_at_str = ev.get("created_at")
            if not created_at_str:
                continue
            created_at = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ")
            if (now - created_at).total_seconds() <= 100800: # 28 hours
                ev_type = ev.get("type")
                repo_name = ev.get("repo", {}).get("name", "unknown")
                payload = ev.get("payload", {})

                if ev_type == "PushEvent":
                    ref = payload.get("ref", "").replace("refs/heads/", "")
                    commits = payload.get("commits", [])
                    
                    if commits:
                        for c in commits:
                            msg = c.get("message", "").strip().split("\n")[0]
                            sha = c.get("sha", "")[:7]
                            if msg and sha not in seen_commits:
                                seen_commits.add(sha)
                                recent_activity.append(f"[{repo_name}] {ref}: {msg}")
                    else:
                        # GitHub public events API omits commits list in payload.
                        # Resolve via commit head SHA:
                        head_sha = payload.get("head")
                        if head_sha and head_sha not in seen_commits:
                            seen_commits.add(head_sha)
                            commit_msg = None
                            try:
                                commit_url = f"https://api.github.com/repos/{repo_name}/commits/{head_sha}"
                                c_resp = httpx.get(commit_url, headers=headers, timeout=8.0)
                                if c_resp.status_code != 200:
                                    # Fallback without auth token for public repos
                                    c_resp = httpx.get(commit_url, headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "kprsnt-ecosystem-agent"}, timeout=8.0)
                                if c_resp.status_code == 200:
                                    c_data = c_resp.json()
                                    commit_msg = c_data.get("commit", {}).get("message", "").strip().split("\n")[0]
                            except Exception as ce:
                                print(f"Warning: Could not fetch commit {head_sha[:7]} for {repo_name}: {ce}")
                            
                            if commit_msg:
                                recent_activity.append(f"[{repo_name}] {ref}: {commit_msg}")
                            else:
                                recent_activity.append(f"[{repo_name}] Pushed commit {head_sha[:7]} to {ref}")

                elif ev_type == "CreateEvent":
                    ref_type = payload.get("ref_type", "")
                    ref_name = payload.get("ref", "")
                    if ref_type == "repository":
                        recent_activity.append(f"Created new repository: {repo_name}")
                    elif ref_type == "branch":
                        recent_activity.append(f"[{repo_name}] Created branch: {ref_name}")

                elif ev_type == "ForkEvent":
                    forkee = payload.get("forkee", {}).get("full_name", "")
                    recent_activity.append(f"Forked {repo_name} to {forkee}")

                elif ev_type == "PullRequestEvent":
                    action = payload.get("action", "")
                    pr_title = payload.get("pull_request", {}).get("title", "")
                    recent_activity.append(f"[{repo_name}] PR {action}: {pr_title}")

        # Baseline contributions: 987 recorded from annual profile + recent activity
        total_commits = max(987, repo_count * 12 + len(recent_activity))

        return {
            "repo_counts": repo_count,
            "language_breakdown": sorted_langs,
            "commit_history": total_commits,
            "recent_activity": recent_activity,
            "active_repos_touched": list(set([a.split("]")[0].replace("[", "") for a in recent_activity if a.startswith("[")]))
        }
    except Exception as e:
        print(f"Error fetching GitHub stats: {e}")
        return None

def update_telemetry(stats):
    """Update the job_data/ecosystem_telemetry.json file with new stats and AI salary estimation."""
    if not stats:
        return
        
    print("Updating telemetry...")
    
    salary_est = {
        "min": 180000,
        "max": 320000,
        "reasoning": "A developer with 100 repositories, strong breadth across TypeScript, JavaScript, Python, and HTML, and specialized experience building AI multi-agent ecosystems fits a senior/staff-level full-stack AI engineer profile."
    }
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
        "top_skills": ["Multi-Agent AI", "Model Context Protocol (MCP)", "BigQuery", "Python", "Flask", "GitHub Actions", "TypeScript"],
        "mcp_endpoints_active": 4,
        "automations_running": 12,
        "sectors_impacted": ["Healthcare / Pharma", "E-commerce", "Insurance", "Education", "SaaS"],
        "recent_activity": stats.get("recent_activity", [])[:10],
        "daily_commits_count": len(stats.get("recent_activity", []))
    }
    
    TELEMETRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TELEMETRY_PATH, "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=2)
    print("Telemetry updated.")

def generate_blog_draft(stats):
    """Generate a blog post summarizing the recent activity directly to blog_inputs. Only publishes if there is activity."""
    if not stats or not call_llm:
        return
        
    recent_activity = stats.get('recent_activity', [])
    if not recent_activity:
        print("ℹ️ No commits or activity in the last 24 hours. Skipping blog publishing.")
        return
        
    print(f"Generating blog post for {len(recent_activity)} recent activity item(s)...")
    activity_summary = "\n".join(recent_activity)

    prompt = f"""You are an expert developer advocate writing a daily dev log for Prashanth (kprsnt2).
Here is the raw activity log from GitHub over the past 24 hours:
{activity_summary}

Write a polished, authentic technical blog post summarizing today's development progress.
Format Requirements:
1. Include exactly this YAML frontmatter at the top:
---
title: "GitHub Scout: [Insert a concise, captivating 4-8 word headline summarizing the primary engineering achievement or repos touched today]"
date: "{datetime.now().strftime('%d %B %Y')}"
category: "Technology"
tags: "GitHub, AI, Open Source, Daily Update, [Add 2-3 relevant technologies touched]"
excerpt: "[1-2 clear sentences summarizing specifically what was built, fixed, or shipped today]"
---

2. Immediately after frontmatter, start with exactly this line:
*Generated by GitHub Scout Agent*

3. Then write 2-3 engaging, technical paragraphs:
- Highlight the exact commits, features, and fixes from the activity log.
- Discuss the technical problems solved (e.g., container/microVM startup, sandbox isolation, API sequencing, UI responsiveness, or serverless configuration).
- Maintain an authentic, engineer-to-engineer tone (humble, detailed, zero fluff).

Do NOT wrap the output in markdown code fences like ```markdown. Return raw markdown text."""
    
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
