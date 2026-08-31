#!/usr/bin/env python3
"""
MCP Job Server — Model Context Protocol server for AI Job Finder
Exposes tools for searching, verifying, and preparing job applications.

Run: python scripts/job_server.py
Or:  mcp run scripts/job_server.py
"""
import os
import sys
import json
import re
import httpx
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'api' / 'data'))
from portfolio_kb import get_mcp_profile

from mcp.server.fastmcp import FastMCP

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
JOB_DATA_DIR = BASE_DIR / "job_data"

# Initialize MCP server
mcp = FastMCP("AI Job Finder")

# --- Candidate Profile (loaded from portfolio knowledge base) ---
PROFILE = get_mcp_profile()


def _load_all_jobs():
    """Load all job listings from job_data/."""
    jobs = []
    if JOB_DATA_DIR.exists():
        for json_file in sorted(JOB_DATA_DIR.glob("*.json"), reverse=True):
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                for job in data.get("jobs", []):
                    job["_source_file"] = json_file.name
                    jobs.append(job)
            except Exception:
                continue
    return jobs


def _save_jobs(jobs, source_file=None):
    """Save jobs back to their source JSON file."""
    if not source_file:
        source_file = datetime.now().strftime("%B-%Y").lower() + ".json"
    
    filepath = JOB_DATA_DIR / source_file
    if filepath.exists():
        data = json.loads(filepath.read_text(encoding="utf-8"))
    else:
        data = {
            "month": datetime.now().strftime("%B %Y"),
            "generated_date": datetime.now().strftime("%Y-%m-%d"),
            "profile_summary": PROFILE["title"],
            "jobs": []
        }
    
    # Update jobs in the file
    job_map = {j["id"]: j for j in jobs if j.get("_source_file") == source_file}
    for i, existing in enumerate(data["jobs"]):
        if existing["id"] in job_map:
            updated = job_map[existing["id"]]
            updated.pop("_source_file", None)
            data["jobs"][i] = updated
    
    filepath.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


# ============ MCP TOOLS ============

@mcp.tool()
def get_profile() -> str:
    """Get the candidate's full profile including skills, experience, projects, and target roles."""
    return json.dumps(PROFILE, indent=2)


@mcp.tool()
def list_current_jobs(tier: int = 0, status: str = "") -> str:
    """List all current job listings from the job finder.
    
    Args:
        tier: Filter by tier (1 or 2). Use 0 for all tiers.
        status: Filter by status ('new', 'applied', 'verified'). Empty for all.
    """
    jobs = _load_all_jobs()
    
    if tier > 0:
        jobs = [j for j in jobs if j.get("tier") == tier]
    if status:
        jobs = [j for j in jobs if j.get("status") == status]
    
    # Clean internal fields
    for j in jobs:
        j.pop("_source_file", None)
    
    return json.dumps({
        "total": len(jobs),
        "jobs": jobs
    }, indent=2)


@mcp.tool()
def search_jobs(query: str = "AI Engineer LLM Remote India", max_results: int = 15) -> str:
    """Search for new job openings using AI with web search.
    Returns real job listings with verified URLs from live web search results.
    
    Args:
        query: Search query like 'AI Engineer LLM Remote India' or 'Pharma AI Drug Discovery'
        max_results: Maximum number of results (5-20)
    """
    try:
        from ai_config import get_openai_client, OPENAI_MODEL
        client = get_openai_client()
        
        prompt = f"""Search for {max_results} real, currently active job openings matching: "{query}"

Candidate: {PROFILE['title']} with skills in {', '.join(PROFILE['skills'][:8])}

CRITICAL: Every apply_url MUST be a real URL from your search results. Do NOT fabricate URLs.

Return ONLY valid JSON:
{{"jobs": [{{"id": "slug", "title": "Job Title", "company": "Company", "company_tag": "", "location": "Remote", "salary": "", "match_score": 85, "tier": 1, "tags": ["tag1"], "why_match": "reason", "apply_url": "https://actual-url-from-search", "applied": false, "status": "new"}}]}}"""

        # Use OpenAI with web search tool
        response = client.responses.create(
            model=OPENAI_MODEL,
            tools=[{"type": "web_search_preview"}],
            input=prompt
        )
        text = response.output_text.strip()
        if text.startswith("```"):
            text = re.sub(r'^```\w*\n?', '', text)
            text = re.sub(r'\n?```$', '', text)
        
        result = json.loads(text.strip())
        return json.dumps({"found": len(result.get("jobs", [])), "jobs": result.get("jobs", [])}, indent=2)
    
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def verify_jobs(job_ids: list[str] = None) -> str:
    """Verify if job listings are still active by checking their URLs.
    
    Args:
        job_ids: List of job IDs to verify. If empty, verifies all jobs.
    """
    jobs = _load_all_jobs()
    
    if job_ids:
        jobs = [j for j in jobs if j.get("id") in job_ids]
    
    results = []
    with httpx.Client(timeout=10, follow_redirects=True) as client:
        for job in jobs:
            url = job.get("apply_url", "")
            if not url or url == "#":
                results.append({
                    "id": job["id"], "title": job["title"],
                    "verified": False, "reason": "No valid URL"
                })
                continue
            
            try:
                resp = client.head(url)
                is_active = resp.status_code < 400
                job["verified"] = is_active
                job["last_verified"] = datetime.now().strftime("%Y-%m-%d")
                results.append({
                    "id": job["id"], "title": job["title"],
                    "verified": is_active,
                    "status_code": resp.status_code,
                    "reason": "Active" if is_active else f"HTTP {resp.status_code}"
                })
            except Exception as e:
                job["verified"] = False
                job["last_verified"] = datetime.now().strftime("%Y-%m-%d")
                results.append({
                    "id": job["id"], "title": job["title"],
                    "verified": False, "reason": str(e)[:100]
                })
    
    # Save updated verification status
    _save_jobs(jobs)
    
    verified_count = sum(1 for r in results if r["verified"])
    return json.dumps({
        "total_checked": len(results),
        "verified_active": verified_count,
        "results": results
    }, indent=2)


