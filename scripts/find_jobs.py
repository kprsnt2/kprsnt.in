#!/usr/bin/env python3
"""
AI Job Finder — Gemini + Google Search Grounding
Uses Gemini API with Google Search grounding to find REAL job postings
with verified, working apply URLs from live web search results.

Saves results as JSON to job_data/ for website rendering.
"""
import os
import sys
import json
import re
import urllib.parse
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "job_data"

# Profile to match against
PROFILE = {
    "title": "Data Analyst & AI Developer",
    "location": "Hyderabad, India",
    "remote": True,
    "skills": [
        "Python", "SQL", "BigQuery", "LLM Fine-tuning", "Prompt Engineering",
        "RAG", "Multi-model AI (Gemini, Claude, OpenAI, NVIDIA NIM)",
        "HuggingFace", "PyTorch", "Flask", "React", "Next.js", "Vercel",
        "Data Analysis", "Dashboards", "ETL", "AppScript",
        "Healthcare Data", "Clinical Data Analysis", "Drug Discovery"
    ],
    "experience": [
        "3+ years Data Analyst at Pi-Datametrics",
        "Fine-tuned 20B LLM on AMD MI300X (BrandXY - 76% manipulation rate)",
        "Published models on HuggingFace",
        "10+ deployed AI applications",
        "Drug Discovery AI (M.Pharm background)",
        "MyLocalCLI - agentic AI coding assistant (6 providers, 26 tools)"
    ],
    "education": "M.Pharm - Pharmaceutical Analysis",
    "target_roles": [
        "Senior Data Analyst", "Data Manager",
        "AI Engineer", "LLM Engineer", "Generative AI Developer",
        "LLM Prompt Engineer", "Prompt Engineer",
        "Clinical Data Analyst", "Healthcare Data Manager",
        "ML Engineer", "AI/ML Solutions Engineer",
        "Forward Deployed Engineer", "Pharma + AI roles"
    ],
    "salary_range": "₹10-50 LPA or $30K-80K USD",
    "preferred": "Remote, async-first teams, startups or mid-size companies"
}


def build_search_prompt(role_category, role_names):
    """Build a focused search prompt for a specific role category."""
    today = datetime.now().strftime("%Y-%m-%d")
    month = datetime.now().strftime("%B %Y")

    return f"""Search for 5 real, currently active job openings for: {', '.join(role_names)}

Today's date: {today}

**Requirements for each job:**
1. The job MUST be a real posting found in search results
2. The apply_url MUST be the actual URL to the job posting page (LinkedIn job URL, company careers page, etc.)
3. Focus on remote-friendly or India-based positions
4. Prefer roles posted within the last 30 days

**Candidate context (for match scoring):**
- Skills: {', '.join(PROFILE['skills'][:12])}
- Experience: {'; '.join(PROFILE['experience'][:4])}
- Education: {PROFILE['education']}

**Output Format:**
Return ONLY a valid JSON object:
{{
  "jobs": [
    {{
      "id": "company-role-slug",
      "title": "Exact Job Title from posting",
      "company": "Company Name",
      "company_tag": "",
      "location": "Remote / City",
      "salary": "salary if listed, or empty string",
      "match_score": 85,
      "tier": 1,
      "tags": ["relevant", "skill", "tags"],
      "why_match": "Brief reason this matches the candidate",
      "apply_url": "https://actual-url-to-job-posting",
      "applied": false,
      "status": "new",
      "target_role": "{role_category}"
    }}
  ]
}}

CRITICAL: Every apply_url must be a real URL from your search results. Do NOT fabricate URLs.
Return valid JSON only, no markdown code fences, no extra text."""


def _parse_json_response(text):
    """Parse JSON from AI response, handling code fences."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r'^```\w*\n?', '', text)
        text = re.sub(r'\n?```$', '', text)
        text = text.strip()

    # Try to find JSON object in the text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON from surrounding text
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    return None


def _extract_grounding_urls(response):
    """Extract real URLs from Gemini's grounding metadata."""
    urls = []
    try:
        for candidate in response.candidates:
            metadata = getattr(candidate, 'grounding_metadata', None)
            if not metadata:
                continue
            chunks = getattr(metadata, 'grounding_chunks', None)
            if not chunks:
                continue
            for chunk in chunks:
                web = getattr(chunk, 'web', None)
                if web:
                    uri = getattr(web, 'uri', None)
                    title = getattr(web, 'title', '')
                    if uri:
                        urls.append({"uri": uri, "title": title})
    except Exception:
        pass
    return urls


