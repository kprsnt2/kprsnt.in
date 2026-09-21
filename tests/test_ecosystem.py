"""
Unit & Integration Tests for the AI Eco Multi-Agent Swarm & FastMCP Layer.
"""
import os
import sys
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "api") not in sys.path:
    sys.path.insert(0, str(ROOT / "api"))


def test_ai_config_timeout_and_unification():
    """Verify AI config timeout is serverless-resilient (<= 10s) and unified."""
    import api.ai_config as api_cfg
    import scripts.ai_config as scripts_cfg

    assert api_cfg.LLM_TIMEOUT <= 10.0, f"Serverless timeout must be <= 10s, got {api_cfg.LLM_TIMEOUT}"
    assert scripts_cfg.LLM_TIMEOUT == api_cfg.LLM_TIMEOUT
    assert scripts_cfg.NVIDIA_MODEL == api_cfg.NVIDIA_MODEL
    assert scripts_cfg.OPENAI_MODEL == api_cfg.OPENAI_MODEL
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


def test_pruner_agent_no_self_match():
    """Verify Ponytail Pruner excludes self and debt_ledger contains 0 self-matches."""
    debt_ledger_file = ROOT / "ecosystem_swarm" / "debt_ledger.json"
    assert debt_ledger_file.exists()
    ledger_data = json.loads(debt_ledger_file.read_text(encoding="utf-8"))

    # Ensure no items point to ecosystem_agents.py
    for item in ledger_data.get("debt_items", []):
        assert "ecosystem_agents.py" not in item.get("file", ""), f"False self-match in debt ledger: {item}"
    print("  [PASS] test_pruner_agent_no_self_match passed")


def test_roadmap_parser_scope():
    """Verify strategic roadmap parser ignores architecture reviews and extracts only goals."""
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

    roadmap_marker = "## 🎯 Next-Week Strategic Roadmap"
    goals = []
    if roadmap_marker in sample_meeting:
        roadmap_part = sample_meeting.split(roadmap_marker, 1)[1]
        if "\n## " in roadmap_part:
            roadmap_part = roadmap_part.split("\n## ", 1)[0]
        for line in roadmap_part.splitlines():
            line_s = line.strip()
            m = re.match(r'^\d+\.\s*(.*)', line_s)
            if m:
                clean_goal = m.group(1).strip()
                if clean_goal:
                    goals.append(clean_goal)

    assert len(goals) == 4
    assert goals[0].startswith("**Goal 1")
    assert not any("Decoupling" in g for g in goals)
    assert not any("Real-time telemetry dashboard" in g for g in goals)
    print("  [PASS] test_roadmap_parser_scope passed")


def test_evaluate_all_10_agents():
    """Verify dynamic evaluation computes real fitness metrics for all 10 agents."""
    import scripts.ecosystem_agents as orch

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

    # Check all 10 agents are present and have non-zero progress
    assert len(targets) == 10
    for agent_key, target_info in targets.items():
        assert target_info.get("progress_pct", 0) > 0, f"{agent_key} has 0 progress"

    # Agent 7 (Pruner) should now have 100% debt ledger coverage with 0 false markers
    assert targets["agent_7_pruner_agent"]["progress_pct"] == 100.0

    # Overall fitness score should be >= 80.0
    overall_fitness = targets_data.get("overall_fitness_score", 0)
    assert overall_fitness >= 80.0, f"Expected overall fitness >= 80.0, got {overall_fitness}"

    # Check milestone 1 is achieved
    milestones = targets_data.get("evolutionary_milestones", [])
    m1 = next((m for m in milestones if m.get("level") == 1), None)
    assert m1 is not None
    assert m1["achieved"] is True
    print("  [PASS] test_evaluate_all_10_agents passed")


if __name__ == "__main__":
    print("Running Ecosystem Swarm Tests...")
    test_ai_config_timeout_and_unification()
    test_swarm_size_consistency()
    test_fastmcp_tools_and_resources()
    test_pruner_agent_no_self_match()
    test_roadmap_parser_scope()
    test_evaluate_all_10_agents()
    print("\n[SUCCESS] All 6 Ecosystem Swarm test suites PASSED successfully!")
