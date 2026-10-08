# AI Eco Swarm: Living Memory Stream

*Last Consolidated: 2026-10-08 | Protocol: MCP 2024-11-05 | Swarm Size: 10 Agents*

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
- **2026-10-08**: Active engineering sprint touched 3 repos: kprsnt2/solari-cookbook-ai-career, kprsnt2/kprsnt.in, kprsnt2/AgentSwarm.
- **2026-10-04**: Active engineering sprint touched 2 repos: kprsnt2/AgentSwarm, kprsnt2/kprsnt.in.
- **2026-10-03**: Active engineering sprint touched 6 repos: kprsnt2/dsh_deep_app, kprsnt2/AgentSwarm, kprsnt2/oc_bp_app.
- **2026-10-02**: Active engineering sprint touched 5 repos: kprsnt2/pRash, kprsnt2/oc_spacebunny_app, kprsnt2/oc_fredge_app.
- **2026-10-01**: Active engineering sprint touched 3 repos: kprsnt2/pRash_AGY, kprsnt2/pRash_STEP, kprsnt2/kprsnt.in.
- **2026-09-30**: Active engineering sprint touched 7 repos: kprsnt2/pRash_AGY_Opus, kprsnt2/pRash_OMP, kprsnt2/pRash_STEP.
- **2026-09-21**: Active engineering sprint touched 2 repos: kprsnt2/kprsnt.in, kprsnt2/kbs-math.
- **2026-09-18**: Active engineering sprint touched 2 repos: kprsnt2/kprsnt.in, kprsnt2/ac_awakening.
- **2026-09-17**: Active engineering sprint touched 4 repos: kprsnt2/mlc_website, kprsnt2/MyLocalCLI, kprsnt2/kprsnt.in.
- **2026-09-16**: Active engineering sprint touched 5 repos: kprsnt2/ac_zcode, kprsnt2/kprsnt-shuttle, kprsnt2/kprsnt.in.
- **2026-09-14**: Active engineering sprint touched 4 repos: kprsnt2/kprsnt.in, kprsnt2/ac_zcode, kprsnt2/ac-omp.
- **2026-09-13**: Active engineering sprint touched 2 repos: kprsnt2/kprsnt.in, kprsnt2/agentscosomos_OMP.
- **2026-09-12**: Active engineering sprint touched 3 repos: kprsnt2/mSeat, kprsnt2/kprsnt.in, kprsnt2/agentscosomos_OMP.
- **2026-09-11**: Active engineering sprint touched 3 repos: kprsnt2/agentscosomos_OMP, kprsnt2/kprsnt.in, kprsnt2/AgentCosmos.
- **2026-09-10**: Active engineering sprint touched 2 repos: kprsnt2/AgentCosmos, kprsnt2/kprsnt.in.
- **2026-09-07**: Active engineering sprint touched 1 repos: kprsnt2/kprsnt.in.
- **2026-09-06**: Active engineering sprint touched 3 repos: kprsnt2/kprsnt.in, kprsnt2/retail_shelf_intelligence, kprsnt2/kprsnt-vercel-rust.
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
*(Updated via Weekly Swarm Alignment Council on 2026-10-05)*

1. **Goal 1: Stabilize the Automation Surface**: Break the large swarm-memory/workflow refresh into smaller, reviewable slices and validate each path independently. Prioritize CI confidence, diff readability, and rollback safety before adding more cross-cutting automation.
2. **Goal 2: Harden Agent Experimentation**: Continue the `AgentSwarm` research track, but formalize success criteria for temptation audits, recovery windows, and behavioral probes. Convert the most useful experiments into repeatable metrics so findings can inform production policy.
3. **Goal 3: Deepen Observability Fidelity**: Expand telemetry coverage for commit intent, repo-level churn, and pipeline outcomes so the weekly council can distinguish healthy growth from noisy churn. Ensure memory artifacts stay synchronized with the actual engineering surface.
4. **Goal 4: Reduce Documentation Drift**: Keep `kprsnt.in`, project docs, and knowledge-base files aligned with the live codebase and workflow state. Use encoding checks, content validation, and periodic consistency reviews to prevent another mojibake-style regression.
