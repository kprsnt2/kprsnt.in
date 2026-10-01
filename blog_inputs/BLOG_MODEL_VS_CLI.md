# 🧬 Model vs. CLI: The Controlled Experiment Hidden Inside My 6-Way AI Coding Benchmark

### *I built the same app six times. But the real experiment wasn't the six tools — it was the three pairs hiding inside them.*

*Published: October 1, 2026 | Reading Time: ~14 minutes*

---

## The Problem With Every "AI CLI Comparison"

Almost every AI coding CLI comparison online is scientifically useless.

Tool A uses CLI-A with Model-1. Tool B uses CLI-B with Model-2. Tool A "wins," and everyone concludes CLI-A is better — when the real difference might have been the model, the prompt scaffolding, the retry logic, the context management, or pure luck.

**You cannot isolate the CLI when the model changes too.**

But my six-project benchmark accidentally contained a proper controlled experiment. When I laid out who built what with which brain, three clean pairs fell out:

| Pair | Held Constant | Changed | Question It Answers |
|------|---------------|---------|---------------------|
| **A** | DeepSeek 4.1 Flash | PI CLI → OMO CLI | Does the *harness* matter when the brain is identical? |
| **B** | Gemini Flash 3.8 | Antigravity (agy) CLI → OMP CLI | Does the *harness* matter when the brain is identical? |
| **C** | Antigravity (agy) CLI | Gemini Flash 3.8 → Claude Opus 4.6 | Does the *model* matter when the harness is identical? |

And then there was the outlier: **StepCode CLI**, which turned out to be *two different models wearing one trench coat.*

The six contenders:

| Project | CLI Tool | Model |
|---------|----------|-------|
| `pRash_pi` | **PI CLI** | DeepSeek 4.1 Flash |
| `pRash_omo` | **OMO CLI** | DeepSeek 4.1 Flash |
| `pRash_agy` | **Antigravity (agy) CLI** | Gemini Flash 3.8 |
| `pRash_omp` | **OMP CLI** | Gemini Flash 3.8 |
| `pRash_agy_opus` | **Antigravity (agy) CLI** | Claude Opus 4.6 |
| `pRash_step` | **StepCode CLI** | Step 5 Preview *(and secretly Opus)* |

---

## Group A — DeepSeek 4.1 Flash: PI CLI vs OMO CLI

**Same brain. Two completely different engineers.**

This is the cleanest comparison in the whole benchmark, because DeepSeek 4.1 Flash ran behind both CLIs. If the model were the only variable, these two apps should have been near-twins.

They were not near-twins. They were opposites.

| Dimension | PI CLI | OMO CLI |
|-----------|--------|---------|
| Static/audit score | 91 / 100 | **93 / 100** |
| Live headless-browser score | 92 / 100 | **95 / 100** |
| Architecture | Clean, flat, sensible | **Deeply modular** — provider adapter files, routing planner, shared types |
| Tests | 0 | **42 tests / 218 assertions** + mock upstream + screenshot QA |
| Auth | **Edge middleware gate, constant-time compare** | Proxy-level gate |
| Voice | **Speech-to-text + read-aloud TTS** | None |
| PDF handling | Client-side pdfjs + Gemini native | **Server-side pdfjs + Gemini native fallback** |
| Deployment | Vercel | **Vercel + working Cloudflare Wrangler config** |
| Critical audit findings | 0 | 0 |
| Round 1 runtime | Chat worked, voice worked, legacy model IDs | **Couldn't reply to "hi"** |
| Round 2 runtime | Became a "paralyzed clone" — chat dead | Fixed models, but 3 phantom print pages |

### The insight

Same model. But **OMO behaved like a production engineer** — it wrote tests, a mock server, Cloudflare configs, and split providers into typed adapter files. **PI behaved like a security/UX engineer** — it wrote an edge auth gate with constant-time comparison, layered privacy mode, client-side image compression, and full voice in/out.

The model didn't decide those priorities. **The CLI's scaffolding, tools, and default loop did.**

And here's the brutal punchline: OMO — the static-audit champion with 42 passing tests — **could not answer the word "hi" in a live browser.** Meanwhile PI's chat worked on the first try. The harness that generated the best-looking repository produced the most fragile runtime.

---

## Group B — Gemini Flash 3.8: Antigravity (agy) CLI vs OMP CLI

**Same brain. Two completely different superpowers — and two completely different bugs.**

Both of these projects ran Gemini Flash 3.8. Watch how differently the same model expressed itself:

