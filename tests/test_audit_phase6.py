"""
Phase 6 bug-hunt regression tests: api/services/* and api/data/*.

Locks in the invariants verified during the audit's final bug-hunt pass.
All tests run offline.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "api"))
sys.path.insert(0, os.path.join(ROOT, "api", "data"))


# --------------------------------------------------------------------------
# api/data/*
# --------------------------------------------------------------------------

def test_projects_have_required_keys():
    import api.data.projects as projects

    for proj in projects.PROJECTS:
        for key in ("title", "description", "tags"):
            assert key in proj, f"{proj.get('title')!r} missing {key}"
        assert isinstance(proj.get("tags", []), list)


def test_portfolio_kb_titles_normalize_consistently():
    from api.data.portfolio_kb import _normalize_title

    # exact-prefix stripping, not character-set lstrip
    assert _normalize_title("📰 Retail Shelf Intelligence") == "retail shelf intelligence"
    assert _normalize_title("📊📰 Nested Emoji") == "nested emoji"
    assert _normalize_title("Plain Title") == "plain title"
    # lstrip(charset) would have mangled these:
    assert _normalize_title("❤️ Loved") == "loved"


def test_portfolio_kb_title_aligns_with_site():
    from api.data.portfolio_kb import PROFILE

    assert PROFILE["title"] == "AI Systems Engineer"


def test_case_study_domains_are_known_labels():
    from api.data.case_studies import PROJECT_CASE_STUDIES

    known = {"Production Systems", "Autonomous Multi-Agent & AI Research", "Developer Tooling & Infrastructure"}
    for study in PROJECT_CASE_STUDIES.values():
        assert study["domain"] in known, study.get("name")


def test_case_study_lookup():
    from api.data.case_studies import get_case_study

    assert get_case_study("mseat")["slug"] == "mseat"
    assert get_case_study("MBBS")["slug"] == "mseat"
    assert get_case_study("zzz-nonexistent-zzz") is None
    # empty keyword: caller (ai_eco_mcp) requires non-empty; the raw lookup
    # itself must not crash
    assert get_case_study("") is None or isinstance(get_case_study(""), dict)


def test_hiring_evidence_structure():
    from api.data.case_studies import get_structured_hiring_evidence

    evidence = get_structured_hiring_evidence("all")
    assert evidence["categorized_domains"]
    assert evidence["top_quantified_proof_points"]


# --------------------------------------------------------------------------
# api/services/*
# --------------------------------------------------------------------------

def test_live_data_survives_missing_files(tmp_path, monkeypatch):
    import api.services.live_data as live

    monkeypatch.setattr(live, "BASE_DIR", str(tmp_path))
    assert live.get_live_jobs_summary() == ""
    assert live.get_live_ecosystem_summary() == ""
    assert live.get_all_live_data() == ""


def test_live_data_survives_malformed_telemetry(tmp_path, monkeypatch):
    import api.services.live_data as live

    (tmp_path / "job_data").mkdir()
    (tmp_path / "job_data" / "ecosystem_telemetry.json").write_text(
        '{"last_updated": null, "commit_history": 1136}', encoding="utf-8"
    )
    monkeypatch.setattr(live, "BASE_DIR", str(tmp_path))
    # non-string last_updated must not crash the summary
    summary = live.get_live_ecosystem_summary()
    assert "1136" in summary


def test_live_data_parses_daily_jobs(tmp_path, monkeypatch):
    import api.services.live_data as live

    daily = tmp_path / "job_data" / "daily"
    daily.mkdir(parents=True)
    (daily / "2026-09-22.json").write_text(
        '{"date": "2026-09-22", "jobs": ['
        '{"title": "AI Engineer", "company": "Acme", "evaluation": {"overall_score": 4.5, "grade": "A"}},'
        '{"title": "Data Analyst", "company": "Beta", "status": "applied"}'
        ']}',
        encoding="utf-8",
    )
    monkeypatch.setattr(live, "BASE_DIR", str(tmp_path))
    summary = live.get_live_jobs_summary()
    assert "2 jobs evaluated" in summary
    assert "1 top matches" in summary
    assert "1 jobs applied to" in summary


def test_insights_handles_empty_and_minimal():
    from api.services.insights import generate_jobs_insight

    assert "No job data" in generate_jobs_insight([], [], {}, {}, {})

    jobs = [{"title": "AI Engineer", "company": "Acme",
             "evaluation": {"overall_score": 4.5, "grade": "A"}, "status": "applied"}]
    text = generate_jobs_insight(jobs, [{"total_jobs": 1}, {"total_jobs": 2}],
                                 {"A": 1}, {"cv_match": 4.0, "culture_signals": 3.0}, [])
    assert "AI Engineer" in text
    assert "<strong>" in text  # markdown-bold -> HTML


def test_rag_helpers_defensive():
    from api.services.rag import retrieve_chunks

    assert retrieve_chunks(None, None) == []
    assert retrieve_chunks(None, {"chunks": []}) == []
    assert retrieve_chunks([0.1, 0.2], None) == []