@mcp.tool()
def generate_cover_letter(job_id: str, tone: str = "professional") -> str:
    """Generate a tailored cover letter or intro message for a specific job listing.
    
    Args:
        job_id: The job ID to generate a cover letter for
        tone: Writing tone - 'professional', 'casual', or 'enthusiastic'
    """
    jobs = _load_all_jobs()
    job = next((j for j in jobs if j.get("id") == job_id), None)
    
    if not job:
        return json.dumps({"error": f"Job '{job_id}' not found. Use list_current_jobs to see available IDs."})
    
    try:
        from ai_config import call_llm
        
        relevant_projects = [p for p in PROFILE["key_projects"] 
                           if any(tag.lower() in p["desc"].lower() for tag in job.get("tags", []))]
        if not relevant_projects:
            relevant_projects = PROFILE["key_projects"][:3]
        
        prompt = f"""Write a {tone}, human-sounding intro message for applying to this job. 
NOT a generic template — reference specific projects and skills that match.

**Job:**
- Title: {job['title']}
- Company: {job['company']} {job.get('company_tag', '')}
- Tags: {', '.join(job.get('tags', []))}
- Why it matches: {job.get('why_match', '')}

**Candidate (Prashanth Kumar):**
- Current: {PROFILE['title']}
- Key Skills: {', '.join(PROFILE['skills'][:10])}
- Relevant Experience: {'; '.join(PROFILE['experience'][:4])}
- Relevant Projects: {json.dumps(relevant_projects)}
- Education: {PROFILE['education']}
- Portfolio: {PROFILE['website']}

Requirements:
1. Keep it under 200 words
2. Sound genuinely human, not AI-generated
3. Reference 2-3 specific projects that relate to the job
4. End with a clear call to action
5. Don't use phrases like "I'm excited" or "I'm passionate" — be concrete instead
6. Return ONLY the message text, no JSON wrapper"""

        cover_letter = call_llm(prompt)
        if not cover_letter:
            return json.dumps({"error": "Failed to generate cover letter — all AI providers failed."})
        cover_letter = cover_letter.strip()
        
        # Save to job data
        job["cover_letter"] = cover_letter
        _save_jobs(jobs, job.get("_source_file"))
        
        return json.dumps({
            "job_id": job_id,
            "company": job["company"],
            "title": job["title"],
            "cover_letter": cover_letter
        }, indent=2)
    
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def mark_applied(job_id: str, notes: str = "") -> str:
    """Mark a job as applied and optionally add notes.
    
    Args:
        job_id: The job ID to mark as applied
        notes: Optional notes about the application (date, platform, etc.)
    """
    jobs = _load_all_jobs()
    job = next((j for j in jobs if j.get("id") == job_id), None)
    
    if not job:
        return json.dumps({"error": f"Job '{job_id}' not found."})
    
    job["applied"] = True
    job["status"] = "applied"
    job["applied_date"] = datetime.now().strftime("%Y-%m-%d")
    if notes:
        job["application_notes"] = notes
    
    _save_jobs(jobs, job.get("_source_file"))
    
    return json.dumps({
        "success": True,
        "job_id": job_id,
        "company": job["company"],
        "title": job["title"],
        "status": "applied",
        "applied_date": job["applied_date"]
    }, indent=2)


# ============ MCP TOOLS ============

@mcp.tool()
def get_ecosystem_telemetry() -> str:
    """Get ecosystem telemetry including commit history, language stats, and live salary estimation."""
    telemetry_file = JOB_DATA_DIR / "ecosystem_telemetry.json"
    if telemetry_file.exists():
        return telemetry_file.read_text(encoding="utf-8")
    return json.dumps({"error": "ecosystem_telemetry.json not found"})


# ============ MCP RESOURCES ============

@mcp.resource("jobs://profile")
def profile_resource() -> str:
    """Candidate profile as a resource."""
    return json.dumps(PROFILE, indent=2)


@mcp.resource("jobs://listings")
def listings_resource() -> str:
    """All current job listings as a resource."""
    jobs = _load_all_jobs()
    for j in jobs:
        j.pop("_source_file", None)
    return json.dumps(jobs, indent=2)


# ============ MCP PROMPTS ============

@mcp.prompt()
def job_search_prompt(role: str = "AI Engineer") -> str:
    """A prompt template for finding jobs matching a specific role."""
    return f"""Find current remote job openings for a {role} with these skills:
{', '.join(PROFILE['skills'][:8])}

The candidate has {PROFILE['experience'][0]} and has {PROFILE['experience'][1]}.
Education: {PROFILE['education']}

Please search for jobs and then verify the top results."""


@mcp.prompt()
def weekly_review_prompt() -> str:
    """A prompt for the weekly job review workflow."""
    return """Please help me with my weekly job search:
1. First, list my current jobs with list_current_jobs
2. Verify all listings are still active with verify_jobs  
3. Search for new jobs matching my profile with search_jobs
4. For any new Tier 1 matches, generate cover letters with generate_cover_letter
5. Give me a summary of what to apply to this weekend"""


if __name__ == "__main__":
    mcp.run()
