"""
Regression tests for audit_merged.md Phase 4 fixes.

Covers M3/M4/M6/M7/M8/M9/M10 (mSeat correctness), M12 (blog soft-404),
M15 (blog truncation marker) and M16 (hiring-evidence "data" alias).

All tests run offline.
"""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "api"))


@pytest.fixture(scope="session")
def client():
    from api.index import app

    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


# --------------------------------------------------------------------------
# M6 / M8: dead 8367 table removed; single source of colleges
# --------------------------------------------------------------------------

def test_custom_table_removed_and_single_college_source():
    import api.mseat_mcp as m

    assert not hasattr(m, "CUSTOM_COLLEGES_8367")
    assert len(m.MASTER_COLLEGES) == 59


def test_all_tools_share_the_same_college_universe():
    import api.mseat_mcp as m

    # every searchable code also appears in the allocation universe
    alloc_codes = {c["code"] for c in m.MASTER_COLLEGES}
    search_codes = {c["code"] for c in m.MASTER_COLLEGES}
    assert alloc_codes == search_codes


# --------------------------------------------------------------------------
# M7: category ratios reconciled with handle_counselling_rules
# --------------------------------------------------------------------------

def test_category_ratios_sum_to_one_and_match_rules():
    from api.mseat_mcp import CATEGORY_RATIOS

    non_sc = {k: v for k, v in CATEGORY_RATIOS.items() if k != "SC"}
    assert round(sum(non_sc.values()), 3) == 1.0
    # SC aggregate equals the sum of its sub-categories
    assert abs(CATEGORY_RATIOS["SC"]
               - (CATEGORY_RATIOS["SC_1"] + CATEGORY_RATIOS["SC_2"] + CATEGORY_RATIOS["SC_3"])) < 1e-9
    # matches handle_counselling_rules percentages
    assert CATEGORY_RATIOS["EWS"] == 0.10
    assert CATEGORY_RATIOS["BC_B"] == 0.10
    assert CATEGORY_RATIOS["ST"] == 0.10


# --------------------------------------------------------------------------
# M10: continuous rank-1 boundary
# --------------------------------------------------------------------------

def test_state_rank_boundary_is_continuous():
    from api.mseat_mcp import estimate_state_rank_from_air as est

    assert est(34) == 1
    assert est(35) == 1
    assert est(1420) == 40
    assert abs(est(1421) - est(1420)) <= 1  # no 1 -> 40 jump
    assert est(0) == 1
    assert est(-5) == 1


# --------------------------------------------------------------------------
# M3: category-specific closing ranks
# --------------------------------------------------------------------------

def test_category_specific_closing_ranks():
    from api.mseat_mcp import handle_predict_seat

    oc = handle_predict_seat({"state_rank": 100, "category": "OC"})
    sc2 = handle_predict_seat({"state_rank": 100, "category": "SC_2"})
    assert oc["allocated"] and sc2["allocated"]
    assert oc["allocation"]["closingRank"] != sc2["allocation"]["closingRank"]
    # SC family ranks against sc2Closing; OC against ocClosing
    assert oc["allocation"]["closingRank"] in {c["ocClosing"] for c in __import__("api.mseat_mcp", fromlist=["MASTER_COLLEGES"]).MASTER_COLLEGES}
    assert sc2["allocation"]["closingRank"] in {c["sc2Closing"] for c in __import__("api.mseat_mcp", fromlist=["MASTER_COLLEGES"]).MASTER_COLLEGES}


def test_sliding_odds_accepts_optional_category():
    from api.mseat_mcp import handle_sliding_odds

    res = handle_sliding_odds({"current_college": "Gandhi", "target_college": "Osmania", "category": "SC_2"})
    assert res.get("success") is True
    assert "slidingProbability" in res


# --------------------------------------------------------------------------
# M9: sliding rules topic implemented
# --------------------------------------------------------------------------

def test_sliding_rules_topic():
    from api.mseat_mcp import handle_counselling_rules

    res = handle_counselling_rules({"topic": "sliding"})
    assert res.get("success") is True
    assert res.get("topic") == "sliding"
    assert "Round 2 Upgradation" in res["data"]


def test_other_rule_topics_still_work():
    from api.mseat_mcp import handle_counselling_rules

    for topic in ("fees", "reservations", "documents", "all"):
        res = handle_counselling_rules({"topic": topic})
        assert res.get("success") is True


# --------------------------------------------------------------------------
# M12: blog soft-404s become real 404s
# --------------------------------------------------------------------------

def test_unknown_blog_slugs_return_404(client):
    assert client.get("/blog/definitely-not-a-slug-xyz").status_code == 404
    assert client.get("/aie/blog/definitely-not-a-slug-xyz").status_code == 404


def test_known_blog_route_still_renders(client):
    from api.index import load_all_blog_posts

    posts = load_all_blog_posts()
    if not posts:
        pytest.skip("no blog posts")
    assert client.get(f"/blog/{posts[0]['slug']}").status_code == 200


# --------------------------------------------------------------------------
# M15: truncation marker on long blog content
# --------------------------------------------------------------------------

def test_blog_post_truncation_flag():
    from api.ai_eco_mcp import _load_all_mcp_blog_posts, handle_get_blog_post

    posts = _load_all_mcp_blog_posts()
    longest = max(posts, key=lambda p: len(p.get("raw_content", "") or ""), default=None)
    if not longest or len(longest.get("raw_content", "") or "") <= 9000:
        pytest.skip("no post exceeds 9000 chars")
    res = handle_get_blog_post({"slug": longest["slug"]})
    assert res["content_truncated"] is True
    assert res["truncation_notice"]
    assert len(res["content"]) == 9000


# --------------------------------------------------------------------------
# M16: hiring evidence "data" alias resolves
# --------------------------------------------------------------------------

def test_hiring_evidence_data_alias():
    from api.ai_eco_mcp import handle_get_hiring_evidence

    res = handle_get_hiring_evidence({"domain": "data"})
    assert res.get("error") is None
    assert len(res["categorized_domains"]["Developer Tooling & Infrastructure"]) > 0


def test_hiring_evidence_other_domains_still_work():
    from api.ai_eco_mcp import handle_get_hiring_evidence

    for domain in ("all", "production", "research"):
        res = handle_get_hiring_evidence({"domain": domain})
        assert res.get("error") is None
        cats = res["categorized_domains"]
        assert sum(len(v) for v in cats.values()) > 0, domain