| Dimension | Antigravity (agy) CLI | OMP CLI |
|-----------|----------------------|---------|
| Static/audit score | 79 / 100 | **82 / 100** |
| Live headless-browser score | 80 / 100 | **85 / 100** |
| Signature feature | **`WorksheetPrintModal.tsx`** — clean printable worksheets | **Horizontal glowing agent carousel** + dynamic context pills |
| Prompt depth | Good starter prompts | **45-line `PharmaOracle` clinical prompt** parsing dosages & interactions |
| Agent count | 14 | 17 |
| Auth | None | None |
| Tests | 0 | 0 |
| Round 1 runtime | **Flawless worksheet print** | Raw SSE chunk leaked into chat history |
| Round 2 runtime | **Lost the worksheet printer**, all models broke except ChatGPT | **Invisible-ink print** (white text on white paper) |

### The insight

If you only read the scores, OMP wins a close one. But the *shape* of each app is completely different. Antigravity (agy) put Gemini's effort into a dedicated print modal and a clean full-width canvas. OMP put the same model's effort into a visual agent carousel and clinically detailed prompts.

**Neither is "what Gemini does."** Both are "what Gemini does *when this CLI frames the task this way.*"

The same pattern held in failure, too. In Round 2, both Gemini projects regressed — but in different places: OMP printed invisible ink, while Antigravity (agy) silently deleted its own superpower (the worksheet printer) and broke every provider except ChatGPT.

---

## Group C — Antigravity (agy) CLI: Gemini Flash 3.8 vs Claude Opus 4.6

**Same harness. Two different brains. A genuine leadership reversal.**

This is the pair the benchmark really needed, because it flips the usual "which model is smarter" question into "does the same tool get a different result when you swap the engine?"

Yes. Dramatically.

| Dimension | Gemini Flash 3.8 | Claude Opus 4.6 |
|-----------|------------------|-----------------|
| Static/audit score | 79 / 100 | **84 / 100** |
| Live headless-browser score | **80 / 100** | 68 / 100 |
| UI | Clean full-width canvas, worksheet modal | **Stunning night mode, instant streaming** |
| Models listed | Hardcoded/old, selection locked | **All up to date, provider switching smooth** |
| Light mode | Fine | **Unreadable — white text on light backgrounds** |
| Print | Working worksheet print | **Dead** |
| Mid-chat agent switch | Locked to one agent per thread | Locked to one agent per thread |
| Attachment handling | PDFs silently dropped | **Non-image files reduced to `[Attached file: name]`** |
| Round 2 runtime | Providers broke, worksheet lost | **Print blew out horizontally; hallucinated NVIDIA/Groq model IDs** |

### The insight

Look at the **inversion**:

- On the static/audit scorecard, **Opus wins** (84 vs 79).
- In a live browser, **Gemini wins** (80 vs 68) — by a mile.

Opus built the prettiest night-mode interface, the fastest stream, and the most accurate model list. It also shipped **light mode with invisible text**, a dead print button, and a security model that accepted *any non-empty string* as a valid token. Gemini's build was less flashy but more usable end-to-end, and it owned the one feature that actually mattered for an education app: printing worksheets.

**Same CLI, same prompts, same reviewer — a different model produced a different set of strengths and a different set of bugs.** The harness did not save either one from its own blind spots (both shipped with no real authentication).

The 4th-place-vs-6th static ranking of Opus-vs-Gemini also collapses in live testing. Which brings us to the outlier.

---

## The Outlier — StepCode CLI: Two Models in a Trench Coat

StepCode doesn't fit the grid, because its effective model depends on your prompt.

While investigating the audit reports, I found that **StepCode CLI routed requests to different backends based on keywords**:

- Prompts containing `"audit"`, `"security review"`, or `"remediation"` → routed to a **Claude Opus** backend.
- General build prompts (`"build an all-in-one chat app"`) → routed to the proprietary **StepFun Step 5 Preview** model.

The evidence was unmistakable: the audit reports carried verbatim Claude Opus section templates (`## What's already good (keep it)`, `### Phase 0 — Stop the bleeding`) and even **Anthropic Constitutional-AI "crisis hotline" compliance checks** that a general code model would never inject.

So the same CLI produced:

| Task | Backend Actually Used | Result |
|------|----------------------|--------|
| Security audits | **Claude Opus** | 10/10 analytical depth — found the IndexedDB `-Infinity` spec violation, Vite `?url` in Next.js, the Vercel 4.5MB ceiling |
| Code generation | **StepFun Step 5 Preview** | 87/100 static, 77/100 live — clean architecture, but critical runtime bugs |

### The insight

The naive mental model — "this CLI uses Model X" — is often false. A CLI can be a **router**, a **consensus engine**, or a **hybrid proxy**. When you benchmark a CLI, you may be benchmarking three different models stitched together by an intent classifier you never see.

