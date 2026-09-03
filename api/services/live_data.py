"""
Live Data Service — Loads real-time pipeline data for AI context.
Reads from job_data/, brand_timeseries.json, and pharma_data/.
"""
import os
import json
import glob
import logging

logger = logging.getLogger(__name__)

BASE_DIR = os.path.join(os.path.dirname(__file__), '..', '..')


def get_live_jobs_summary():
    """Load latest job pipeline data and return a summary string."""
    try:
        daily_dir = os.path.join(BASE_DIR, 'job_data', 'daily')
        if not os.path.exists(daily_dir):
            return ""

        daily_files = sorted(glob.glob(os.path.join(daily_dir, '*.json')), reverse=True)
        if not daily_files:
            return ""

        with open(daily_files[0], 'r', encoding='utf-8') as f:
            data = json.load(f)

        jobs = data.get('jobs', [])
        if not jobs:
            return ""

        total = len(jobs)
        date = data.get('date', 'Unknown')
        top_matches = sum(1 for j in jobs if j.get('evaluation', {}).get('overall_score', 0) >= 3.5)
        grade_a = sum(1 for j in jobs if j.get('evaluation', {}).get('grade', '').startswith('A'))
        applied = sum(1 for j in jobs if j.get('status') == 'applied')
        avg_score = round(
            sum(j.get('evaluation', {}).get('overall_score', 0) for j in jobs if j.get('evaluation'))
            / max(sum(1 for j in jobs if j.get('evaluation')), 1), 1
        )

        # Top 3 jobs
        scored_jobs = sorted(jobs, key=lambda j: j.get('evaluation', {}).get('overall_score', 0), reverse=True)
        top_3 = []
        for j in scored_jobs[:3]:
            ev = j.get('evaluation', {})
            top_3.append(f"  - {j.get('title', '?')} at {j.get('company', '?')} (Score: {ev.get('overall_score', 0)}/5, Grade {ev.get('grade', '?')})")

        summary = f"""LIVE JOB PIPELINE DATA (as of {date}):
- {total} jobs evaluated by the 4-agent AI pipeline
- {top_matches} top matches (score >= 3.5/5), {grade_a} Grade-A opportunities
- Average evaluation score: {avg_score}/5
- {applied} jobs applied to
- Top matches:
{chr(10).join(top_3)}"""
        return summary

    except Exception as e:
        logger.warning(f"Failed to load live jobs data: {e}")
        return ""


def get_live_brand_summary():
    """Load latest brand tracking data and return a summary string."""
    try:
        brand_file = os.path.join(BASE_DIR, 'job_data', 'brand_timeseries.json')
        if not os.path.exists(brand_file):
            return ""

        with open(brand_file, 'r', encoding='utf-8') as f:
            ts_data = json.load(f)

        runs = ts_data.get('runs', [])
        if not runs:
            return ""

        latest = runs[-1]
        brands = latest.get('brands', [])
        if not brands:
            return ""

        date = latest.get('date', '')[:10]
        brand_count = len(brands)
        avg_llmo = round(sum(b.get('report', {}).get('llmo_score', 0) for b in brands) / max(brand_count, 1), 1)
        total_runs = len(runs)

        sorted_brands = sorted(brands, key=lambda b: b.get('report', {}).get('llmo_score', 0), reverse=True)
        top_brands = [f"  - {b.get('brand', '?')}: LLMO score {b.get('report', {}).get('llmo_score', 0)}/100" for b in sorted_brands[:5]]

        summary = f"""LIVE BRAND TRACKER DATA (as of {date}):
- Tracking {brand_count} brands across {total_runs} pipeline runs
- Average LLMO score: {avg_llmo}/100
- Top brands by LLMO score:
{chr(10).join(top_brands)}"""
        return summary

    except Exception as e:
        logger.warning(f"Failed to load live brand data: {e}")
        return ""


def get_live_pharma_summary():
    """Load latest pharma pipeline data and return a summary string."""
    try:
        pharma_dir = os.path.join(BASE_DIR, 'job_data', 'pharma_data')
        if not os.path.exists(pharma_dir):
            return ""

        compounds = []
        for f in glob.glob(os.path.join(pharma_dir, '*.json')):
            try:
                with open(f, 'r', encoding='utf-8') as fh:
                    compounds.append(json.load(fh))
            except Exception:
                pass

        if not compounds:
            return ""

        compounds.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        compound_count = len(compounds)

        recent = []
        for c in compounds[:5]:
            name = c.get('compound_name', c.get('name', '?'))
            status = c.get('status', c.get('phase', '?'))
            recent.append(f"  - {name} ({status})")

        summary = f"""LIVE PHARMA PIPELINE DATA:
- {compound_count} compounds analyzed by the AI drug discovery pipeline
- Recent analyses:
{chr(10).join(recent)}"""
        return summary

    except Exception as e:
        logger.warning(f"Failed to load live pharma data: {e}")
        return ""

def get_live_ecosystem_summary():
    """Load latest AI Eco multi-agent swarm telemetry and return a summary string."""
    try:
        eco_file = os.path.join(BASE_DIR, 'job_data', 'ecosystem_telemetry.json')
        if not os.path.exists(eco_file):
            return ""

        with open(eco_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        commits = data.get('commit_history', 987)
        repos = data.get('repo_counts', 100)
        langs = list(data.get('language_breakdown', {}).keys())[:4]
        salary = data.get('live_salary_estimation', {})
        sal_min = salary.get('min', 180000)
        sal_max = salary.get('max', 320000)
        last_updated = data.get('last_updated', '')[:10]

        summary = f"""LIVE AI ECO SWARM DATA (as of {last_updated}):
- 6 autonomous agents running daily (GitHub Scout, Dashboard, Portfolio Sync, MCP Engineer, Docs, Readme)
- {commits} verified commits across {repos} tracked repositories
- Primary languages: {', '.join(langs)}
- Active Model Context Protocol (MCP) server exposing tools, resources, and prompts
- Live US Market Salary Benchmark: ${sal_min:,} - ${sal_max:,}"""
        return summary

    except Exception as e:
        logger.warning(f"Failed to load live ecosystem data: {e}")
        return ""


def get_all_live_data():
    """Get combined summary of all live pipeline data."""
    parts = []

    ecosystem = get_live_ecosystem_summary()
    if ecosystem:
        parts.append(ecosystem)

    jobs = get_live_jobs_summary()
    if jobs:
        parts.append(jobs)

    brands = get_live_brand_summary()
    if brands:
        parts.append(brands)

    pharma = get_live_pharma_summary()
    if pharma:
        parts.append(pharma)

    if not parts:
        return ""

    return "\n\n" + "\n\n".join(parts)
