# Adversarial Antipersona Agent: Architectural Red-Team Notes
*Audited: 2026-09-21 10:39:10 | Agent: Agent 8 (Adversarial Bar-Raiser / Antipersona) | Skill: Staff+ Architecture Stress-Testing*

## Role & Operating Philosophy
The **Antipersona Agent** acts as the swarm's adversarial red-team stress-tester. While builder agents optimize for features and velocity, the Antipersona relentlessly probes for catastrophic failure modes, cold-start timeouts, quota starvation, and hidden dependencies.

## 1. Serverless Cold Starts & Timeout Bounds (Vercel <10s)
- **Live Verification**: Passed (LLM_TIMEOUT=8.0s <= 8.0s enforced)
- **Invariant Required**: All external API calls in serverless routes must enforce hard 8-second timeouts with instant fallback to cached constants or static context.

## 2. FastMCP Transport Isolation (Stdio & SSE)
- **Live Verification**: Passed (16 FastMCP tools responsive, JSON-RPC 2.0 valid)
- **Invariant Required**: Stdio transport verified. All informational logging redirected to `sys.stderr` or file-based logging.

## 3. API Quota Blackouts & Offline Degradation
- **Live Verification**: Passed (8-SHA cap with unauthenticated public fallback active)
- **Invariant Required**: Inspired by Project Awakening surviving a 330-turn cloud API blackout, all swarm routines must support offline heuristic mode with zero data loss.

## 4. Living Memory Compaction Boundary
- **Live Verification**: Passed (665/4,000 words, 83.4% headroom)
- **Invariant Required**: Strict 4,000-word ceiling enforced with automated summarization triggers.
