"""
Lightweight guards against accidental drift/emptying of the canonical portfolio
data. These intentionally assert structure, not exact copy, so content edits
don't break CI while accidental deletion or malformed variants do.

Note: api/data/projects.py and api/resume_data.py overlap. Treat PROJECTS /
SKILLS / EXPERIENCES as the canonical source and keep resume variants in sync;
full consolidation is tracked as a follow-up refactor.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "api"))


def test_canonical_project_data_present():
    from api.data.projects import PROJECTS, SKILLS, EXPERIENCES, RESUME_PROJECTS

    assert PROJECTS, "PROJECTS is empty"
    assert SKILLS, "SKILLS is empty"
    assert EXPERIENCES, "EXPERIENCES is empty"
    assert RESUME_PROJECTS, "RESUME_PROJECTS is empty"


def test_resume_variants_are_complete():
    from api.resume_data import ROLE_DEFINITIONS, ROLE_RESUMES

    assert ROLE_DEFINITIONS, "ROLE_DEFINITIONS is empty"
    for slug, data in ROLE_RESUMES.items():
        assert slug in ROLE_DEFINITIONS, f"role '{slug}' has no definition"
        for key in ("summary", "experiences", "projects", "skills"):
            assert data.get(key), f"resume variant '{slug}' is missing '{key}'"


def test_shared_contact_data_present():
    from api.resume_data import CONTACT, EDUCATION

    assert CONTACT.get("name") and CONTACT.get("email")
    assert EDUCATION.get("institution")


def test_dashboard_data_schema_is_normalized():
    """Mixed-schema pipeline JSON must be normalized before it reaches templates."""
    from api.index import load_brand_timeseries, load_pharma_log

    ts = load_brand_timeseries()
    for run in ts.get("runs", []) or []:
        for brand in run.get("brands", []) or []:
            assert "llmo_score" in brand.get("report", {}), "brand report missing llmo_score"

    log = load_pharma_log()
    for run in log.get("pipeline_runs", []) or []:
        assert "avg_ind_score" in run, "pharma run missing avg_ind_score"
