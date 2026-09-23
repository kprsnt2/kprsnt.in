"""
Unit & Integration Tests for the AI Eco Multi-Agent Swarm & FastMCP Layer.
"""
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "api") not in sys.path:
    sys.path.insert(0, str(ROOT / "api"))


def test_ai_config_timeout_and_unification():
    """Config must be single-sourced: scripts.ai_config re-exports api.ai_config.

    Identity (not equality) proves no silent fallback duplicate exists (audit T5).
    """
    import api.ai_config as api_cfg
    import scripts.ai_config as scripts_cfg

    assert api_cfg.LLM_TIMEOUT <= 10.0, f"Serverless timeout must be <= 10s, got {api_cfg.LLM_TIMEOUT}"
    assert scripts_cfg.LLM_TIMEOUT == api_cfg.LLM_TIMEOUT
    assert scripts_cfg.OPENAI_MODEL is api_cfg.OPENAI_MODEL
    assert scripts_cfg.NVIDIA_MODEL is api_cfg.NVIDIA_MODEL
    print("  [PASS] test_ai_config_timeout_and_unification passed")


def test_swarm_size_consistency():
    """Verify all contracts, memory headers, and tools reference 10 agents."""
    import scripts.ecosystem_agents as orch
    assert orch.SWARM_SIZE == 10

    memory_path = ROOT / "ecosystem_swarm" / "memory.md"
    assert memory_path.exists()
    content = memory_path.read_text(encoding="utf-8")
    assert "Swarm Size: 10 Agents" in content

    from api.ai_eco_mcp import handle_site_overview, handle_prompt_get
    overview = handle_site_overview({})
    features = overview.get("interactive_features", [])
    assert any("10-Agent Autonomous Swarm" in f for f in features)

    prompt_res = handle_prompt_get("ai_eco_overview", {})
    messages = prompt_res.get("messages", [])
    assert len(messages) > 0
    prompt_text = messages[0]["content"]["text"]
    assert "10 specialized agents" in prompt_text
    print("  [PASS] test_swarm_size_consistency passed")


def test_fastmcp_tools_and_resources():
    """Verify FastMCP tool list and JSON-RPC dispatch."""
    from api.ai_eco_mcp import process_mcp_request

    # Test tools/list
    req = {"jsonrpc": "2.0", "id": "t1", "method": "tools/list"}
    resp = process_mcp_request(req)
    assert resp.get("jsonrpc") == "2.0"
    tools = resp.get("result", {}).get("tools", [])
    assert len(tools) >= 15

    # Check that get_swarm_daily_views describes 10 perspectives
    daily_tool = next((t for t in tools if t["name"] == "get_swarm_daily_views"), None)
    assert daily_tool is not None
    assert "10 active perspectives" in daily_tool["description"]

    # Test resources/list
    req_res = {"jsonrpc": "2.0", "id": "r1", "method": "resources/list"}
    resp_res = process_mcp_request(req_res)
    assert resp_res.get("jsonrpc") == "2.0"
    resources = resp_res.get("result", {}).get("resources", [])
    assert len(resources) >= 5
    print("  [PASS] test_fastmcp_tools_and_resources passed")


def test_pruner_excludes_self_and_tests():
    """The pruner's exclusion predicate must drop orchestrator/MCP/test files (audit T2)."""
    from scripts.ecosystem_agents import _is_pruner_excluded

    assert _is_pruner_excluded(Path("scripts/ecosystem_agents.py"))
    assert _is_pruner_excluded(Path("api/ai_eco_mcp.py"))
    assert _is_pruner_excluded(Path("tests/test_ecosystem.py"))
    assert not _is_pruner_excluded(Path("api/index.py"))
    print("  [PASS] test_pruner_excludes_self_and_tests passed")


def test_ledger_respects_exclusion_rule():
    """The live debt ledger must contain no excluded (self-matched) files."""
    from scripts.ecosystem_agents import _is_pruner_excluded

    debt_ledger_file = ROOT / "ecosystem_swarm" / "debt_ledger.json"
    assert debt_ledger_file.exists()
    ledger_data = json.loads(debt_ledger_file.read_text(encoding="utf-8"))

    for item in ledger_data.get("debt_items", []):
        assert not _is_pruner_excluded(ROOT / item.get("file", "")), f"Excluded file in debt ledger: {item}"
    print("  [PASS] test_ledger_respects_exclusion_rule passed")


