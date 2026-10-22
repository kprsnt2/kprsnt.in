"""
Profile-consistency guard — stops the site drifting from the single source of truth.

PURPOSE
    Every claim on kprsnt.in (projects, resume variants, skills) must be traceable
    to ``D:\\JobAgents\\config\\profile.md`` — the single source of truth — with
    live-site deviations allowed only where ``scratch/GROUND_TRUTH.md`` re-verified
    them. This test fails CI when a superseded number, a fabricated employer, an
    inflated held title, or a naming regression comes back.

WHAT IS CHECKED (all offline, no API keys, no network)
    1. SUPERSEDED_NUMBERS  — stale metrics never reappear in the data modules or
       templates/ (a leading "~"/"+"/"-" is tolerated, so "~7,533" still trips).
    2. FABRICATED_CLAIMS   — fake employers, unearned publication/disclosure
       status, production-user/revenue claims, and AI titles asserted as held
       employment ("AI Systems Engineer at Black Piano") never reappear.
    3. EMPLOYERS / DATES   — exactly three employers, with the profile.md dates;
       the independent projects are never framed as an employer.
    4. HELD TITLES         — every employment role/title is one profile.md says he
       held; AI/agentic titles may only appear as a clearly-marked target.
    5. VERIFIED_METRICS    — every pinned number exists in profile.md, in the
       module that renders it, AND (when readable) in profile.md's
       "Verified Metrics" table. A pin can disappear from the code, never from
       the profile.
    6. rAsh Score naming   — canonical name/URL is rAsh Score / rashscore.live;
       legacy "BrandScore" / "bs.kprsnt.in" may only be labelled legacy/stale.
    7. OFFLINE             — the guard imports no network/LLM client, and the
       guarded modules stay pure data (no os/sys/subprocess imports).

WHAT IS DELIBERATELY ALLOWED (do not "fix" these by widening the lists)
    "CVSS Scoring" / "CWE Classification" (profile.md skills, not CVSS numbers),
    "1,441" / "1,553" / "330" (Awakening's live-verified metrics), "20B" / "120B",
    "M.Pharm", the real repo URL github.com/kprsnt2/BrandScore (provenance, not a
    naming claim), and disclaimers such as "no claimed users, downloads or revenue"
    (a ban is tolerated when the same sentence negates it).

HOW TO UPDATE WHEN profile.md CHANGES
    • First update profile.md (and re-verify against the live sites, per rule 11),
      then ``scratch/GROUND_TRUTH.md``.
    • Retired number  -> move it into ``SUPERSEDED_NUMBERS`` here.
      New verified number -> add it to ``VERIFIED_METRICS`` here.
      Employer/title change -> edit ``EMPLOYERS`` / ``ALLOWED_HELD_TITLES``.
    • Every number must appear *literally* in profile.md (e.g. "34 runs and 9
      domains"), which is why the identifiers carry their unit words.

CI NOTE
    profile.md lives outside the repo. Only the metrics-vs-profile.md check
    skips when that path is unreadable; every other assertion still runs and
    still fails on drift.
"""
import ast
import os
import re
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "api"))

try:
    from data.projects import EXPERIENCES, PROJECTS, RESUME_PROJECTS
    from resume_data import ROLE_DEFINITIONS, ROLE_RESUMES
except ImportError:
    from api.data.projects import EXPERIENCES, PROJECTS, RESUME_PROJECTS
    from api.resume_data import ROLE_DEFINITIONS, ROLE_RESUMES

try:
    from data import portfolio_kb
except ImportError:
    from api.data import portfolio_kb

PROJECTS_MODULE = os.path.join(ROOT, "api", "data", "projects.py")
RESUME_MODULE = os.path.join(ROOT, "api", "resume_data.py")
DATA_MODULES = [PROJECTS_MODULE, RESUME_MODULE]
PROFILE_KBD = os.path.join(ROOT, "api", "data", "portfolio_kb.py")
TEMPLATES_DIR = os.path.join(ROOT, "templates")
PROFILE_MD = os.environ.get("KPRSNT_PROFILE_MD", r"D:\JobAgents\config\profile.md")
GROUND_TRUTH_MD = os.path.join(ROOT, "scratch", "GROUND_TRUTH.md")

MIN_VERIFIED_METRICS_ROWS = 20  # profile.md's table is far bigger; guards the parser


# ---------------------------------------------------------------------------
# Helpers - read source text, never imported values, so comments are covered too
# ---------------------------------------------------------------------------

