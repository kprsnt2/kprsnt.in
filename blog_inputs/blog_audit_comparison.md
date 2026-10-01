# 🔍 When AI Audits AI: What Happens When You Cross-Examine AI-Generated Code

**The surprising results of using StepCode and Antigravity (agy) to audit each other's work**

*Published: September 27, 2026 | Reading Time: ~8 minutes*

---

## The Setup

After having 6 AI coding tools build the same application (see: [The Full Comparison](./blog_mega_comparison.md)), I did something unusual: I used the AIs to **audit each other's code**.

- **StepCode CLI** (Step 5 Preview model) audited 5 projects built by other tools
- **Antigravity (agy) CLI** (Gemini Flash 3.8) audited the StepCode project

The question: Can AI effectively review AI-generated code? And does the auditor matter?

---

## The Auditors Compared

### StepCode as Auditor: The Spec-Level Detective 🕵️

StepCode's audits were **surgical**. It found bugs that required deep knowledge of browser APIs and cloud platform constraints:

**🔴 Most Impressive Find — IndexedDB Spec Violation (StepCode project audit by Antigravity (agy))**
> `getAllFromIndex("messages", "byChat", [chatId, -Infinity])` — According to W3C IndexedDB spec §3.1.2, `-Infinity` is an **invalid key**. Passing it inside an array does exact equality matching, not range matching. **No messages will ever match this query.** Saved chats silently disappear on reload.

**🔴 Vite vs Next.js Incompatibility**
> `import pdfWorkerUrl from "pdfjs-dist/build/pdf.worker.min.mjs?url"` — The `?url` suffix is Vite-specific. Next.js (Webpack/Turbopack) doesn't support it. The PDF worker silently fails at runtime.

**🔴 Vercel Payload Ceiling**
> The app allows 20 files × 25MB, but Vercel's serverless gateway enforces a hard **4.5MB** request body limit. A single smartphone photo (~5MB → ~6.7MB base64) crashes with `413 Payload Too Large`.

### Antigravity (agy) as Auditor: The Security Architect 🏗️

Antigravity (agy)'s audits took a **broader, architectural view**:

**🔴 Universal Authentication Gap**
> Identified across 4 projects that `/api/chat` has zero authentication — anyone can POST requests and drain paid API keys.

**🔴 Forgeable Auth Tokens**
> In the Antigravity (agy) + Opus project: the `GET /api/auth` endpoint validates tokens by checking `if (token && token.trim() !== '')` — it literally accepts ANY non-empty string as valid.

**🟠 Vision/Fallback Mismatch**
> When images are sent to vision-capable models but fallback occurs to text-only models (NVIDIA/Groq), the image data is still sent → second failure → "All models failed."

---

## Side-by-Side Audit Quality

| Dimension | StepCode (Step 5 Preview) | Antigravity (agy) + Gemini Flash 3.8 |
|-----------|--------------------------|------------------------|
| **Bug Depth** | Runtime/spec-level (IDB queries, Vite syntax, payload limits) | Architecture/security-level (auth gaps, missing headers) |
| **Scoring System** | Quantified 10-point scorecard per subsystem | P0–P3 severity classification |
| **Actionable Fixes** | Code snippets with exact replacements | Recommendations with effort estimates (S/M/L) |
| **False Positives** | Low — findings verified against specs | Low — findings backed by file:line references |
| **Remediation Plan** | 5-phase roadmap with Mermaid diagram | 4-phase plan with verification checklists |
| **Overall Tone** | Technical, specification-focused | Strategic, risk-focused |

### The Verdict on Auditors

**StepCode found the bugs that crash your app. Antigravity (agy) found the bugs that drain your wallet.**

Both perspectives are essential. The ideal workflow:
1. Use a **spec-level auditor** (like StepCode) to find correctness/runtime bugs
2. Use a **security-focused auditor** (like Antigravity (agy)) to find architectural vulnerabilities
3. Combine both reports into a unified remediation plan

---

## What the Audits Revealed About Each Project

| Project | Audit By | Worst Finding | # Critical Issues |
|---------|----------|---------------|-------------------|
| Antigravity (agy) + Gemini | StepCode | PDFs silently dropped, broken provider URLs | 4 |
| Antigravity (agy) + Opus | StepCode | Login accepts any token, non-image files dropped | 5 Critical + 4 High |
| OMO DeepSeek | StepCode | Attachment text lost on save, extraction error blanks messages | 0 Critical (best!) |
| OMP Gemini | StepCode | XLSX parsing broken, multi-turn context dropped | 1 High + 3 Medium |
| PI DeepSeek | StepCode | No rate limiting on passcode, broken ESLint | 0 Critical |
| StepCode Step5 | Antigravity (agy) + Gemini | IDB queries return empty, PDF worker fails | 4 Critical + 5 High |

**The pattern is clear:** DeepSeek projects (OMO and PI) had **zero critical issues**. The Gemini and Opus projects had the most. StepCode had deep architectural quality but critical implementation bugs.

---

## Lessons for AI-Assisted Development

### 1. Always Cross-Audit
Never let the same AI model that wrote the code also review it. Different models catch different classes of bugs.

### 2. Spec-Level Bugs Are the Deadliest
The IndexedDB `-Infinity` bug is invisible to linters, type checkers, and even `next build`. It only manifests at runtime, silently. Only a model with deep browser API knowledge would catch it.

### 3. Security Is the Consistent Blind Spot
Across all 6 projects, security was the weakest category. AI models optimize for "making it work" and consistently skip authentication, rate limiting, and security headers.

### 4. The Audit Report Format Matters
StepCode's quantified scorecard (3/10 for Core Functionality) immediately communicates severity. Antigravity (agy)'s P0–P3 system is more granular but requires reading the full report to assess overall health.

---

*For the full 6-way comparison including code examples and scoring, read [The Mega Blog Post](./blog_mega_comparison.md).*