def test_roadmap_parser_scope():
    """Strategic roadmap parser must ignore architecture reviews (audit T3):
    this test now calls the PRODUCTION parser, not a re-implementation."""
    from api.ai_eco_mcp import parse_strategic_roadmap

    sample_meeting = """# Swarm Alignment Council: Weekly Meeting 2026-W38
*Session Date: 2026-09-21 | Quorum: 10/10 Agents Present*

## 🧠 Collective Opinion on Architecture Quality
The swarm evaluates the current architectural posture as Strong & Maturing:
1. **Decoupling**: Python backend, FastMCP protocol engine, and static site generation maintain clean boundaries.
2. **Observability**: Real-time telemetry dashboard provides transparent visibility into commit cadence.
3. **Resilience**: The system gracefully handles missing API tokens.

## 🎯 Next-Week Strategic Roadmap (Prioritized Goals)
1. **Goal 1: Stabilize Memory Spine**: Keep living memory unified.
2. **Goal 2: Cross-Repo Coordination**: Synchronize policies.
3. **Goal 3: Operational Observability**: Extend failure alerting.
4. **Goal 4: Durable Releases**: Release verified increments.
"""

    goals = parse_strategic_roadmap(sample_meeting)

    assert len(goals) == 4
    assert goals[0].startswith("**Goal 1")
    assert not any("Decoupling" in g for g in goals)
    assert not any("Real-time telemetry dashboard" in g for g in goals)
    print("  [PASS] test_roadmap_parser_scope passed")


def test_evaluate_all_10_agents(tmp_path, monkeypatch):
    """Dynamic evaluation computes real fitness metrics for all 10 agents.

    Uses a seeded temp fixture for the swarm dir instead of live mutable
    artifacts (audit T4/T7); asserts ranges rather than exact live values.
    """
    import scripts.ecosystem_agents as orch

    # Seed temp fixtures: copy the live targets.json shape, control the ledger
    live_dir = ROOT / "ecosystem_swarm"
    targets_src = live_dir / "targets.json"
    assert targets_src.exists(), "live targets.json is the registry fixture"
    (tmp_path / "targets.json").write_text(targets_src.read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "debt_ledger.json").write_text(json.dumps({
        "last_audited": "2026-09-23T00:00:00",
        "total_markers": 4,
        "markers_without_trigger": 0,
        "debt_items": []
    }), encoding="utf-8")
    monkeypatch.setattr(orch, "SWARM_DIR", tmp_path)

    dummy_stats = {
        "repo_counts": 100,
        "language_breakdown": {"TypeScript": 26, "Python": 19},
        "commit_history": 1124,
        "recent_activity": ["[kprsnt2/kprsnt.in] commit abc1234: test update"],
        "recent_commits": [{"sha": "abc1234", "repo": "kprsnt2/kprsnt.in", "message": "test update"}],
        "active_repos_touched": ["kprsnt2/kprsnt.in"]
    }

    targets_data = orch.evaluate_swarm_targets(dummy_stats, save=False)
    assert targets_data
    targets = targets_data.get("targets", {})

    assert len(targets) == 10
    for agent_key, target_info in targets.items():
        assert 0 <= target_info.get("progress_pct", 0) <= 100, f"{agent_key} progress out of range"

    # Pruner coverage with a fully-triggered fixture ledger must be 100%
    assert targets["agent_7_pruner_agent"]["progress_pct"] == 100.0

    overall_fitness = targets_data.get("overall_fitness_score", 0)
    assert 0 <= overall_fitness <= 100.0

    milestones = targets_data.get("evolutionary_milestones", [])
    m1 = next((m for m in milestones if m.get("level") == 1), None)
    assert m1 is not None
    print("  [PASS] test_evaluate_all_10_agents passed")


if __name__ == "__main__":
    print("Running Ecosystem Swarm Tests...")
    test_ai_config_timeout_and_unification()
    test_swarm_size_consistency()
    test_fastmcp_tools_and_resources()
    test_pruner_excludes_self_and_tests()
    test_ledger_respects_exclusion_rule()
    test_roadmap_parser_scope()
    print("\n[SUCCESS] All Ecosystem Swarm test suites PASSED successfully!")
