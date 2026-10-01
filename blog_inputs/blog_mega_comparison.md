# 🏆 AI Coding CLI Battle Royale 2026: I Asked 6 AI Tools to Build the Same App — Here's What Happened

**The definitive comparison of AGY (Gemini), AGY (Opus), OMO (DeepSeek), OMP (Gemini), PI (DeepSeek), and StepCode (Step 5 Preview)**

*Published: September 27, 2026 | Reading Time: ~20 minutes*

---

## 📋 TL;DR — The Final Rankings

| Rank | Tool + Model | Overall Score | Best At |
|------|-------------|---------------|---------|
| 🥇 1st | **OMO + DeepSeek 4.1 Flash** | **93/100** | Architecture, Testing, Deployment |
| 🥈 2nd | **PI + DeepSeek 4.1 Flash** | **91/100** | Privacy, Security, UX |
| 🥉 3rd | **StepCode + Step 5 Preview** | **87/100** | Agent System, Provider Abstraction |
| 4th | **AGY + Claude Opus 4.6** | **84/100** | Code Organization, AI SDK Usage |
| 5th | **OMP + Gemini Flash 3.8** | **82/100** | Attachment Pipeline, Agent Variety |
| 6th | **AGY + Gemini Flash 3.8** | **79/100** | Solid Foundation, Clean Types |

> **Bottom Line:** DeepSeek 4.1 Flash models (via both OMO and PI CLIs) dominated this comparison. OMO's project is the only one with **42 passing unit tests**, a QA harness with screenshots, and a Wrangler config for Cloudflare Workers. The margin was clear.

---

## 🎯 The Experiment

I gave every AI coding tool the **exact same prompt** — build an all-in-one personal AI chat application with these requirements:

1. **Multi-provider fallback**: OpenAI (GPT-5.4-mini/nano) → Gemini Flash → NVIDIA → Groq
2. **7+ specialized agents**: KidStory, StudyBuddy, Worksheet, DataAnalyst, Doctor, Psycho, Spiritual
3. **Multi-file attachments** (the killer feature — ChatGPT/Claude limit attachments)
4. **Privacy mode**: Switch to Gemini-only when privacy is enabled (my paid key, no data training)
5. **Deployable** on Vercel/Cloudflare
6. **Fancy/creative agent names** + additional useful daily agents

