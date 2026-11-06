"""Headline numbers for the home page, in one place.

There are two kinds of numbers on the site, and they must never be presented as
the same thing:

``snapshot``
    All-time aggregates that belong to the **other** project repos (JobAgents
    sourced N roles, BugAgents promoted M reports, AgentSwarm sealed K ledgers).
    This app cannot observe those pipelines, so they are constants here — taken
    from each project's own written records — and they are rendered as
    "all-time totals", never as live telemetry with a pulsing dot.

``live()``
    Things this repo can actually read at request time: swarm telemetry, the
    newest daily job-pipeline run, dev-log and blog counts, and the number of
    deployed systems derived from ``api/data/projects.py``.

If you quote a new number on the home page, add it here rather than typing it
into the template: that is what stopped the hero from lying with a green dot.
"""

import glob
import json
import logging
import os
from datetime import datetime, timezone

try:  # same paired-import pattern as the rest of the app
    from api.data.projects import PROJECTS
except ImportError:  # pragma: no cover - local script execution
    from data.projects import PROJECTS

try:  # the swarm roster, so "N agents" is never a hardcoded claim
    from api.ai_eco_mcp import AI_ECO_SWARM
except ImportError:  # pragma: no cover
    try:
        from ai_eco_mcp import AI_ECO_SWARM
    except ImportError:
        AI_ECO_SWARM = None

logger = logging.getLogger(__name__)

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

# ---------------------------------------------------------------------------
# All-time totals, as reported by each project's own pipeline records.
# Reconcile these with the source repos when they change; the UI labels them
# with SNAPSHOT_NOTE so they can never look like live counters.
# ---------------------------------------------------------------------------
SNAPSHOT = {
    # JobAgents
    'jobs_sourced': 9697,
    'distinct_roles': 7665,
    'sources': 10,
    'companies': 349,
    'duplicates_merged': 2032,
    'scores_computed': 29091,
    'llm_shortlist': 234,
    'score_threshold': 65,
    'fabrications_caught': '8/8',
    # BugAgents
    'hunt_runs': 22,
    'agent_turns': 84,
    'bug_tool_calls': 15317,
    'findings': 8,
    'findings_high_critical': 5,
    'findings_medium': 3,
    'reports_promoted': 2,
    'reports_refused': 34,
    'vulnerability_classes': 14,
    # AgentSwarm
    'swarm_runs': 34,
    'ledger_chains': '35/35',
    'oracle_violations': 0,
    'oracle_tool_calls': 1254,
    'audit_verdict': 'B+',
    'audit_claims_verified': '22/25',
}

SNAPSHOT_NOTE = (
    "All-time totals reported by each project's own pipeline records — not live "
    "telemetry. Live numbers are on the Fleet Command Center and /ecosystem."
)


def _load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("site_stats: cannot read %s: %s", path, exc)
        return None


def _count(pattern):
    return len(glob.glob(os.path.join(BASE_DIR, pattern)))


def _newest(pattern):
    files = sorted(glob.glob(os.path.join(BASE_DIR, pattern)))
    return files[-1] if files else None


def _deployed_systems():
    """Featured projects that point at a real running deployment.

    A blog-post URL is documentation, not a deployment, so those are excluded —
    which is why this counts higher and more honestly than the old hardcoded
    hero number.
    """
    count = 0
    for project in PROJECTS:
        url = (project.get('url') or '').strip()
        if not project.get('featured') or not url.startswith('http'):
            continue
        if '/blog/' in url:
            continue
        count += 1
    return count


def live():
    """Signals this repo can actually verify right now."""
    data = {
        'data_date': None,
        'commits_tracked': None,
        'repos_scanned': None,
        'swarm_agents': None,
        'mcp_endpoints': None,
        'telemetry_updated': None,
        'latest_job_run': None,
        'dev_logs': _count('AI_Eco_Blogs/*.md'),
        'blog_posts': _count('blog_inputs/*.md') + _count('blog_data/*.json'),
        'swarm_daily_views': _count('ecosystem_swarm/daily_views/*.md'),
        'weekly_meetings': _count('ecosystem_swarm/weekly_meetings/*.md'),
        'deployed_systems': _deployed_systems(),
        'swarm_agents': len(AI_ECO_SWARM) if AI_ECO_SWARM else None,
    }

    telemetry = _load_json(os.path.join(BASE_DIR, 'job_data', 'ecosystem_telemetry.json'))
    if isinstance(telemetry, dict):
        data['commits_tracked'] = telemetry.get('commit_history')
        data['repos_scanned'] = telemetry.get('repo_counts')
        data['mcp_endpoints'] = telemetry.get('mcp_endpoints_active')
        data['telemetry_updated'] = telemetry.get('last_updated')

    newest_run = _newest('job_data/daily/*.json')
    if newest_run:
        run = _load_json(newest_run)
        if isinstance(run, dict):
            data['latest_job_run'] = {
                'date': run.get('date') or os.path.basename(newest_run).replace('.json', ''),
                'jobs': len(run.get('jobs') or []),
                'version': run.get('pipeline_version'),
            }

    # The freshest date this repo's own content can prove.
    newest_log = _newest('AI_Eco_Blogs/*.md')
    if newest_log:
        data['last_dev_log'] = os.path.basename(newest_log).replace('.md', '').replace('github-activity-', '')
        data['data_date'] = data['last_dev_log']

    return data


def all_stats():
    """Everything the templates need, with the snapshot clearly separated."""
    return {
        'snapshot': SNAPSHOT,
        'snapshot_note': SNAPSHOT_NOTE,
        'live': live(),
        'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'),
    }
