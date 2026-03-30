#!/usr/bin/env python3
"""
AI Job Finder — Multi-Model Edition
Uses multiple AI models via NVIDIA NIM API to search and curate job openings.
Models: GLM-5, Kimi-2.5, Step-3.5-Flash (all via NVIDIA NIM)
Fallback: Gemini, Claude
Saves results as JSON to job_data/ for website rendering.
"""
import os
import sys
import json
import re
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

# NVIDIA NIM Models Configuration
NVIDIA_MODELS = [
    {
        "id": "z-ai/glm5",
        "name": "GLM-5",
        "source_tag": "glm5",
        "color": "#76b900"  # NVIDIA green
    },
    {
        "id": "moonshotai/kimi-k2.5",
        "name": "Kimi 2.5",
        "source_tag": "kimi",
        "color": "#6366f1"  # Indigo
    },
    {
        "id": "stepfun-ai/step-3.5-flash",
        "name": "Step 3.5 Flash",
        "source_tag": "step",
        "color": "#f59e0b"  # Amber
    }
]


def build_prompt(model_name="AI"):
    """Build the AI prompt for job search."""
    today = datetime.now().strftime("%Y-%m-%d")
    month = datetime.now().strftime("%B %Y")
    return f"""You are an AI job search assistant. Find and curate current remote job openings that match this profile.
IMPORTANT: Focus on jobs posted or actively hiring in the LAST 24 HOURS (today is {today}). Do NOT hallucinate jobs. Every job you return MUST be real and currently active.

**Candidate Profile:**
- Title: {PROFILE['title']}
- Location: {PROFILE['location']} (prefers remote)
- Key Skills: {', '.join(PROFILE['skills'])}
- Experience: {'; '.join(PROFILE['experience'])}
- Education: {PROFILE['education']}
- Target Roles: {', '.join(PROFILE['target_roles'])}

**Instructions:**
1. Search for real, authentic, and currently hiring positions from {month}. 
2. Search specifically on these platforms: LinkedIn, Indeed, YC Combinator, Glassdoor, remote hiring sites, startup career pages. Also search X (Twitter) or other social media posts with hiring announcements for the job role names.
3. EVERY single job MUST include a real, valid, and working `apply_url` link to the actual job posting. Do NOT provide fake, broken, or placeholder links. This is the most critical requirement.
4. Focus on remote-friendly roles in India or worldwide.
5. Match roles based on skills overlap.
6. IMPORTANT: You MUST generate EXACTLY 5 matching jobs for EACH of the following 5 target roles (totaling exactly 25 jobs):
   - Senior Data Analyst
   - Data Manager
   - AI Engineer
   - Prompt Engineer
   - Clinical/Healthcare Data Analyst
7. Include a mix of strong matches (Tier 1) and good matches (Tier 2).
8. For each job, calculate a match_score (0-100) based on skill overlap.
9. The candidate's Pharma + AI combo is UNIQUE — always include pharma+AI roles for the Clinical/Healthcare target role.

**Output Format:**
Return ONLY a valid JSON object with this structure:
{{
  "month": "{month}",
  "generated_date": "{today}",
  "profile_summary": "Data Analyst & AI Developer | LLM Fine-tuning | Python | Multi-model AI",
  "jobs": [
    {{
      "id": "company-role-slug",
      "title": "Job Title",
      "company": "Company Name",
      "company_tag": "YC W22 or blank",
      "location": "Remote / City",
      "salary": "₹X-Y LPA or blank if unknown",
      "match_score": 85,
      "tier": 1,
      "tags": ["LLM", "Python", "RAG"],
      "why_match": "Brief reason why this matches the profile",
      "apply_url": "https://platform.com",
      "applied": false,
      "status": "new",
      "target_role": "ai-engineer"
    }}
  ]
}}

The "target_role" field should be one of: "senior-data-analyst", "data-manager", "ai-engineer", "prompt-engineer", "clinical-healthcare"

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


def generate_with_nvidia(prompt, model_config):
    """Generate job listings using NVIDIA NIM API (OpenAI-compatible) with streaming."""
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        print(f"  ⚠️  NVIDIA_API_KEY not set, skipping {model_config['name']}")
        return None

    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=api_key,
            base_url="https://integrate.api.nvidia.com/v1"
        )

        sys.stdout.write(f"  ⏳ Generating with {model_config['name']} (this may take a minute due to reasoning/streaming)... ")
        sys.stdout.flush()

        completion = client.chat.completions.create(
            model=model_config["id"],
            messages=[
                {"role": "system", "content": "You are a job search assistant. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=16384,
            extra_body={"chat_template_kwargs": {"enable_thinking": True, "clear_thinking": False}},
            stream=True
        )

        full_content = ""
        for chunk in completion:
            if not getattr(chunk, "choices", None):
                continue
            if len(chunk.choices) == 0 or getattr(chunk.choices[0], "delta", None) is None:
                continue
            
            delta = chunk.choices[0].delta
            # We ignore reasoning content for the final JSON parsing, but handle it so we don't crash
            # reasoning = getattr(delta, "reasoning_content", None)
            
            content = getattr(delta, "content", None)
            if content is not None:
                full_content += content

        print("Done!")
        
        text = full_content.strip()
        result = _parse_json_response(text)
        
        if result and "jobs" in result and len(result["jobs"]) > 0:
            # Tag each job with model source
            for job in result["jobs"]:
                job["model_source"] = model_config["source_tag"]
                job["model_name"] = model_config["name"]
            print(f"  ✅ Found {len(result['jobs'])} jobs with {model_config['name']}")
            return result
        else:
            print(f"  ⚠️  {model_config['name']} response missing jobs. Raw output snippet:\n{text[:200]}...")
            return None

    except ImportError:
        print("  ⚠️  openai package not installed")
        return None
    except Exception as e:
        print(f"  ⚠️  {model_config['name']} error: {e}")
        return None


def generate_with_gemini(prompt):
    """Generate job listings using Gemini (fallback)."""
    api_key = os.environ.get("GEMINI_API_KEY_PAID")
    if not api_key:
        print("  ⚠️  GEMINI_API_KEY_PAID not set, skipping Gemini")
        return None

    try:
        from google import genai
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-pro-latest",
            contents=prompt
        )
        text = response.text.strip()
        result = _parse_json_response(text)

        if result and "jobs" in result and len(result["jobs"]) > 0:
            for job in result["jobs"]:
                job["model_source"] = "gemini"
                job["model_name"] = "Gemini"
            print(f"  ✅ Found {len(result['jobs'])} jobs with Gemini")
            return result
        else:
            print("  ⚠️  Gemini response missing jobs")
            return None

    except ImportError:
        print("  ⚠️  google-genai package not installed")
        return None
    except Exception as e:
        print(f"  ⚠️  Gemini error: {e}")
        return None


def generate_with_claude(prompt):
    """Generate job listings using Claude (fallback)."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("  ⚠️  ANTHROPIC_API_KEY not set, skipping Claude")
        return None

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        response = client.messages.create(
            model="claude-haiku-4-5-20250315",
            max_tokens=8192,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text.strip()
        result = _parse_json_response(text)

        if result and "jobs" in result and len(result["jobs"]) > 0:
            for job in result["jobs"]:
                job["model_source"] = "claude"
                job["model_name"] = "Claude"
            print(f"  ✅ Found {len(result['jobs'])} jobs with Claude")
            return result
        else:
            print("  ⚠️  Claude response missing jobs")
            return None

    except ImportError:
        print("  ⚠️  anthropic package not installed")
        return None
    except Exception as e:
        print(f"  ⚠️  Claude error: {e}")
        return None


def deduplicate_jobs(all_jobs):
    """Remove duplicate jobs across models based on company+title similarity."""
    seen = {}
    unique_jobs = []
    
    for job in all_jobs:
        key = f"{job.get('company', '').lower().strip()}-{job.get('title', '').lower().strip()}"
        # Simple dedup: keep the first occurrence (higher-priority model)
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

            # Preserve applied status, cover letters, and verification from existing data
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


def verify_jobs(jobs):
    """Verify job listings are still active by checking their URLs."""
    print("  🔎 Verifying job URLs...")
    
    try:
        import httpx
    except ImportError:
        print("  ⚠️  httpx not installed, skipping verification")
        return jobs
    
    verified = 0
    failed = 0
    
    with httpx.Client(timeout=10, follow_redirects=True) as client:
        for job in jobs:
            url = job.get("apply_url", "")
            if not url or url == "#":
                job["verified"] = False
                job["last_verified"] = datetime.now().strftime("%Y-%m-%d")
                failed += 1
                continue
            
            try:
                resp = client.head(url)
                is_active = resp.status_code < 400
                job["verified"] = is_active
                job["last_verified"] = datetime.now().strftime("%Y-%m-%d")
                if is_active:
                    verified += 1
                else:
                    failed += 1
                    print(f"    ⚠️  {job['company']} — HTTP {resp.status_code}")
            except Exception as e:
                job["verified"] = False
                job["last_verified"] = datetime.now().strftime("%Y-%m-%d")
                failed += 1
                print(f"    ⚠️  {job['company']} — {str(e)[:60]}")
    
    print(f"  ✅ Verified: {verified} active, {failed} failed/unreachable")
    return jobs


def main():
    """Main entry point."""
    print("🔍 AI Job Finder — Multi-Model Edition")
    print(f"   Output: {OUTPUT_DIR}")
    print(f"   Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    prompt = build_prompt()
    all_jobs = []
    model_results = {}

    # --- Phase 1: Run all NVIDIA NIM models ---
    print("📡 Phase 1: NVIDIA NIM Models")
    for model_config in NVIDIA_MODELS:
        print(f"  🤖 Trying {model_config['name']} ({model_config['id']})...")
        result = generate_with_nvidia(prompt, model_config)
        if result and result.get("jobs"):
            all_jobs.extend(result["jobs"])
            model_results[model_config["source_tag"]] = len(result["jobs"])
    
    # --- Phase 2: Run Gemini/Claude ---
    print("\n📡 Phase 2: Other Models")
    
    print("  🤖 Trying Gemini (gemini-pro-latest)...")
    result = generate_with_gemini(prompt)
    if result and result.get("jobs"):
        all_jobs.extend(result["jobs"])
        model_results["gemini"] = len(result["jobs"])
    
    print("  🤖 Trying Claude (claude-haiku-4-5)...")
    result = generate_with_claude(prompt)
    if result and result.get("jobs"):
        all_jobs.extend(result["jobs"])
        model_results["claude"] = len(result["jobs"])

    if not all_jobs:
        print("\n  ❌ Failed to generate jobs with any model")
        sys.exit(1)

    # --- Phase 3: Deduplicate & merge ---
    print(f"\n🔧 Phase 3: Processing")
    print(f"  📊 Raw jobs from all models: {len(all_jobs)}")
    all_jobs = deduplicate_jobs(all_jobs)
    print(f"  📊 After deduplication: {len(all_jobs)}")

    # Sort by match score
    all_jobs.sort(key=lambda j: j.get("match_score", 0), reverse=True)

    # Build final result
    today = datetime.now().strftime("%Y-%m-%d")
    month = datetime.now().strftime("%B %Y")
    result = {
        "month": month,
        "generated_date": today,
        "profile_summary": "Data Analyst & AI Developer | LLM Fine-tuning | Python | Multi-model AI",
        "models_used": model_results,
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

    print(f"\n  💾 Saved: {output_path.name}")
    print(f"  📊 {len(result.get('jobs', []))} jobs found for {result.get('month', 'this month')}")
    print(f"  🤖 Models used: {', '.join(f'{k} ({v} jobs)' for k, v in model_results.items())}")


if __name__ == "__main__":
    main()
