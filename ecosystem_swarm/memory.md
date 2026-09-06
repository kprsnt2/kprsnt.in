# AI Eco Swarm: Living Memory Stream

*Last Consolidated: 2026-09-06 | Protocol: MCP 2024-11-05 | Swarm Size: 6 Agents*

---

## 🏛️ Core Portfolio Architecture
- **Host Application**: `kprsnt.in` (Flask/Python runtime on Vercel Serverless with Next.js/React frontend components).
- **Autonomous Swarm Pipeline**: `scripts/ecosystem_agents.py` executed daily via GitHub Actions (`.github/workflows/ecosystem_agents.yml`).
- **Protocol Interface**: FastMCP JSON-RPC 2.0 (`api/ai_eco_mcp.py`) supporting Stdio, HTTP (`/api/mcp`), and SSE transports.
- **Data Layers**:
  - Telemetry: `job_data/ecosystem_telemetry.json` (commit timelines, compensation benchmarks, language distributions).
  - Dev Logs: `AI_Eco_Blogs/` (structured project-by-project engineering summaries).
  - Knowledge Base: `api/data/projects.py` and `api/resume_data.py`.
  - Swarm Memory: `ecosystem_swarm/` (daily views, weekly meetings, living memory stream).

---

## 💡 Learned Engineering Patterns
- **2026-09-06**: Active engineering sprint touched 3 repos: kprsnt2/kprsnt.in, kprsnt2/retail_shelf_intelligence, kprsnt2/kprsnt-vercel-rust.
- **2026-09-06**: Active engineering sprint touched 3 repos: kprsnt2/kprsnt-vercel-rust, kprsnt2/retail_shelf_intelligence, kprsnt2/kprsnt.in.
- **2026-09-05**: Swarm steady-state maintenance: verified telemetry parity and protocol readiness.
- **2026-09-05**: Active engineering sprint touched 2 repos: kprsnt2/mSeat, kprsnt2/kprsnt.in.
1. **GitHub API Rate-Limit Protection**: Sequential commit SHA lookups must remain capped (max 8 per run) with automatic unauthenticated public fallback when `GITHUB_TOKEN` is unavailable or rate-limited.
2. **Monotonic Telemetry Retention**: Never reset historical commit totals (baseline 987); append verified new commits without synthetic multiplication.
3. **Rolling 7-Day Timeline Preservation**: Maintain `commit_timeline_7d` structures to prevent visual dashboard charts from collapsing to zero during quiet cycles.
4. **Stdio MCP Cleanliness**: Standard input/output in MCP stdio mode must NEVER leak logging or debug print statements; stdout is strictly reserved for valid JSON-RPC 2.0 frames.
5. **Deterministic Fallback Generation**: LLM synthesis calls must have robust rule-based templates so CI pipelines never break if external API keys expire or rate limit.

---

## ⚠️ Active Constraints & Boundaries
- **Context Ceiling**: Keep `memory.md` under 4,000 words. When approaching the threshold, consolidate daily insights into high-entropy engineering heuristics.
- **Serverless Timeouts**: API routes in `api/index.py` must load swarm memory with zero blocking network overhead (direct local filesystem reads with fallback).
- **Public Portfolio Privacy**: Exclude sensitive environment variables, internal tokens, or personal identifiers outside established public profile constants.

---

## 🔄 Recurring Bottlenecks & Mitigations
- **Commit SHA Resolution**: Commits fetched without full git clone can lack parent SHAs; mitigation uses GitHub Commit Details API with caching.
- **Multi-Role Parity Drift**: Changes to project tags in `api/data/projects.py` can drift from resume skill mappings; guarded by Portfolio Sync Agent validations.
- **CI Git Concurrency**: Simultaneous commits to `main` during scheduled workflow runs; mitigation uses `git pull --rebase` and atomic `git diff --quiet` guards.

---

## 🎯 Active Weekly Focus & Strategic Roadmap
*(Updated via Weekly Swarm Alignment Council on 2026-09-05)*

1. **Decoupling**: Python backend, FastMCP protocol engine, and static site generation maintain clean boundaries.
2. **Observability**: Real-time telemetry dashboard provides transparent visibility into commit cadence and skills distribution.
3. **Resilience**: The system gracefully handles missing API tokens or network latency with structured fallback mechanisms.
4. **Goal 1: Swarm Memory Orchestration**: Fully automate daily inter-agent dialogue logging and memory updates inside `scripts/ecosystem_agents.py`.
5. **Goal 2: FastMCP Memory Exposure**: Expose `eco://swarm/memory` resource and swarm inspection tools to Claude Desktop and Cursor.
6. **Goal 3: Dashboard Memory Visualization**: Integrate active swarm opinions and weekly goals directly into the `/ecosystem` web dashboard.
7. **Goal 4: Automated Compaction Guardrails**: Maintain word-count checks on `memory.md` to prevent context window overflow.
