# Adversarial Antipersona Agent: Architectural Red-Team Notes
*Audited: 2026-09-21 03:20:01 | Agent: Agent 8 (Adversarial Bar-Raiser / Antipersona) | Skill: Staff+ Architecture Stress-Testing*

## Role & Operating Philosophy
The **Antipersona Agent** acts as the swarm's adversarial red-team stress-tester. While builder agents optimize for features and velocity, the Antipersona relentlessly probes for catastrophic failure modes, cold-start timeouts, quota starvation, and hidden dependencies.

## 1. Serverless Cold Starts & Timeout Bounds (Vercel <10s)
- **Adversarial Assessment**: Dynamic LLM calls on cold lambdas can exceed Vercel's hobby execution ceiling (10s), triggering 504 Gateway Timeouts.
- **Invariant Required**: All external API calls in serverless routes must enforce hard 8-second timeouts with instant fallback to cached constants or static context.

## 2. FastMCP Transport Isolation (Stdio & SSE)
- **Adversarial Assessment**: Stray `print()` statements in Python backend contaminate the stdio JSON-RPC stream, causing Claude Desktop or Cursor clients to crash.
- **Invariant Required**: Stdio transport verified. All informational logging redirected to `sys.stderr` or file-based logging.

## 3. API Quota Blackouts & Offline Degradation
- **Adversarial Assessment**: Cloud LLM provider outages (Gemini 429 / OpenAI rate limits) must never take down the portfolio or ecosystem telemetry.
- **Invariant Required**: Inspired by Project Awakening surviving a 330-turn cloud API blackout, all swarm routines must support offline heuristic mode with zero data loss.

## 4. Living Memory Compaction Boundary
- **Adversarial Assessment**: Memory drift creates token bloat and context window degradation.
- **Invariant Required**: Strict 4,000-word ceiling enforced with automated summarization triggers.