def _build_google_search_fallback(company, title):
    """Build a Google Search URL as fallback for unverified jobs."""
    query = f"{company} {title} careers apply"
    return f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"


def generate_jobs_for_role(client, role_category, role_names):
    """Generate job listings for a specific role using Gemini with Google Search grounding."""
    from google.genai import types

    prompt = build_search_prompt(role_category, role_names)

    # Configure Google Search grounding
    google_search_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    config = types.GenerateContentConfig(
        tools=[google_search_tool]
    )

    try:
        sys.stdout.write(f"  🔍 Searching for {role_category} roles... ")
        sys.stdout.flush()

        gemini_key_paid = os.environ.get("GEMINI_API_KEY_PAID")
        model_name = "gemini-pro-latest" if gemini_key_paid else "gemini-2.5-flash-lite"
        
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=config
        )

        text = response.text.strip()
        result = _parse_json_response(text)

        # Extract grounding URLs for cross-referencing
        grounding_urls = _extract_grounding_urls(response)

        if result and "jobs" in result and len(result["jobs"]) > 0:
            jobs = result["jobs"]

            # Tag each job with source info
            for job in jobs:
                job["model_source"] = "gemini"
                job["model_name"] = "Gemini (Search Grounded)"

                # Cross-reference apply_url with grounding URLs
                apply_url = job.get("apply_url", "")
                is_grounded = False
                if apply_url and grounding_urls:
                    for g_url in grounding_urls:
                        # Check if any grounding URL domain matches the apply URL
                        try:
                            apply_domain = urllib.parse.urlparse(apply_url).netloc.lower()
                            grounding_domain = urllib.parse.urlparse(g_url["uri"]).netloc.lower()
                            if apply_domain and grounding_domain and (
                                apply_domain in grounding_domain or grounding_domain in apply_domain
                            ):
                                is_grounded = True
                                break
                        except Exception:
                            continue

                job["url_grounded"] = is_grounded

            print(f"✅ Found {len(jobs)} jobs ({sum(1 for j in jobs if j.get('url_grounded'))} grounded)")
            return jobs
        else:
            print(f"⚠️  No jobs found")
            return []

    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def verify_jobs(jobs):
    """Verify job listing URLs are still active via HTTP HEAD requests."""
    print("  🔎 Verifying job URLs...")

    try:
        import httpx
    except ImportError:
        print("  ⚠️  httpx not installed, marking all as unverified")
        for job in jobs:
            job["verified"] = False
            job["last_verified"] = datetime.now().strftime("%Y-%m-%d")
        return jobs

    verified = 0
    failed = 0

    with httpx.Client(
        timeout=15,
        follow_redirects=True,
        headers={"User-Agent": "Mozilla/5.0 (compatible; JobVerifier/1.0)"}
    ) as client:
        for job in jobs:
            url = job.get("apply_url", "")
            if not url or url == "#" or "google.com/search" in url:
                job["verified"] = False
                job["last_verified"] = datetime.now().strftime("%Y-%m-%d")
                failed += 1
                continue

            try:
                # Try HEAD first, fall back to GET if HEAD fails
                resp = client.head(url)
                if resp.status_code == 405:  # Method not allowed
                    resp = client.get(url)

                is_active = resp.status_code < 400
                job["verified"] = is_active
                job["last_verified"] = datetime.now().strftime("%Y-%m-%d")
                if is_active:
                    verified += 1
                else:
                    failed += 1
                    # Add Google Search fallback for failed URLs
                    job["search_url"] = _build_google_search_fallback(
                        job.get("company", ""), job.get("title", "")
                    )
                    print(f"    ⚠️  {job['company']} — HTTP {resp.status_code}")
            except Exception as e:
                job["verified"] = False
                job["last_verified"] = datetime.now().strftime("%Y-%m-%d")
                job["search_url"] = _build_google_search_fallback(
                    job.get("company", ""), job.get("title", "")
                )
                failed += 1
                print(f"    ⚠️  {job['company']} — {str(e)[:60]}")

    print(f"  ✅ Verified: {verified} active, {failed} failed/unreachable")
    return jobs


def deduplicate_jobs(all_jobs):
    """Remove duplicate jobs across searches based on company+title similarity."""
    seen = {}
    unique_jobs = []

    for job in all_jobs:
        key = f"{job.get('company', '').lower().strip()}-{job.get('title', '').lower().strip()}"
        if key not in seen:
            seen[key] = True
            unique_jobs.append(job)

    return unique_jobs