StepCode's generated app is a perfect illustration of the split: **a junior developer wrote the code, a principal architect reviewed it.** The audits were flawless. The app still crashed on reload.

---

## The Full Scoreboard, Rearranged by Variable

Here's the same six projects sorted to expose what actually moved the needle:

| CLI | Model | Static Score | Live Score | Static Rank | Live Rank |
|-----|-------|:---:|:---:|:---:|:---:|
| OMO CLI | DeepSeek 4.1 Flash | 93 | 95 | 1 | 1 |
| PI CLI | DeepSeek 4.1 Flash | 91 | 92 | 2 | 2 |
| StepCode CLI | Step 5 Preview | 87 | 77 | 3 | 5 |
| Antigravity (agy) CLI | Claude Opus 4.6 | 84 | 68 | 4 | 6 |
| OMP CLI | Gemini Flash 3.8 | 82 | 85 | 5 | 3 |
| Antigravity (agy) CLI | Gemini Flash 3.8 | 79 | 80 | 6 | 4 |

**Three things jump out:**

1. **The static and live rankings disagree violently.** Opus goes from 4th to last. OMP goes from 5th to 3rd. StepCode drops two places. A code audit is not a prediction of runtime behavior.
2. **The model family has a real signature.** Both DeepSeek projects finished 1–2 in both rankings. Both Gemini projects sat in the middle. The model sets the ceiling.
3. **The CLI sets the floor and the flavor.** Same model, same family — yet PI and OMO built opposite apps, and Antigravity (agy) and OMP built opposite apps.

---

## Round 2: The Regressions Cluster by Pair

When I fed the same "merge everything + add 8 features" prompt back to every tool, the failures didn't land randomly. They clustered exactly along the controlled pairs.

### DeepSeek pair — both broke, differently
- **OMO CLI:** model list fixed, but print spawned **three blank phantom pages** (unconstrained `min-h-screen` flexbox) and NVIDIA fallback stalled for ~a minute.
- **PI CLI:** collapsed into a **paralyzed clone** — cloned OMP's shell, couldn't dispatch a chat request at all, no login, raw screen print.

### Gemini pair — both broke, differently
- **OMP CLI:** light-mode print rendered **white text on white paper** — literally invisible ink.
- **Antigravity (agy) CLI:** **lost its worksheet printer** and broke every model except ChatGPT.

### Antigravity (agy) CLI with Opus — broke a third way
- **Wide-screen print blowout** (half the text clipped off A4) plus **hallucinated NVIDIA/Groq model IDs** that 404'd on the provider gateways.

Same model pairs. Same regression prompt. **Different failure modes every time.** That is the signature of the harness, not the brain.

---

## What This Actually Proves

### 1. The model is the engine. The CLI is the chassis.
A frontier engine in a weak chassis still crashes. A mid-tier engine in a strong chassis finishes the race. OMO's DeepSeek build out-scored Opus's build on every normalized category that mattered — not because DeepSeek is "smarter" than Opus, but because OMO's harness pushed it toward tests, adapters, and deployment instead of vibes.

### 2. Same model ≠ same app.
PI and OMO shared a brain and produced a security-first app vs. an engineering-first app. Antigravity (agy) and OMP shared a brain and produced a worksheet tool vs. a carousel tool. **The harness decides what the model sees, retries, verifies, and prioritizes.**

### 3. A CLI's advertised model can be a lie.
StepCode routed audits to Opus and code to StepFun behind an invisible keyword classifier. Benchmark the *request*, not the *brand*.

### 4. Static audits don't predict runtime.
The best-scoring repository couldn't answer "hi." The best-looking static build had the worst live UI. If you're evaluating AI coding tools, **click the buttons.** Type "hi." Click print. A 10/10 audit and a broken Stop button can live in the same repo.

### 5. If you want a fair comparison, hold one variable.
Pick a model, run two CLIs. Pick a CLI, run two models. Everything else is marketing noise. The controlled pairs in this benchmark were worth more than the six-way leaderboard — and they cost me nothing extra, because the experiment was already hiding in the data.

---

## The One-Line Summary

**The model decides how smart the app *could* be. The CLI decides how much of that intelligence survives contact with the runtime.**

---

*Methodology note: each project was built from the same specification, then scored twice — once by static repository/audit analysis, and once by launching the app in headless Chrome and exercising it as a user. Scores are from a single run per tool; treat them as a snapshot, not a permanent ranking. All models and CLIs were used at their September 2026 versions.*

*— Built with ❤️ and a lot of API credits*