def _read_module(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def _module_args():
    """pytest params: (path, module name) so node IDs stay short and readable."""
    return [(path, os.path.basename(path)) for path in DATA_MODULES]


def _source_parts(path):
    """Split a module into (raw text, comment lines, string-literal chunks).

    Splitting lets us ban a phrase as *data* while allowing the disclaimer text
    ("AI Systems Engineer is a target, never a held title") that documents the ban.
    """
    text = _read_module(path)
    comments = [line.split("#", 1)[1] for line in text.splitlines() if line.lstrip().startswith("#")]
    chunks = []
    for node in ast.walk(ast.parse(text)):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            chunks.append(node.value)
    return text, comments, chunks


def _renderable_strings(path):
    """Every string the module actually renders — docstrings and comments excluded.

    A file header is documentation ("profile.md forbids 'peer-reviewed' claims");
    only real data can put a claim on the page.
    """
    tree = ast.parse(_read_module(path))
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = getattr(node, "body", [])
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                if isinstance(body[0].value.value, str):
                    docstrings.add(id(body[0].value))
    return [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstrings
    ]


# Phrases that turn a quoted ban into documentation of the rule.
COMMENT_ALLOWED_WORDS = {
    "superseded": (
        "removed", "remove", "removing", "retired", "retire", "stale",
        "superseded", "unsourced", "forbidden", "replaced", "dropped", "drop",
        "deleted", "delete", "banned", "ban", "no longer", "must not", "never",
        "pre-", "deny-list", "hard bans", "do not", "not in profile", "demoted",
    ),
    # "fabricated" and "held_title" reuse the shared lists defined below.
}


def _comment_violations(comment, checks):
    """Complaints about a comment quoting a ban without explaining it.

    ``comment`` is a whole contiguous comment block (explanations may wrap), and
    every vocabulary word is matched case-insensitively.
    """
    problems = []
    if "superseded" in checks:
        allowed = COMMENT_ALLOWED_WORDS["superseded"]
        for needle in SUPERSEDED_NUMBERS:
            if needle.lower() in comment.lower() and not _match_any(comment, allowed):
                problems.append(f"retired figure {needle!r} not explained: {comment.strip()[:140]!r}")
    if "fabricated" in checks:
        problems.extend(_fabrication_hits([comment]))
    if "held_title" in checks:
        for phrase in re.findall(r"[^.;]*\bAI Systems Engineer\b[^.;]*", comment):
            if not _match_any(phrase, TARGET_LABEL_WORDS + ("held", "never", "not a", "forbid")):
                problems.append(f"AI title quoted without a target label: {phrase.strip()[:140]!r}")
    return problems


def _all_strings(value):
    """Recursively collect every string inside a data structure."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from _all_strings(child)
    elif isinstance(value, (list, tuple, set)):
        for child in value:
            yield from _all_strings(child)


# A phrase is tolerated only when the same sentence DISCLAIMS it ("not
# peer-reviewed", "never claim production users"), which is how the data modules
# document the bans they follow.
DISCLAIMER_WORDS = (
    "not ", "no ", "never", "non-", "without", "zero", "false", "avoid", "forbid",
    "must ", "rule", "claim", "stale", "legacy", "target", "not-", "n't",
)
# A field may only quote "AI Systems Engineer" as a target/direction.
TARGET_LABEL_WORDS = ("target", "transition", "→", "->", "direction")


def _context_allows(phrase, chunk):
    """True when every occurrence of ``phrase`` sits in a negating/limiting sentence."""
    lowered = chunk.lower()
    start = 0
    while True:
        index = lowered.find(phrase.lower(), start)
        if index < 0:
            return True
        sentence_start = max(lowered.rfind(". ", 0, index), lowered.rfind("\n", 0, index)) + 1
        sentence = lowered[sentence_start:index]
        if not any(word in sentence for word in DISCLAIMER_WORDS):
            return False
        start = index + len(phrase)


def _fabrication_hits(text_chunks):
    hits = []
    for chunk in text_chunks:
        for phrase in FABRICATED_CLAIMS:
            if phrase.lower() in chunk.lower() and not _context_allows(phrase, chunk):
                at = chunk.lower().find(phrase.lower())
                hits.append(f"{phrase!r} in {chunk[max(0, at - 60):at + 100]!r}")
    return hits


def _templates():
    for dirpath, _dirnames, filenames in os.walk(TEMPLATES_DIR):
        for filename in sorted(filenames):
            if filename.endswith((".html", ".jinja", ".j2")):
                path = os.path.join(dirpath, filename)
                with open(path, encoding="utf-8") as handle:
                    yield os.path.relpath(path, ROOT), handle.read()


def _norm(text):
    """Tolerant number comparison: 18,000+ / 18.000 / 18 000 compare equal."""
    return re.sub(r"[\s,+]", "", text)


def _as_pattern(needle):
    return re.compile(r"\s+".join(re.escape(part) for part in needle.split()))


def _match_any(line, words):
    """Return the words from ``words`` that appear in ``line``."""
    low = line.lower()
    return [word for word in words if word.lower() in low]


def load_profile_text():
    try:
        with open(PROFILE_MD, encoding="utf-8") as handle:
            return handle.read()
    except OSError:
        return None


def parse_verified_metrics_table(profile_text):
    """Rows of profile.md's ``| Metric | Value | Source |`` Verified Metrics table."""
    lines = profile_text.splitlines()
    start = next(
        (
            i
            for i, line in enumerate(lines)
            if line.strip().startswith("#") and "Verified Metrics" in line
        ),
        None,
    )
    assert start is not None, f"'Verified Metrics' heading not found in {PROFILE_MD}"
    rows = []
    started = False
    for line in lines[start + 1:]:
        stripped = line.strip()
        if stripped.startswith("#"):
            break
        if stripped.startswith("|"):
            started = True
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if len(cells) >= 2 and not set(cells[0]) <= set("-: "):
                rows.append((cells[0], cells[1]))
        elif started and not stripped:
            break
    return rows


# ---------------------------------------------------------------------------
# Curated tables — the single place to edit when profile.md changes
# ---------------------------------------------------------------------------

# 1. Every superseded metric / known-false figure. These must never render.
#    Numbers that profile.md DOES verify (1,441 / 1,553 / 330 / CVSS Scoring as a
#    skill name / "CWE Classification" / BrandXY "76.5" / "20B" / "120B") are
#    deliberately absent from this list.
SUPERSEDED_NUMBERS = [
    # JobAgents — pre-2026-10-11 snapshot (superseded by live 9,697 / 7,665 / …)
    "7,533",
    "7,500",
    "5,784",
    "1,864",
    "22,647",
    "22,000",
    "32/32",
    "7 sources",
    # BugAgents / AgentSwarm spend + tool-call claims that were never verified
    "3,156",
    "$0.067",
    "0.067",
    "2,592",
    "80 turns",
    "4 public programs",
    # CVSS severity claims (profile.md: cite severity only, never a CVSS score)
    "CVSS 9.3",
    "CVSS 8.6",
    "9.3 and 8.6",
    "9.3 cvss",
    # MyLocalCLI — the real figures are v4.0.2 / 8 providers / 42 tools / 38 skills
    "6 AI providers",
    "26 tools",
    "22 skills",
    # Black Piano / Pi Software bullet inflation (not in profile.md)
    "4 enterprise clients",
    "15+ dashboards",
    "reduced manual reporting by 60%",
    "cutting manual reporting overhead by 60%",
    "manual reporting time by 60%",
    # Unverified project claims
    "arXiv paper",
    "Solari",
    "Retail Shelf Intelligence",
    "MCP 2024-11-05",
    "Zero-Prompt Emergence",
]

# Numbers that only mean something with their unit attached: the unit-less
# suffix appears incidentally (an inline <style> block's `top: -60%`, sample CSV
# cells, a 60 fps counter), so these are matched with their words.
SUPERSEDED_PHRASE_PATTERNS = [
    re.compile(r"60\s*%\s*(?:reduction|less|fewer|faster|time|in (?:manual|reporting))", re.IGNORECASE),
    re.compile(r"(?:by|of|cut|cutting|reduced?|reduce)\s*[a-z ]{0,24}?\b60\s*%", re.IGNORECASE),
]

# 2. Phrases that assert something profile.md forbids. Each : notes the fix.
FABRICATED_CLAIMS = [
    "Independent AI Research & Development",  # a fake employer block
    "Independent AI Research and Development",
    "employee of",  # independent projects are never employment
    "counts as employment",
    "peer-reviewed",  # Paper 1 is a Zenodo PREPRINT
    "peer reviewed",
    "published in journal",
    "journal-published",
    "bounty awarded",
    "bounty paid",
    "vulnerability disclosed",
    "production users",
    "paying users",
    "annual revenue",
    "revenue from",
    "commercial adoption",
]


# 3. Employment as written in profile.md ("Employment (verbatim)"). Order matters:
#    the job title is the line above each period.
EMPLOYERS = [
    {"company": "Black Piano", "role": "Data Analyst", "period": "Mar 2026 – Present"},
    {"company": "Pi Software Solutions", "role": "Data Analyst", "period": "Mar 2023 – Feb 2026"},
    {
        "company": "Optum",
        "role": "Enrollment Quality & Audit Representative (CMS Auditor)",
        "period": "Apr 2014 – Mar 2023",
    },
]

# 4. Titles profile.md says were actually held (rule 1 + rule 12).
ALLOWED_HELD_TITLES = {
    "data analyst",
    "enrollment quality & audit representative (cms auditor)",
}

# 5. Numbers rendered on the site, pinned to where they come from.
#    module:  which data module renders the claim (a string maps to any occurrence,
#             a list to "first number, later number" i.e. the claim's real order).
#    profile: the literal phrase in profile.md that makes the number citable.
#    site:    "verified_metrics" (default) = profile.md's Verified Metrics TABLE is
#             the authority for this figure. Any other value = profile.md's own
#             rule 11 requires an extra source, and re-verified live-site figures
#             (scratch/GROUND_TRUTH.md) are the only ones allowed that exemption.
VERIFIED_METRICS = {
    # BugAgents
    "bugagents_findings": {"value": "8 findings", "module": PROJECTS_MODULE, "profile": "8 findings"},
    "bugagents_cwe_classes": {"value": "14", "module": PROJECTS_MODULE, "profile": "14 vulnerability classes"},
    "bugagents_tool_calls": {
        "value": "15,317", "module": PROJECTS_MODULE,
        "profile": "15,317 tool calls", "site": "featured_projects_prose",
    },
    "bugagents_promoted": {"value": "2 reports", "module": PROJECTS_MODULE, "profile": "promoted 2 reports"},
    "bugagents_refusals": {"value": "34", "module": PROJECTS_MODULE, "profile": "34 filter refusals"},
    "bugagents_runs": {"value": "22", "module": PROJECTS_MODULE, "profile": "22 hunt runs"},
    "bugagents_turns": {"value": "84", "module": PROJECTS_MODULE, "profile": "84 agent turns"},
    # AgentSwarm
    "agentswarm_runs": {"value": "34", "module": PROJECTS_MODULE, "profile": "34 runs"},
    "agentswarm_chains": {"value": "35", "module": PROJECTS_MODULE, "profile": "35 ledger hash chains"},
    "agentswarm_domains": {"value": "9", "module": PROJECTS_MODULE, "profile": "9 research domains"},
    "agentswarm_artifacts": {"value": "520", "module": PROJECTS_MODULE, "profile": "520 world artifacts"},
    "agentswarm_publications": {"value": "33", "module": PROJECTS_MODULE, "profile": "33 publications"},
    "agentswarm_finding_blogs": {"value": "202", "module": PROJECTS_MODULE, "profile": "202 finding blogs"},
    "agentswarm_harnesses": {"value": "4", "module": PROJECTS_MODULE, "profile": "4 harnesses"},
    "agentswarm_oracle_calls": {
        "value": "1,254", "module": PROJECTS_MODULE,
        "profile": "1,254 tool calls", "site": "featured_projects_prose",
    },
    "agentswarm_audit": {"value": "22 of 25", "module": PROJECTS_MODULE, "profile": "22 of 25"},
    "agentswarm_tests": {
        "value": "195/224", "module": PROJECTS_MODULE,
        "profile": "195/224", "site": "featured_projects_prose", "optional": True,
    },
    # JobAgents — live 2026-10-22 numbers (scratch/GROUND_TRUTH.md supersedes the
    # 2026-10-11 profile.md snapshot; profile.md's own rule: the live site wins).
    "jobagents_jobs": {"value": "9,697", "module": PROJECTS_MODULE, "profile": "9,697",
                       "site": "live_ground_truth"},
    "jobagents_roles": {"value": "7,665", "module": PROJECTS_MODULE, "profile": "7,665",
                        "site": "live_ground_truth"},
    "jobagents_sources": {"value": "10", "module": PROJECTS_MODULE, "profile": "10 sources"},
    "jobagents_dupes": {"value": "2,032", "module": PROJECTS_MODULE, "profile": "2,032",
                        "site": "live_ground_truth"},
    "jobagents_scores": {"value": "29,091", "module": PROJECTS_MODULE, "profile": "29,091",
                         "site": "live_ground_truth"},
    "jobagents_above_threshold": {"value": "234", "module": PROJECTS_MODULE, "profile": "234",
                                  "site": "live_ground_truth"},
    "jobagents_runs": {"value": "71", "module": PROJECTS_MODULE, "profile": "71",
                       "site": "live_ground_truth"},
    "jobagents_companies": {"value": "349", "module": PROJECTS_MODULE, "profile": "349",
                            "site": "live_ground_truth"},
    "jobagents_guard": {"value": "8/8", "module": PROJECTS_MODULE, "profile": "8/8"},
    # Project Awakening
    "awakening_turns": {"value": "1,441", "module": PROJECTS_MODULE, "profile": "1,441 turns"},
    "awakening_commits": {"value": "1,553", "module": PROJECTS_MODULE, "profile": "1,553 commits"},
    "awakening_blackout": {"value": "330", "module": PROJECTS_MODULE, "profile": "330 turns"},
    # mSeat
    "mseat_candidates": {
        "value": "18,000+", "module": PROJECTS_MODULE,
        "profile": "18,000+", "site": "featured_projects_prose",
    },
    "mseat_colleges": {"value": "59", "module": PROJECTS_MODULE, "profile": "59 colleges"},
    "mseat_ranks": {"value": "73", "module": PROJECTS_MODULE, "profile": "73 ranks"},
    "mseat_compression": {"value": "90.6", "module": PROJECTS_MODULE, "profile": "90.6"},
    # Geetha
    "geetha_verses": {"value": "700", "module": PROJECTS_MODULE, "profile": "700 verses"},
    # MyLocalCLI
    "mylocalcli_version": {"value": "4.0.2", "module": PROJECTS_MODULE, "profile": "4.0.2"},
    "mylocalcli_providers": {"value": "8", "module": PROJECTS_MODULE, "profile": "8 documented"},
    "mylocalcli_tools": {"value": "42", "module": PROJECTS_MODULE, "profile": "42 built-in tools"},
    "mylocalcli_skills": {"value": "38", "module": PROJECTS_MODULE, "profile": "38 dynamic skills"},
    "mylocalcli_subagents": {"value": "5", "module": PROJECTS_MODULE, "profile": "5 specialised sub-agents"},
    # rAsh Score
    "rash_brands": {"value": "300", "module": PROJECTS_MODULE, "profile": "300 tracked brands"},
    "rash_cohorts": {"value": "20", "module": PROJECTS_MODULE, "profile": "20 industry cohorts"},
    "rash_dimensions": {"value": "4", "module": PROJECTS_MODULE, "profile": "4 independent"},
    # BrandXY
    "brandxy_lift": {"value": "76.5", "module": PROJECTS_MODULE, "profile": "76.5"},
    # Black Piano / Pi Software / Optum bullets
    "blackpiano_etl": {"value": "18", "module": PROJECTS_MODULE, "profile": "18 automated ETL pipelines"},
    "pi_dashboards": {"value": "10+", "module": PROJECTS_MODULE, "profile": "10+ client dashboards",
                      "site": "employment_verbatim"},
    "pi_reports": {"value": "30+", "module": PROJECTS_MODULE, "profile": "30+ analytical reports",
                   "site": "employment_verbatim"},
    "optum_years": {"value": "9", "module": PROJECTS_MODULE, "profile": "9 years"},
    # Resume variant (/resume/data-ai-engineer)
    "resume_bugagents_calls": {"value": "15,317", "module": RESUME_MODULE, "profile": "15,317 tool calls",
                               "site": "featured_projects_prose"},
    "resume_agentswarm_runs": {"value": "34 runs", "module": RESUME_MODULE, "profile": "34 runs"},
    "resume_agentswarm_chains": {"value": "35/35", "module": RESUME_MODULE, "profile": "35 ledger hash chains"},
    "resume_brandxy": {"value": "76.5", "module": RESUME_MODULE, "profile": "76.5"},
    "resume_mylocalcli": {"value": "4.0.2", "module": RESUME_MODULE, "profile": "4.0.2"},
    "resume_mseat": {"value": ["18,000+", "59", "73"], "module": RESUME_MODULE, "profile": "18,000+",
                     "site": "featured_projects_prose"},
    "resume_jobagents": {"value": ["9,697", "7,665"], "module": RESUME_MODULE, "profile": "9,697",
                         "site": "live_ground_truth"},
    "resume_papers": {"value": "10.5281/zenodo.23232189", "module": RESUME_MODULE,
                      "profile": "10.5281/zenodo.23232189", "site": "zenodo_record"},
}

# 6. rAsh Score naming (formerly BrandScore; bs.kprsnt.in is a stale deployment).
CANONICAL_RASH_NAME = "rash score"
CANONICAL_RASH_URL = "rashscore.live"
LEGACY_RASH_MARKERS = ("brandscore", "bs.kprsnt.in")
LEGACY_LABEL_WORDS = ("legacy", "stale", "old", "former", "deprecated")
# github.com/kprsnt2/BrandScore is the real, unrenamed repo — a source link is not
# a naming claim, so only `url` fields are held to the canonical domain.
RASH_URL_KEYS = ("url", "domain", "site", "website")


def _all_projects():
    return list(PROJECTS) + list(RESUME_PROJECTS)


# Source-code hosts: a repo link is provenance, not a naming or hosting claim.
CODE_HOSTS = ("github.com", "gitlab.com", "bitbucket.org", "npmjs.com", "pypi.org", "huggingface.co")


def _looks_like_code_url(value):
    lowered = value.strip().lower()
    return lowered.startswith("http") and any(host in lowered for host in CODE_HOSTS)


# ---------------------------------------------------------------------------
# 1. Superseded numbers
# ---------------------------------------------------------------------------

def _superseded_hits(text):
    """Return "needle -> offending line" for every superseded figure in ``text``."""
    hits = []
    for needle in SUPERSEDED_NUMBERS:
        # A leading "~", "+" or "-" is tolerated ("~7,533"), and the lookbehind
        # stops a match inside a longer number.
        pattern = re.compile(r"(?<![\d.,])[~+\-]?" + re.escape(needle), re.IGNORECASE)
        line = next((raw for raw in text.splitlines() if pattern.search(raw)), None)
        if line is not None:
            hits.append(f"{needle!r} -> {line.strip()[:140]!r}")
    for pattern in SUPERSEDED_PHRASE_PATTERNS:
        match = pattern.search(text)
        if match:
            hits.append(f"{match.group(0)!r} -> {match.group(0)[:140]!r}")
    return hits


@pytest.mark.parametrize("path,name", _module_args(), ids=[os.path.basename(p) for p in DATA_MODULES])
def test_no_superseded_numbers_in_data_modules(path, name):
    """Superseded figures may not survive in rendered values.

    A module header may name a retired figure only to forbid it ("removed as
    unsourced: 15+ dashboards"); ``test_documented_removals_are_explained``
    keeps that exemption honest.
    """
    hits = _superseded_hits("\n".join(_renderable_strings(path)))
    assert not hits, f"superseded figures in {name}:\n" + "\n".join(hits)


def _comment_blocks(path):
    """Contiguous runs of comment lines, joined — an explanation may wrap."""
    blocks, current = [], []
    for lineno, line in enumerate(_read_module(path).splitlines(), start=1):
        stripped = line.lstrip()
        if stripped.startswith("#"):
            current.append(stripped[1:])
        else:
            if current:
                blocks.append((lineno - len(current), "\n".join(current)))
            current = []
    if current:
        blocks.append((lineno - len(current) + 1, "\n".join(current)))
    return blocks


def test_documented_removals_are_explained():
    """A retired figure quoted in a comment must be explained as removed/forbidden."""
    offenders = []
    for path in DATA_MODULES:
        for start_line, block in _comment_blocks(path):
            for problem in _comment_violations(block, ("superseded", "fabricated")):
                offenders.append(f"{os.path.basename(path)}:{start_line} {problem}")
    assert not offenders, "comments that quote a ban without explaining it:\n" + "\n".join(offenders)


def test_no_superseded_numbers_in_templates():
    offenders = []
    for relpath, text in _templates():
        for hit in _superseded_hits(text):
            offenders.append(f"{relpath}: {hit}")
    assert not offenders, "superseded figures in templates:\n" + "\n".join(offenders)


# ---------------------------------------------------------------------------
# 2. Fabricated / unearned claims
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("path,name", _module_args(), ids=[os.path.basename(p) for p in DATA_MODULES])
def test_no_fabricated_claims_as_data(path, name):
    """No rendered string may assert what profile.md forbids.

    A string may quote a banned phrase only to forbid it ("never claim
    peer-reviewed"); the negating words have to sit in the same sentence.
    """
    hits = _fabrication_hits(_renderable_strings(path))
    assert not hits, (
        f"forbidden claim(s) asserted by {os.path.basename(path)}:\n" + "\n".join(hits)
    )


def test_no_fabricated_claims_in_templates():
    """Templates render copy directly, so any occurrence is a rendered claim."""
    offenders = [
        f"{relpath}: {phrase!r}"
        for relpath, text in _templates()
        for phrase in FABRICATED_CLAIMS
        if phrase.lower() in text.lower()
    ]
    assert not offenders, "templates render forbidden claims:\n" + "\n".join(offenders)


def test_no_ai_title_asserted_as_held_employment():
    """'AI Systems Engineer' / 'Agentic Engineer' may not sit next to an employer."""
    offenders = []
    for relpath in DATA_MODULES:
        name = os.path.basename(relpath)
        strings = _renderable_strings(relpath)
        for string in strings:
            if not re.search(r"\b(AI|Agentic)\b[^.]{0,40}\b(Engineer|Systems Engineer)\b", string):
                continue
            if _match_any(string, TARGET_LABEL_WORDS):
                continue
            # A keyword or label that merely names the target ("target_role") is fine.
            if "engineer" not in string.lower():
                offenders.append(f"{name}: {string[:120]!r}")
        _raw, comments, _chunks = _source_parts(relpath)
        for comment in comments:
            offenders.extend(
                f"{name} comment: {problem}"
                for problem in _comment_violations(comment, ("held_title",))
            )

    # Employment entries: the role is what HR would read as the title.
    for entry in EXPERIENCES:
        employer = entry.get("company", "")
        assert entry.get("role", "").strip().lower() in ALLOWED_HELD_TITLES, (
            f"EXPERIENCES[{employer}] asserts role {entry.get('role')!r}"
        )

    for slug, record in ROLE_RESUMES.items():
        for entry in record.get("experiences", []):
            assert str(entry.get("role", "")).strip().lower() in ALLOWED_HELD_TITLES, (
                f"ROLE_RESUMES[{slug}] asserts role {entry.get('role')!r}"
            )
        role = record.get("role") if isinstance(record.get("role"), dict) else {}
        title = str(role.get("title", ""))
        if re.search(r"\b(AI|Agentic)\b.{0,40}\bEngineer\b", title, re.IGNORECASE):
            labelled = _match_any(title, TARGET_LABEL_WORDS) or _match_any(
                role.get("description", ""), ("target", "transition", "direction")
            )
            if not labelled:
                offenders.append(
                    f"ROLE_RESUMES[{slug}]['role']['title'] inflates a held title: {title!r}"
                )

    assert not offenders, "AI/agentic title asserted as held employment:\n" + "\n".join(offenders)


# ---------------------------------------------------------------------------
# 3. Employers and dates
# ---------------------------------------------------------------------------

def _resume_experiences():
    found = []
    for slug, record in ROLE_RESUMES.items():
        for entry in record.get("experiences", []):
            found.append((slug, entry))
    return found


def _companies(entries):
    return [entry.get("company") for entry in entries]


def test_exactly_three_employers_with_profile_dates():
    expected = [(item["company"], item["role"], item["period"]) for item in EMPLOYERS]
    expected_order = [item["company"] for item in EMPLOYERS]

    def _marks(company):
        return [employer for employer in expected_order if employer in str(company)]

    # 1. Exactly three employment entries, in profile.md's order, with its dates.
    assert len(EXPERIENCES) == len(EMPLOYERS), (
        f"EXPERIENCES must hold exactly {len(EMPLOYERS)} employers, got {_companies(EXPERIENCES)}"
    )
    for entry in EXPERIENCES:
        marks = _marks(entry.get("company", ""))
        assert marks, f"EXPERIENCES has an employer profile.md never lists: {entry.get('company')!r}"
        assert len(marks) == 1, f"ambiguous employer {entry.get('company')!r} matches {marks}"
        expected_entry = expected[expected_order.index(marks[0])]
        assert entry.get("role") == expected_entry[1], (
            f"{marks[0]}: role {entry.get('role')!r} != profile.md {expected_entry[1]!r}"
        )
        assert entry.get("period") == expected_entry[2], (
            f"{marks[0]}: period {entry.get('period')!r} != profile.md {expected_entry[2]!r}"
        )

    resume_entries = [entry for _slug, entry in _resume_experiences()]
    assert len(resume_entries) == len(EMPLOYERS), (
        f"resume variants must hold exactly {len(EMPLOYERS)} employers, got {_companies(resume_entries)}"
    )
    for slug, entry in _resume_experiences():
        marks = _marks(entry.get("company", ""))
        assert marks, f"ROLE_RESUMES[{slug}] employer profile.md never lists: {entry.get('company')!r}"
        expected_entry = expected[expected_order.index(marks[0])]
        assert (entry.get("role"), entry.get("period")) == (expected_entry[1], expected_entry[2]), (
            f"ROLE_RESUMES[{slug}] {marks[0]}: role/period "
            f"{(entry.get('role'), entry.get('period'))!r} != profile.md {expected_entry[1:]!r}"
        )


def test_no_extra_employment_blocks_anywhere():
    """Any dict shaped like an employment entry must name a profile.md employer."""
    allowed = {item["company"] for item in EMPLOYERS}

    def _names_profile_employer(value):
        return isinstance(value, str) and any(employer in value for employer in allowed)

    for relpath in DATA_MODULES + [PROFILE_KBD]:
        name = os.path.basename(relpath)
        for node in ast.walk(ast.parse(_read_module(relpath))):
            if not isinstance(node, ast.Dict):
                continue
            mapping = {
                key.value: value.value if isinstance(value, ast.Constant) else None
                for key, value in zip(node.keys, node.values)
                if isinstance(key, ast.Constant) and isinstance(key.value, str)
            }
            fields = ("company", "employer", "organization", "org")
            shaped_like_job = any(mapping.get(field) for field in fields) or (
                mapping.get("role") and mapping.get("period")
            )
            if not shaped_like_job or any(_names_profile_employer(mapping.get(field)) for field in fields):
                continue
            named = next((mapping[field] for field in fields if mapping.get(field)), None)
            pytest.fail(
                f"{name}: unexpected employer-like block {named!r} "
                f"(only {sorted(allowed)} are employment; independent projects are not)"
            )


# ---------------------------------------------------------------------------
# 4. Held titles
# ---------------------------------------------------------------------------

def test_held_titles_are_only_titles_profile_md_lists():
    titles = []
    for entry in EXPERIENCES:
        titles.append((f"EXPERIENCES[{entry.get('company')}]", entry.get("role")))
    for slug, entry in _resume_experiences():
        titles.append((f"ROLE_RESUMES[{slug}]", entry.get("role")))

    for source, title in titles:
        assert title and title.strip().lower() in ALLOWED_HELD_TITLES, (
            f"{source} role {title!r} is not a title profile.md says he held"
        )

    for item in EMPLOYERS:
        assert item["role"].strip().lower() in ALLOWED_HELD_TITLES

    for slug, definition in ROLE_DEFINITIONS.items():
        for key in ("title", "resume_title", "headline"):
            value = definition.get(key)
            if not value or not re.search(r"\b(AI|Agentic)\b.{0,40}\bEngineer\b", value, re.IGNORECASE):
                continue
            labelled = _match_any(value, TARGET_LABEL_WORDS) or _match_any(
                definition.get("description", ""), ("target", "transition", "direction")
            )
            assert labelled, (
                f"ROLE_DEFINITIONS[{slug}][{key}] = {value!r} asserts an AI title as held; "
                "mark it as a target (e.g. 'Data Analyst → AI Systems Engineer')"
            )


# ---------------------------------------------------------------------------
# 5. Verified metrics
# ---------------------------------------------------------------------------

def test_verified_metrics_pins_are_internally_consistent():
    module_cache = {}

    def module_text(path):
        if path not in module_cache:
            module_cache[path] = _norm(_read_module(path))
        return module_cache[path]

    offenders = []
    for name, pin in VERIFIED_METRICS.items():
        haystack = module_text(pin["module"])
        cursor = 0
        for needle in ([pin["value"]] if not isinstance(pin["value"], list) else pin["value"]):
            # Prefer the exact phrase ("34 runs"); fall back to the bare number
            # only when the pin names a multi-word claim, never for a bare number.
            position = haystack.find(_norm(needle), cursor)
            if position < 0 and " " in needle:
                position = haystack.find(_norm(needle.split()[0]), cursor)
            if position < 0:
                if pin.get("optional"):
                    continue  # curated shortcut: may be dropped, never altered
                offenders.append(
                    f"{name}: {needle!r} not rendered by {os.path.basename(pin['module'])}"
                )
            else:
                cursor = position + 1
    assert not offenders, "verified-metric pins missing from data modules:\n" + "\n".join(offenders)


def test_verified_metrics_pins_are_citable_from_profile_md():
    profile_text = load_profile_text()
    if profile_text is None:
        pytest.skip(f"profile.md not readable at {PROFILE_MD} (expected outside the repo, e.g. CI)")

    table = parse_verified_metrics_table(profile_text)
    assert len(table) >= MIN_VERIFIED_METRICS_ROWS, (
        f"parsed only {len(table)} Verified Metrics rows - parser or profile.md format changed"
    )
    profile_norm = _norm(profile_text)

    def _candidates(needle):
        candidates = [needle]
        if " " in needle:
            candidates.append(needle.split()[0])  # "34 runs" -> "34"
        return [_norm(candidate) for candidate in candidates]

    ground_truth = None
    if os.path.exists(GROUND_TRUTH_MD):
        with open(GROUND_TRUTH_MD, encoding="utf-8") as handle:
            ground_truth = _norm(handle.read())

    missing = []
    for name, pin in VERIFIED_METRICS.items():
        needles = [pin["value"]] if not isinstance(pin["value"], list) else pin["value"]
        if ground_truth is not None and pin.get("site") == "live_ground_truth":
            # profile.md rule 11: a figure that superseded the table must be
            # re-verified against the live sites — GROUND_TRUTH.md records that.
            for needle in needles:
                if not any(candidate in ground_truth for candidate in _candidates(needle)):
                    missing.append(f"{name}: {needle!r} is not re-verified in scratch/GROUND_TRUTH.md")
            continue
        if not any(candidate in profile_norm for candidate in _candidates(pin["profile"])):
            missing.append(f"{name}: {pin['profile']!r} appears nowhere in profile.md")
        for needle in needles:
            if not any(candidate in profile_norm for candidate in _candidates(needle)):
                missing.append(f"{name}: {needle!r} appears nowhere in profile.md")
    assert not missing, (
        "numbers on the site that profile.md does not authorise:\n" + "\n".join(missing)
    )


# ---------------------------------------------------------------------------
# 6. rAsh Score naming
# ---------------------------------------------------------------------------

def test_rash_score_uses_canonical_name_and_url():
    offenders = []
    for project in _all_projects():
        label = project.get("title") or project.get("name") or ""
        if CANONICAL_RASH_NAME not in label.lower():
            continue
        urls = " ".join(str(project.get(key, "")) for key in RASH_URL_KEYS)
        assert CANONICAL_RASH_URL in urls, f"rAsh Score entry lacks {CANONICAL_RASH_URL}: {label!r}"
        for key in RASH_URL_KEYS:
            value = str(project.get(key, ""))
            for marker in LEGACY_RASH_MARKERS:
                if marker in value.lower() and not _match_any(value, LEGACY_LABEL_WORDS):
                    offenders.append(f"{label!r}[{key}]: legacy domain used canonically -> {value!r}")

    # A string may mention the legacy name/domain only if it is labelling it
    # legacy (e.g. "bs.kprsnt.in is a stale deployment"). Repo URLs are exempt:
    # github.com/kprsnt2/BrandScore is the real, unrenamed repository, and a
    # source link is not a naming claim.
    for relpath in DATA_MODULES:
        for chunk in _renderable_strings(relpath):
            if _looks_like_code_url(chunk):
                continue
            for marker in LEGACY_RASH_MARKERS:
                if marker in chunk.lower() and not _match_any(chunk, LEGACY_LABEL_WORDS):
                    offenders.append(f"{os.path.basename(relpath)} string: {chunk.strip()[:160]!r}")
    assert not offenders, "use rAsh Score / rashscore.live (legacy allowed only when labelled):\n" + "\n".join(
        offenders
    )


# ---------------------------------------------------------------------------
# 7. Offline / no-network sanity
# ---------------------------------------------------------------------------

def test_guard_is_offline():
    """This module must never import a network or LLM client.

    Inspects the AST (imports + calls), not the raw text: the banned names are
    written in this very file as string data, so a substring scan would always
    match itself.
    """
    with open(os.path.abspath(__file__), encoding="utf-8") as handle:
        tree = ast.parse(handle.read())

    banned_roots = {"requests", "httpx", "urllib", "socket", "openai", "dotenv", "anthropic", "aiohttp"}
    banned_calls = {"urlopen", "urlretrieve", "urljoin", "urlencode"}

    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    offending_imports = sorted(imported & banned_roots)
    assert not offending_imports, f"guard must stay offline; imports {offending_imports}"

    called = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                called.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                called.add(node.func.attr)
    assert not (called & banned_calls), f"guard must not call network helpers: {sorted(called & banned_calls)}"

    # The same rule for the modules under guard: they are data, not clients.
    for path in DATA_MODULES:
        module_names = set()
        for node in ast.walk(ast.parse(_read_module(path))):
            if isinstance(node, ast.Import):
                module_names.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                module_names.add(node.module.split(".")[0])
        assert not (module_names & (banned_roots | {"os", "sys", "subprocess"})), (
            f"{os.path.basename(path)} must stay a pure-data module; imports {sorted(module_names)}"
        )


def test_portfolio_kb_does_not_assert_held_ai_title():
    profile = portfolio_kb.PROFILE
    title = profile.get("title", "")
    if re.search(r"\bAI Systems Engineer\b", title) and not _match_any(title, TARGET_LABEL_WORDS):
        pytest.fail(f"portfolio_kb PROFILE['title'] asserts a held AI title: {title!r}")
    assert profile.get("current_title", "").strip().lower() in ALLOWED_HELD_TITLES, (
        f"portfolio_kb current_title {profile.get('current_title')!r} is not a held title"
    )

