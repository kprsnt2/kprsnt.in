# RFC-02: Asynchronous Multi-Agent Execution & Pipeline Latency Reduction

## Status: Proposed
## Author: Agent 9 (SOTA Trend Hunter)
## Target: scripts/ecosystem_agents.py

### Objective
Transition the sequential 10-agent execution harness to an asynchronous event loop, executing independent agent workflows concurrently to drop daily cron execution time from ~60s to <20s.

### Architecture Proposal
1. Group agents into DAG execution tiers:
   - Tier 1 (Parallel Ingestion): Agent 1 (GitHub Scout), Agent 7 (Ponytail Pruner), Agent 5 (Docs Agent), Agent 6 (Readme Agent).
   - Tier 2 (Synthesis & Auditing): Agent 2 (Dashboard Agent), Agent 3 (Portfolio Sync), Agent 4 (MCP Engineer), Agent 8 (Adversarial Bar-Raiser).
   - Tier 3 (Governance & Philosophy): Agent 9 (Trend Hunter), Agent 10 (Cosmic Observer), Swarm Memory Compaction.
2. Isolate network I/O timeouts using per-agent tasks with strict cancellation.
