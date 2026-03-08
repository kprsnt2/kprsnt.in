#!/usr/bin/env python3
"""
AI Job Finder
Uses Gemini API to search and curate job openings matching the profile.
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
        "Data Analysis", "Dashboards", "ETL", "AppScript"
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
        "AI Engineer", "LLM Engineer", "Generative AI Developer",
        "Data Analyst (Senior)", "ML Engineer", "Prompt Engineer",
        "AI/ML Solutions Engineer", "Forward Deployed Engineer",
        "Pharma + AI roles"
    ],
    "salary_range": "₹10-50 LPA or $30K-80K USD",
    "preferred": "Remote, async-first teams, startups or mid-size companies"
}


def build_prompt():
    """Build the AI prompt for job search."""
    month = datetime.now().strftime("%B %Y")
    return f"""You are an AI job search assistant. Find and curate current remote job openings that match this profile.

**Candidate Profile:**
- Title: {PROFILE['title']}
- Location: {PROFILE['location']} (prefers remote)
- Key Skills: {', '.join(PROFILE['skills'])}
- Experience: {'; '.join(PROFILE['experience'])}
- Education: {PROFILE['education']}
- Target Roles: {', '.join(PROFILE['target_roles'])}

**Instructions:**
1. Search for real, currently hiring positions from March 2026
2. Focus on remote-friendly roles in India or worldwide
3. Match roles based on skills overlap — prioritize LLM/AI engineer roles
4. Include a mix of strong matches (Tier 1) and good matches (Tier 2)
5. For each job, calculate a match_score (0-100) based on skill overlap
6. Include at least 10 jobs, up to 20
7. The candidate's Pharma + AI combo is UNIQUE — always include pharma+AI roles if available

**Output Format:**
Return ONLY a valid JSON object with this structure:
{{
  "month": "{month}",
  "generated_date": "{datetime.now().strftime('%Y-%m-%d')}",
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
      "status": "new"
    }}
  ]
}}

Return valid JSON only, no markdown code fences, no extra text."""


def generate_with_gemini(prompt):
    """Generate job listings using Gemini."""
    api_key = os.environ.get("GEMINI_API_KEY_PAID")
    if not api_key:
        print("  ⚠️  GEMINI_API_KEY_PAID not set, skipping Gemini")
        return None

    try:
        from google import genai
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3-pro-preview",
            contents=prompt
        )
        text = response.text.strip()

        # Handle code fences
        if text.startswith("```"):
            text = re.sub(r'^```\w*\n?', '', text)
            text = re.sub(r'\n?```$', '', text)
            text = text.strip()

        result = json.loads(text)
        if "jobs" in result and len(result["jobs"]) > 0:
            print(f"  ✅ Found {len(result['jobs'])} jobs with Gemini")
            return result
        else:
            print("  ⚠️  Gemini response missing jobs")
            return None

    except ImportError:
        print("  ⚠️  google-genai package not installed")
        return None
    except json.JSONDecodeError as e:
        print(f"  ⚠️  Gemini returned invalid JSON: {e}")
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

        if text.startswith("```"):
            text = re.sub(r'^```\w*\n?', '', text)
            text = re.sub(r'\n?```$', '', text)
            text = text.strip()

        result = json.loads(text)
        if "jobs" in result and len(result["jobs"]) > 0:
            print(f"  ✅ Found {len(result['jobs'])} jobs with Claude")
            return result
        else:
            print("  ⚠️  Claude response missing jobs")
            return None

    except ImportError:
        print("  ⚠️  anthropic package not installed")
        return None
    except json.JSONDecodeError as e:
        print(f"  ⚠️  Claude returned invalid JSON: {e}")
        return None
    except Exception as e:
        print(f"  ⚠️  Claude error: {e}")
        return None


def merge_with_existing(new_data):
    """Merge new jobs with existing data, preserving 'applied' status."""
    month_slug = datetime.now().strftime("%B-%Y").lower()
    output_path = OUTPUT_DIR / f"{month_slug}.json"

    if output_path.exists():
        try:
            existing = json.loads(output_path.read_text(encoding="utf-8"))
            existing_jobs = {j["id"]: j for j in existing.get("jobs", [])}

            # Preserve applied status from existing data
            for job in new_data.get("jobs", []):
                if job["id"] in existing_jobs:
                    old = existing_jobs[job["id"]]
                    job["applied"] = old.get("applied", False)
                    job["status"] = old.get("status", "new")

            print(f"  🔄 Merged with existing data ({len(existing_jobs)} existing jobs)")
        except Exception as e:
            print(f"  ⚠️  Could not merge: {e}")

    return new_data


def main():
    """Main entry point."""
    print("🔍 AI Job Finder")
    print(f"   Output: {OUTPUT_DIR}")

    prompt = build_prompt()

    # Try Gemini first, then Claude fallback
    result = generate_with_gemini(prompt)
    if result is None:
        result = generate_with_claude(prompt)

    if result is None:
        print("  ❌ Failed to generate with both Gemini and Claude")
        sys.exit(1)

    # Merge with existing data
    result = merge_with_existing(result)

    # Save
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    month_slug = datetime.now().strftime("%B-%Y").lower()
    output_path = OUTPUT_DIR / f"{month_slug}.json"
    output_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"  💾 Saved: {output_path.name}")
    print(f"  📊 {len(result.get('jobs', []))} jobs found for {result.get('month', 'this month')}")


if __name__ == "__main__":
    main()