def merge_with_existing(new_data):
    """Merge new jobs with existing data, preserving 'applied' status."""
    month_slug = datetime.now().strftime("%B-%Y").lower()
    output_path = OUTPUT_DIR / f"{month_slug}.json"

    if output_path.exists():
        try:
            existing = json.loads(output_path.read_text(encoding="utf-8"))
            existing_jobs = {j["id"]: j for j in existing.get("jobs", [])}

            for job in new_data.get("jobs", []):
                if job["id"] in existing_jobs:
                    old = existing_jobs[job["id"]]
                    job["applied"] = old.get("applied", False)
                    job["status"] = old.get("status", "new")
                    if old.get("cover_letter"):
                        job["cover_letter"] = old["cover_letter"]
                    if old.get("verified") is not None:
                        job["verified"] = old["verified"]
                        job["last_verified"] = old.get("last_verified", "")

            print(f"  🔄 Merged with existing data ({len(existing_jobs)} existing jobs)")
        except Exception as e:
            print(f"  ⚠️  Could not merge: {e}")

    return new_data


def main():
    """Main entry point."""
    print("🔍 AI Job Finder — Gemini + Google Search Grounding")
    print(f"   Output: {OUTPUT_DIR}")
    print(f"   Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    # Check API key
    gemini_key_paid = os.environ.get("GEMINI_API_KEY_PAID")
    gemini_key_free = os.environ.get("GEMINI_API_KEY")
    api_key = gemini_key_paid or gemini_key_free
    if not api_key:
        print("  ❌ GEMINI API key not set. Set GEMINI_API_KEY_PAID or GEMINI_API_KEY.")
        sys.exit(1)

    try:
        from google import genai
    except ImportError:
        print("  ❌ google-genai package not installed. Run: pip install google-genai")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    # Define role categories to search
    role_categories = [
        ("senior-data-analyst", ["Senior Data Analyst", "Lead Data Analyst", "Data Analyst Remote"]),
        ("data-manager", ["Data Manager", "Data Operations Manager", "Analytics Manager"]),
        ("ai-engineer", ["AI Engineer", "LLM Engineer", "Generative AI Developer", "ML Engineer"]),
        ("prompt-engineer", ["Prompt Engineer", "AI Prompt Engineer", "LLM Prompt Engineer"]),
        ("clinical-healthcare", ["Clinical Data Analyst", "Healthcare Data Analyst", "Pharma AI", "Drug Discovery AI"]),
    ]

    all_jobs = []

    # Search for each role category separately for better results
    print("📡 Searching with Gemini + Google Search Grounding")
    for role_category, role_names in role_categories:
        jobs = generate_jobs_for_role(client, role_category, role_names)
        all_jobs.extend(jobs)

    if not all_jobs:
        print("\n  ❌ Failed to find any jobs")
        sys.exit(1)

    # Deduplicate across categories
    print(f"\n🔧 Processing")
    print(f"  📊 Raw jobs from all searches: {len(all_jobs)}")
    all_jobs = deduplicate_jobs(all_jobs)
    print(f"  📊 After deduplication: {len(all_jobs)}")

    # Sort by match score
    all_jobs.sort(key=lambda j: j.get("match_score", 0), reverse=True)

    # Build result
    today = datetime.now().strftime("%Y-%m-%d")
    month = datetime.now().strftime("%B %Y")
    result = {
        "month": month,
        "generated_date": today,
        "profile_summary": "Data Analyst & AI Developer | LLM Fine-tuning | Python | Multi-model AI",
        "models_used": {"gemini_grounded": len(all_jobs)},
        "jobs": all_jobs
    }

    # Merge with existing data
    result = merge_with_existing(result)

    # Verify job URLs
    result["jobs"] = verify_jobs(result.get("jobs", []))

    # Save
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    month_slug = datetime.now().strftime("%B-%Y").lower()
    output_path = OUTPUT_DIR / f"{month_slug}.json"
    output_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    # Summary
    total = len(result.get("jobs", []))
    verified_count = sum(1 for j in result.get("jobs", []) if j.get("verified"))
    grounded_count = sum(1 for j in result.get("jobs", []) if j.get("url_grounded"))

    print(f"\n  💾 Saved: {output_path.name}")
    print(f"  📊 {total} jobs found for {month}")
    print(f"  ✅ {verified_count} verified active | 🔗 {grounded_count} search-grounded")


if __name__ == "__main__":
    main()