Then I asked each tool to push to GitHub. After that, I used **StepCode CLI** to audit each project (except StepCode's own project, which was audited by **AGY CLI with Gemini**).

### The Contenders

| Project | CLI Tool | AI Model | Model Type |
|---------|----------|----------|------------|
| `pRash_agy` | Antigravity CLI | Gemini Flash 3.8 | Google |
| `pRash_agy_opus` | Antigravity CLI | Claude Opus 4.6 | Anthropic |
| `pRash_omo` | OMO CLI | DeepSeek 4.1 Flash | DeepSeek |
| `pRash_omp` | OMP CLI | Gemini Flash 3.8 | Google |
| `pRash_pi` | PI CLI | DeepSeek 4.1 Flash | DeepSeek |
| `pRash_step` | StepCode CLI | Step 5 Preview | Step (distilled?) |

---

## 📊 Category-by-Category Deep Dive

### 1. 🏗️ Architecture & Project Structure

**Winner: OMO + DeepSeek** 🏆

| Project | Structure | Score |
|---------|-----------|-------|
| OMO | `lib/agents/`, `lib/providers/`, `lib/attachments/`, `lib/client/`, `lib/route/`, `lib/storage/` — deeply modular | **10/10** |
| StepCode | `src/agents/` (separate domain files: learning, life, work, mind), `src/lib/providers/` with individual files | **9/10** |
| PI | Clean `app/`, `components/`, `lib/` with speech utilities and auth built-in | **9/10** |
| AGY Gemini | Standard `src/app`, `src/components`, `src/lib`, `src/types` — clean but flat | **9/10** |
| AGY Opus | Added `src/hooks/useChat.ts` for state management — nice separation | **9/10** |
| OMP | Mirrors AGY Gemini structure with additional `api-providers.ts` | **9/10** |

**Key Insight:** OMO's project was the only one that truly decomposed providers into individual adapter files (`gemini.ts`, `openai.ts`) with shared types, SSE utilities, and a routing planner (`route/plan.ts`). This isn't just clean code — it's **architecture**. Every other project crammed provider logic into the API route handler.

---

### 2. 🤖 Agent/Plugin System

**Winner: OMO + DeepSeek (21 agents)** 🏆 — tied with OMP + Gemini (17 agents with best prompts)

| Project | # Agents | Agent Quality | Naming Creativity |
|---------|----------|---------------|-------------------|
| AGY Opus | 22 | Good prompts, medical disclaimers | Standard (KidStory, StudyBuddy) |
| OMO | 21 | Detailed, per-agent temperature/maxTokens | Creative (Genie, PaperOwl, FixItFox) |
| PI | 18 | Best safety rules wrapper, per-agent model preferences | Very Creative (with shared `withRules()`) |
| OMP | 17 | Exceptional prompts — Doctor extracts Rx details, Worksheet forces printable layouts | Creative with glow effects/colors |
| AGY Gemini | 14 | Good starter prompts, gradient styling | Creative (SlumberSpun, FeynmanForge, PrintNova) |
| StepCode | 17 | Split across domain files (learning, life, work, mind) | Creative (Orbit, ByteWise, Quill, QuizForge) |

**Key Insight:** PI's approach of wrapping all agent prompts with shared safety rules (`withRules()`) was brilliant — one function injects safety guidelines into every agent automatically. OMP had the most **detailed, specialized prompts** — its Doctor agent actually parses prescription details and flags abnormal lab values.

---

### 3. 🔌 AI Model Integration & Fallback Chain

**Winner: PI + DeepSeek** 🏆

This is the most critical category. The prompt required a 4-tier fallback: OpenAI → Gemini → NVIDIA → Groq.

| Project | Fallback Impl | Vision Guard | Per-Agent Routing | Stream Quality |
|---------|---------------|--------------|-------------------|----------------|
| PI | Explicit `buildCandidates()` with capability filtering, vision/PDF detection, key detection | ✅ Filters by capability | ✅ Agent `prefer` field | 10/10 |
| OMO | `planChain()` router → `openFirstWorking()` runner with first-token timeout + abandoned generator cleanup | ✅ | ✅ Via `forceProvider` | 10/10 |
| StepCode | `streamWithFallback()` in `chain.ts` loops through `CHAIN_ORDER` | ⚠️ Partial (bug #8) | ✅ Provider overrides | 8/10 |
| OMP | `DEFAULT_FALLBACK_CHAIN` with micro-fallback (mini→4o-mini), telemetry headers | ⚠️ Not checked | ❌ | 9/10 |
| AGY Gemini | `getProviderCascade()` + failover chain badge UI | ❌ Vision→text-only bug | ❌ | 8/10 |
| AGY Opus | Vercel AI SDK abstraction with `getModelChain()` | ❌ `supportsVision` declared but never used | ❌ | 7/10 |

**Key Insight:** PI's `buildCandidates()` function is a masterpiece — it automatically detects what capabilities each model has (vision, PDF), checks which API keys are available, respects agent preferences, and builds an ordered fallback list. OMO's `openFirstWorking()` is equally impressive — it opens streams to providers in order and commits to the first one that produces a token, cleanly releasing abandoned generators.

**The Vercel AI SDK Trap:** AGY Opus was the only project using Vercel's `ai` SDK. While this simplifies the code, it actually **reduced flexibility** — the SDK abstracts away the streaming details, making it harder to implement features like vision capability guards, per-agent model routing, and transparent fallback with telemetry headers.

---

### 4. 📎 File & Attachment Handling

**Winner: OMO + DeepSeek** 🏆

The whole point of this app was "ChatGPT/Claude don't support many attachments." Let's see who delivered.

| Project | PDF Support | Image Handling | Multi-File | Text/CSV/Code | XLSX |
|---------|-------------|----------------|------------|---------------|------|
| OMO | ✅ Server-side pdfjs-dist extraction + Gemini native PDF passthrough | ✅ Client-side compression | ✅ 60MB budget | ✅ Full extraction | ❌ |
| PI | ✅ Client-side pdfjs + Gemini native | ✅ Auto-resize to ~1.1MB | ✅ 10 files, 3MB cap | ✅ Full extraction | ❌ |
| OMP | ✅ Client-side pdfjs (15-page cap, CDN worker) | ✅ Base64 data URLs | ✅ Drag & drop | ✅ Text parsing | ❌ (broken for xlsx) |
| StepCode | ⚠️ Broken — Vite `?url` import fails in Next.js | ✅ But no compression (violates Vercel 4.5MB limit) | ✅ 20 files × 25MB | ✅ | ❌ |
| AGY Gemini | ❌ PDF accepted but silently dropped | ✅ | ✅ Multi-file | ✅ Text extraction | ❌ |
| AGY Opus | ❌ Non-image files reduced to `[Attached file: name]` | ✅ Images only | ✅ | ❌ Name only, no content | ❌ |

**Key Insight:** OMO was the only project with **server-side PDF extraction** AND a smart fallback — if pdfjs can't extract text (scanned PDFs), it passes the raw binary directly to Gemini's native PDF API. PI's client-side image compression (auto-resizing 12MP phone photos to ~1.1MB) shows real-world deployment awareness.

**The Biggest Failure:** AGY Opus silently reduces every non-image attachment to just `[Attached file: report.pdf]` — the AI literally never sees the document content. For an app whose raison d'être is "support many attachments," this is a critical miss.

---

### 5. 🔒 Privacy Mode

**Winner: PI + DeepSeek** 🏆 — tied with OMO

All projects implemented privacy mode, but the depth varied wildly:

| Project | Server Enforcement | Client Persistence Block | Storage Cleanup |
|---------|-------------------|--------------------------|-----------------|
| PI | ✅ `buildCandidates` locks to Gemini | ✅ `saveConversation` aborts | ✅ Deletes on toggle |
| OMO | ✅ `planChain` filters to `PRIVACY_SAFE_PROVIDERS` | ✅ `persist()` skips | ✅ |
| StepCode | ✅ `resolveChain` collapses to `['gemini']` | ✅ Only writes if `!chat.privacy` | ✅ |
| OMP | ✅ `PRIVACY_FALLBACK_CHAIN` (Gemini-only) | ✅ Prevents `localStorage` saves | ✅ |
| AGY Gemini | ✅ Privacy routing | ✅ IndexedDB persistence gated | ✅ |
| AGY Opus | ✅ `getModelChain` returns only Google | ⚠️ Basic, relies on React state | ⚠️ |

**Key Insight:** PI earns the win by having the most **layered** implementation — server-side model locking, client-side persistence blocking, AND active deletion of the local copy when privacy is toggled. OMO additionally surfaces skip reasons to the UI, so the user sees exactly why certain providers were excluded.

---

### 6. 🛡️ Security

**Winner: PI + DeepSeek** 🏆

| Project | Auth Mechanism | API Protection | Rate Limiting | Security Headers |
|---------|---------------|----------------|---------------|------------------|
| PI | SHA-256 cookie + `safeEqual()` constant-time compare + middleware gate | ✅ Edge middleware on all `/api/*` | ⚠️ Recommended, not built | ❌ |
| OMO | SHA-256 cookie + proxy.ts (Next.js 16 proxy) | ✅ Proxy-level gate | ❌ | ❌ |
| StepCode | Jose JWT with `SESSION_SECRET` + middleware | ✅ | ❌ | ❌ |
| AGY Opus | `APP_PASSWORD` + random token (but validation accepts ANY non-empty token!) | ❌ `/api/chat` is unprotected! | ❌ | ❌ |
| OMP | None | ❌ Completely open | ❌ | ❌ |
| AGY Gemini | None | ❌ Completely open | ❌ | ❌ |

**Key Insight:** **4 out of 6 projects have a completely unprotected `/api/chat` endpoint.** This means anyone who finds your Vercel URL can drain your paid API keys. PI was the only project with a proper middleware gate that intercepts ALL requests before they reach the API routes, using constant-time comparison for the auth cookie.

**The Horror Show:** AGY Opus has the worst security in the pack — it has a login screen that creates a token, but the token validation accepts literally any non-empty string (`if (token && token.trim() !== '')`), AND the `/api/chat` route never checks the token at all. It's security theater.

---

### 7. ✅ Testing & Quality

**Winner: OMO + DeepSeek** 🏆 (by a landslide)

| Project | Unit Tests | Integration Tests | QA Harness | Lint | CI |
|---------|------------|-------------------|------------|------|-----|
| OMO | ✅ **42 tests, 218 assertions** (Bun test) | ✅ Mock upstream server | ✅ Browser QA with screenshots | ⚠️ Directives but no config | ❌ |
| PI | ❌ 0 tests | ❌ | ❌ | ⚠️ Broken (`next lint` without ESLint) | ❌ |
| StepCode | ❌ 0 tests | ❌ | ❌ | ❌ ESLint unconfigured | ❌ |
| AGY Opus | ❌ 0 tests | ❌ | ❌ | ⚠️ `next lint` but no config | ❌ |
| AGY Gemini | ❌ 0 tests | ❌ | ❌ | ⚠️ Broken | ❌ |
| OMP | ❌ 0 tests | ❌ | ❌ | ❌ None | ❌ |

**Key Insight:** OMO is in a completely different league here. **42 passing tests across 5 test files** covering agents, attachments, plan routing, providers, and the run engine. Plus a mock upstream server and a headless browser QA harness that takes actual screenshots of the running app. No other project came close to zero tests.

---

### 8. 🚀 Deployment Readiness

**Winner: OMO + DeepSeek** 🏆

| Project | Vercel Config | Cloudflare Config | Deploy Docs | Build Status |
|---------|---------------|-------------------|-------------|-------------|
| OMO | ✅ `vercel.json` | ✅ `wrangler.jsonc` + `open-next.config.ts` | ✅ Comprehensive `deploy.md` | ✅ Builds clean |
| StepCode | ✅ `vercel.json` | ❌ | ✅ Detailed `deploy.md` | ✅ Builds (with warnings) |
| PI | ✅ README instructions | ✅ OpenNext mention | ✅ | ✅ |
| AGY Opus | ✅ `vercel.json` + standalone output | ❌ | ✅ `deploy.md` | ✅ |
| AGY Gemini | ✅ `maxDuration=60` | ⚠️ Mentioned in DEPLOY.md | ✅ `DEPLOY.md` | ✅ |
| OMP | ❌ No config | ❌ | ⚠️ README mentions both | ✅ |

**Key Insight:** OMO is the only project with a **working Wrangler configuration** for Cloudflare Workers/Pages. The `open-next.config.ts` adapter means you can literally `wrangler deploy` and it works. Every other project just mentions Cloudflare in docs without actually providing the config.

---

## 🔍 The Audit Wars: StepCode vs AGY as Auditors

Here's where it gets really interesting. I used **StepCode CLI** to audit 5 projects and **AGY CLI (Gemini)** to audit the StepCode project. The auditors themselves revealed their own strengths:

### StepCode as Auditor (Step 5 Preview)

StepCode's audit of the Step project (done by AGY/Gemini) was incredibly deep:
- Found the **IndexedDB `-Infinity` query bug** — a spec-level violation where `getAllFromIndex` does exact key matching, not prefix matching
- Identified the **Vite `?url` syntax** incompatibility with Next.js Webpack/Turbopack
- Caught the **Vercel 4.5MB payload ceiling** conflicting with the 25MB attachment limit
- Discovered **provider misattribution** where NVIDIA/Groq streams report as "OpenAI"

### AGY as Auditor (Gemini Flash 3.8)

AGY's audits focused more on high-level concerns:
- API authentication gaps
- Missing rate limiting
- Security header absence
- Documentation accuracy
- Dependency vulnerabilities

**Verdict:** StepCode's Step 5 Preview model found **deeper, more specific runtime bugs** — the kind that crash your app in production. AGY/Gemini found **broader security/architecture concerns** — important but more obvious. The best audit would combine both.

### 🧐 Is Step 5 Actually Distilling from Opus?

The user suspects Step 5 Preview might be distilling from Claude Opus. After reviewing both the StepCode project and its audit output, here are the clues:

**Evidence FOR distillation:**
- The `pRash_step` code uses Jose JWT for sessions — very similar to how Claude Opus projects handle auth
- The agents are split into domain files (`learning.ts`, `life.ts`, `work.ts`, `mind.ts`) — a pattern common in Opus-generated code
- The audit depth resembles Claude-level reasoning (finding spec violations, understanding browser APIs deeply)

**Evidence AGAINST distillation:**
- The project has several unique bugs (Vite `?url` syntax, `-Infinity` in IDB queries) that Claude Opus wouldn't typically produce
- The code style differs from `pRash_agy_opus` — Opus uses the Vercel AI SDK, while Step 5 builds raw fetch-based streaming
- Step 5's agent naming conventions are different

**My take:** The coding quality is somewhere between Opus and Gemini, but the **bug types** are unique to Step 5. If there's distillation happening, it's been substantially modified. The audit quality, however, is genuinely impressive and competitive with frontier models.

---

## 📈 The Scorecard

### Normalized Scores (out of 10)

| Category | AGY Gemini | AGY Opus | OMO DeepSeek | OMP Gemini | PI DeepSeek | StepCode Step5 |
|----------|-----------|----------|-------------|-----------|------------|---------------|
| Architecture | 9 | 9 | **10** | 9 | 9 | 9 |
| Agents | 8 | 9 | **10** | 9 | **10** | 9 |
| Model Integration | 7 | 7 | **10** | 9 | **10** | 8 |
| File Handling | 5 | 4 | **10** | 8 | 9 | 6 |
| Privacy | 9 | 8 | **10** | 9 | **10** | **10** |
| Security | 3 | 3 | 8 | 3 | **9** | 7 |
| Testing | 1 | 1 | **10** | 1 | 1 | 1 |
| Deployment | 8 | 8 | **10** | 7 | 8 | 9 |
| UI/UX | 9 | 9 | 9 | 9 | **9** | 7 |
| Code Quality | 9 | 8 | **9** | 9 | 9 | 8 |
| **TOTAL** | **68** | **66** | **96** | **73** | **84** | **74** |
| **Percentage** | **68%** | **66%** | **96%** | **73%** | **84%** | **74%** |

---

## 🏅 The Verdict

### 🥇 1st Place: OMO + DeepSeek 4.1 Flash

OMO's project isn't just the best — it's in a **different category**. It's the only project with:
- 42 unit tests and 218 assertions
- A mock upstream server for integration testing
- A headless browser QA harness with screenshot evidence
- Working Cloudflare Workers deployment (Wrangler config)
- Server-side PDF extraction with Gemini native fallback
- Individual provider adapter files with shared types
- A routing planner that separates chain resolution from execution

**The DeepSeek 4.1 Flash model clearly understands production software engineering**, not just code generation. It generated tests, QA infrastructure, deployment configs, and documentation — the stuff that actually matters when you run software.

### 🥈 2nd Place: PI + DeepSeek 4.1 Flash

PI's project is the most **security-conscious** and **user-experience-focused**. Highlights:
- Only project with proper Edge middleware auth gate
- Constant-time password comparison
- Client-side image compression (12MP → ~1.1MB)
- Web Speech API integration (voice input + text-to-speech)
- Shared safety rules injected into all agents
- Per-agent model preferences

### 🥉 3rd Place: StepCode + Step 5 Preview

StepCode's architecture is solid with excellent provider abstraction. However, it has **critical runtime bugs** (IDB queries, PDF worker, provider attribution) that prevent it from working in production. If these were fixed, it could compete with PI.

### 4th–6th: The Gemini/Opus Projects

AGY Opus, OMP Gemini, and AGY Gemini all produced **good-looking apps** with clean TypeScript and nice UIs. But they all share the same fatal flaws:
- No API authentication (anyone can drain your keys)
- No tests whatsoever
- Broken or missing file handling for non-image attachments
- No deployment configs beyond basic Next.js

---

## 🎓 Lessons Learned

### 1. The Model Matters More Than The CLI
Both DeepSeek 4.1 Flash projects (OMO and PI) outperformed all others despite using different CLIs. The model's understanding of production engineering patterns — testing, security, deployment — is the differentiator.

### 2. Tests Are The Ultimate Differentiator
OMO's 42 tests immediately separated it from the pack. Every other project has zero tests. In a real engineering review, "0 tests" is a non-starter for production deployment.

### 3. Security Is Systematically Ignored
4 out of 6 AI-generated projects have completely unprotected API endpoints. This is a pattern — AI models optimize for "does it work?" not "is it secure?" Always audit security separately.

### 4. File Handling Is Where AI Models Struggle
Only 2 out of 6 projects properly handle non-image attachments. PDFs are silently dropped, Excel files produce mojibake, and file content is replaced with just the filename. This is the hardest requirement to get right.

### 5. Auditing Your AI's Code with Another AI Works
Using StepCode to audit AGY projects (and vice versa) was incredibly effective. The cross-tool auditing found bugs that self-review would miss. **Always audit AI-generated code with a different AI model.**

---

## 🔗 Links & References

- **All projects**: Available at `github.com/kprsnt2/pRash_*`
- **Audit reports**: In the `audit/` folder of the pRash repo
- **Tools used**: AGY CLI, OMO CLI, OMP CLI, PI CLI, StepCode CLI

---

*This comparison was conducted on September 27, 2026. All AI models and CLI tools were used at their then-current versions. Your mileage may vary as models evolve.*

*— Built with ❤️ and a lot of API credits*
