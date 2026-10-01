# I Tested 6 AI Coding CLIs Twice — And Round 2 Broke Almost Everything
### *From "Nothing Was Great" to "Everything Became Worse": A forensic, real-world post-mortem on Fred Brooks’ Second-System Effect in autonomous AI engineering.*

---

### The Origin: Why I Started This Test

I did not start this experiment to write a benchmark paper. I started it because I was fed up with the artificial walls of ChatGPT Plus and Claude Pro.

Every developer knows the frustration: you have five complex PDF documents, two CSV datasets, and three architecture diagrams, and the web interfaces choke with attachment limits, truncate your context, or retain your proprietary prompts. 

So I set out to build a sovereign, all-in-one local chat platform tailored to my daily life:
- **4-tier automatic fallback routing:** OpenAI (`gpt-5.4-mini` / `gpt-5.4-nano`) → Google Gemini → NVIDIA NIM → Groq.
- **Strict zero-retention privacy mode:** Automatically lock the chat exclusively to paid Google Gemini (where enterprise data is never trained on) with zero disk retention.
- **Specialized agent personas:** `KidStory` (bedtime reading practice), `StudyBuddy` (first-principles explanations), `Worksheet` (printable exercises with answer keys), `DataAnalyst` (SQL, Tableau, Looker Studio), `Doctor` (analyzing lab reports and prescription attachments), `Psycho` (mental wellness), and `Spiritual` (life philosophy).

Instead of writing it by hand, I put six cutting-edge autonomous AI coding agent CLIs to the test on the exact same specification:
1. **`pRash_Pi`** (driven by DeepSeek 4.1 Flash)
2. **`pRash_Step`** (driven by Step 5 Preview)
3. **`Antigravity (agy) CLI`** (driven by Gemini Flash 3.8)
4. **`pRash_OMO`** (driven by DeepSeek 4.1 Flash)
5. **`pRash_OMP`** (driven by Gemini Flash 3.8)
6. **`Antigravity (agy) CLI + Opus`** (driven by Claude Opus 4.6)

What followed was a two-round rollercoaster that revealed the vast, uncomfortable gulf between **what AI code audits praise** and **what actually happens when a human sits down, types a message, and clicks print.**

---

## Part 1: Round 1 First Impressions — "Nothing Was Great"

When the six projects finished their initial builds, I opened each in my browser, authenticated, clicked every toggle, attached files, tested audio, and tried to print.

My immediate conclusion after Round 1 was simple: **Nothing was great. Every single project had its own distinct superpower, and every single project had a baffling, unforced failure.**

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                ROUND 1: FIRST-RUN VERDICT MATRIX                                │
├────────────────┬─────────────┬───────────────────────────────┬───────────────────────────────────┤
│ CLI Project    │ Initial View│ What Actually Worked (Pros)   │ Where It Failed (Cons)            │
├────────────────┼─────────────┼───────────────────────────────┼───────────────────────────────────┤
│ pRash_Pi       │ "Worst"     │ Voice input, TTS speech, auto │ All old legacy models listed;     │
│                │             │ routing, full chat print.     │ zero login/password protection.   │
├────────────────┼─────────────┼───────────────────────────────┼───────────────────────────────────┤
│ pRash_Step     │ "Mid/Okay"  │ Working JWT auth, chat export,│ Clunky, utilitarian UI layout;    │
│                │             │ requested models all working. │ zero aesthetic polish.            │
├────────────────┼─────────────┼───────────────────────────────┼───────────────────────────────────┤
│ Antigravity    │ "Good"      │ Flawless worksheet print out, │ Hardcoded old models, can't pick  │
│                │             │ clean full-width canvas.      │ models, alternate APIs broke.     │
├────────────────┼─────────────┼───────────────────────────────┼───────────────────────────────────┤
│ pRash_OMO      │ "Catastrophe│ Scored #1 on automated code   │ Couldn't even reply to "hi"; UI   │
│                │ (Audit Star)│ audit; 42 unit tests!         │ clunky, no model/agent selection. │
├────────────────┼─────────────┼───────────────────────────────┼───────────────────────────────────┤
│ pRash_OMP      │ "Ugly Duck" │ Grew on me; auto-routing work;│ API key setup error; leaked raw   │
│                │             │ copy works, speech works.     │ SSE chunks into message history.  │
├────────────────┼─────────────┼───────────────────────────────┼───────────────────────────────────┤
│ Agy Opus       │ "The Best?" │ Stunning night mode, instant  │ Light mode unreadable (contrast); │
│                │ (At start)  │ chat stream, updated models.  │ print dead; agent locked to chat. │
└────────────────┴─────────────┴───────────────────────────────┴───────────────────────────────────┘
```

### 1. `pRash_Pi`: The Voice King Trapped in 2023
- **My First Feeling:** *Worst.*
- **The Good:** Despite my initial disappointment, Pi did two things remarkably well: **Voice input and speech synthesis**. Clicking the microphone allowed natural browser dictation, and clicking "Read Aloud" played the assistant's reply cleanly. Auto-routing handled basic drops, and printing the entire chat worked without blowing up the layout.
- **The Bad:** It listed ancient legacy models, and it completely skipped security. Anyone who opened the URL had full access to execute prompts.

### 2. `pRash_Step`: The Boring Workhorse
- **My First Feeling:** *Not good, not bad.*
- **The Good:** Stepcode didn't care about flashy gradients, but it respected the contract. It had password-protected login gates, clean chat export to JSON, and—miracle of miracles—every model I asked for was present, correctly named, and functioning.
- **The Bad:** The UI was rough around the edges. Clunky padding, dated typography, and a stiff layout that felt like an internal enterprise admin panel from 2012.

### 3. `Antigravity (agy) CLI`: The Educational Worksheet Master
- **My First Feeling:** *Good, but severely boxed in.*
- **The Good:** The UI felt spacious and made great use of the full viewport width. But its true superpower was the **Worksheet generator**. When asked to create an educational quiz or math drill, it had a dedicated print feature that formatted the worksheet cleanly, hid extraneous chat bubbles, and produced a ready-to-print document.
- **The Bad:** It locked model selection down. You couldn't choose a specific model; alternate provider fallbacks failed silently; and it completely omitted login authentication.

### 4. `pRash_OMO`: The Code Audit Darling That Couldn't Say "Hi"
- **My First Feeling:** *A complete catastrophe.*
- **The Irony:** When we ran automated code analysis, linters, and repository audits, **OMO was ranked #1 across the board**. It had 42 comprehensive unit tests, mock server harnesses, pristine TypeScript types, modular file structures, and Cloudflare Wrangler configurations.
- **The Reality:** I booted the app, loaded the UI, typed:
  > *"Hi"*
  ...and received **absolutely nothing.** Complete silence. No spinner, no error banner, no token stream. An unhandled promise rejection in its route handler choked before the first chunk could be flushed. All those unit tests on disk couldn't save it from failing the simplest smoke test in human history.

### 5. `pRash_OMP`: The Ugly Duckling With the Raw SSE Leak
- **My First Feeling:** *Initial impression was ugly, thought it would be the worst—but after using it, my opinion completely flipped.*
- **The Good:** The interface grew on me quickly. The horizontal agent carousel felt responsive. Gemini failed due to an API key setup snag, but OMP's auto-fallback gracefully rescued the session and routed to ChatGPT without crashing. Copying code blocks was seamless, and voice input worked.
- **The Bizarre Bug:** Printing placed weird text artifacts across the page. And then, during an API key error, the streaming parser suffered a catastrophic buffer split. Instead of rendering markdown or a polite error banner, OMP dumped **this exact raw JSON Server-Sent Events chunk into the chat history**:

```json
{"id":"chatcmpl-ETVG6sumyv8LwjGBdEioS2OHQJSkv","object":"chat.completion.chunk","created":1790700378,"model":"gpt-5.4-mini-2026-03-17","service_tier":"default","system_fingerprint":null,"choices":[{"index":0,"delta":{"content":"At"},"finish_reason":null}],"obfuscation":""}
```

The client-side stream reader in `page.tsx` split a TCP packet, missed the `data:` prefix, branched into an unescaped text fallback, and permanently committed raw server telemetry into the conversation database!

### 6. `Antigravity (agy) CLI + Opus`: The Prom Queen With Invisible Day-Mode Text
- **My First Feeling:** *Looked great and seemed like the best build.*
- **The Good:** Night mode was gorgeous. Response times were instantaneous, all listed models were up to date, and provider switches worked smoothly.
- **The Flaws:** The moment I switched to Day (Light) Mode, typography contrast broke completely. Section headings and titles rendered white text on light-gray backgrounds, turning critical UI text invisible. Printing was broken. And worst of all, you could not change an agent mid-chat: if you started a session with `KidStory`, you were permanently locked into `KidStory` for that thread.

---

## Part 2: The Second Chance — The Grand Unification Prompt

Every project had a missing piece, but between the six of them, the perfect app already existed in fragments:
- **Antigravity (agy) CLI** had the worksheet printer.
- **Step** had authentication, export, and stable model plumbing.
- **Pi** had speech recognition and read-aloud voice output.
- **OMP** had automatic error-routing and dynamic prompts.
- **Antigravity (agy) CLI + Opus** had the refined night-mode visual presentation.

So, I gave every CLI another opportunity. I fed back my review notes and issued this unifying prompt to execute:

```text
Merge all features from these, then I want these features:
1. Password at login to open
2. Export chat, if needed - I can import this chat and resume the session
3. Print PDF formatted correctly with working which had answers, had a feature to hide answer sheet if required
4. Switch agent in the middle of the chat
5. Dark/light mode and chat should fill all the space and copy button for any code - show stats for chat like tokens, response time and etc
6. Update models to listed ones only, add an option to bypass to default model for each one using env variable
7. Speaking/voice output for chat will be good - couple of projects implemented this beautifully
8. Auto route to groq/nvidia or any free provider if any error happened and handle api errors and auto route to others and mention the model name and explanation at end of chat will be good
```

I wanted a single, unified build that combined every strength and eliminated every defect.

Instead, **almost all of them collapsed.**

---

## Part 3: Round 2 Review — "I Think All Became Worst Now"

The updated builds — with **`pRash_merged`** representing Stepcode's latest unified attempt — did not just fail to merge cleanly—they actively introduced severe regressions into features that had worked in Round 1.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             ROUND 2: THE REGRESSION AUTOPSY                                      │
├────────────────┬─────────────┬───────────────────────────────────────────────────────────────────┤
│ CLI Project    │ R2 Verdict  │ The Exact Forensic Breakage                                       │
├────────────────┼─────────────┼───────────────────────────────────────────────────────────────────┤
│ pRash_OMP      │ Regressed   │ Model IDs still incorrect; API key setup error persists; light    │
│                │             │ mode print renders white-on-white text (invisible ink!).          │
├────────────────┼─────────────┼───────────────────────────────────────────────────────────────────┤
│ pRash_OMO      │ Mixed / Slow│ Model list accurate, but Gemini API key not found; print spawns 3 │
│                │             │ phantom blank pages; NVIDIA fallback is unbearably slow.          │
├────────────────┼─────────────┼───────────────────────────────────────────────────────────────────┤
│ pRash_Step     │ Very Bad    │ Harvested 33 agents, but OpenAI dead (404s); switching agent      │
│ (pRash_merged) │ (Bricked)   │ mid-chat returns blank reply and permanently freezes Stop button! │
├────────────────┼─────────────┼───────────────────────────────────────────────────────────────────┤
│ pRash_Pi       │ Broken      │ Cloned OMP's shell; can't chat; no login; print dumps raw screen  │
│                │             │ instead of dedicated worksheet.                                   │
├────────────────┼─────────────┼───────────────────────────────────────────────────────────────────┤
│ Antigravity    │ Degraded    │ All models broken except ChatGPT; Gemini dead; worksheet print    │
│                │             │ superpowers lost (prints full raw chat).                          │
├────────────────┼─────────────┼───────────────────────────────────────────────────────────────────┤
│ Agy Opus       │ Mediocre    │ Unconstrained print layouts blow out horizontally; hallucinated   │
│                │             │ invalid NVIDIA & Groq model strings.                              │
└────────────────┴─────────────┴───────────────────────────────────────────────────────────────────┘
```

### 1. `pRash_OMP`: The "Invisible Ink" Print Disaster
In Round 1, OMP was a capable workhorse despite its streaming hiccup. In Round 2:
- Model listings were still incorrect.
- The initialization API key setup error was still rearing its head.
- **The Print Catastrophe:** When I clicked print in light mode, the paper was entirely blank. Why? The agent injected Tailwind CSS variables into the root layout, but in the print stylesheet (`@media print`), it set `background: #ffffff !important` without overriding the text color variables. The text rendered in `#ffffff` on white paper. It literally printed **invisible ink**.

### 2. `pRash_OMO`: The 3 Phantom Pages Bug
OMO finally managed to boot and populate its model picker cleanly. But under real usage:
- It threw `GEMINI_API_KEY not found` because it looked exclusively for `GOOGLE_AI_API_KEY` without checking standard fallback aliases.
- The NVIDIA model was unbearably slow, stalling for nearly a minute before first token output.
- **The Print Bug:** In the print preview modal, everything looked acceptable. But when I actually printed to physical paper or PDF, **three completely blank, empty phantom pages** suddenly appeared at the end. An unconstrained Flexbox container with `min-height: 100vh` was overflowing the browser's paginated layout engine.

### 3. `pRash_Step` (`pRash_merged`): The Complete Architecture Deadlock
Stepcode attempted the most ambitious merge: it created `scripts/harvest-agents.ts` and successfully consolidated **all 33 agent personas** across every single repository into one structured registry.

On paper, this looked like the ultimate winner. In practice:
- **OpenAI was completely broken:** It hardcoded speculative model IDs like `gpt-5.4-mini` into its primary configuration without graceful fallbacks. When sent to the live OpenAI endpoint, the API returned 404 Model Not Found. Only Gemini worked.
- **The Mid-Chat Agent Switch Deadlock:** This was the most catastrophic bug in the entire shootout. When I tried to switch agents midway through an ongoing chat:
  1. The assistant rendered an empty, blank response bubble.
  2. The **Stop** button lit up and became permanently frozen.
  3. Clicking "Stop" did nothing because the `AbortController` reference was bound to the previous agent session, while the UI stream listener was awaiting an event on the new session that never fired. The entire application was locked in an unrecoverable pending state until localStorage was wiped.

### 4. `pRash_Pi`: The Paralyzed Clone
Pi looked like it attempted to copy OMP's frontend components wholesale.
- Login was still missing.
- Model IDs were scrambled.
- **Chat was completely dead:** Typing a message and pressing Enter failed to dispatch the POST request.
- The dedicated worksheet print button was replaced with a generic `window.print()` call that dumped raw navigation sidebars, buttons, and input boxes onto the paper.

### 5. `Antigravity (agy) CLI`: Superpowers Destroyed
In Round 1, Antigravity (agy) CLI had the cleanest educational worksheet printer of any tool.
- In Round 2, while trying to integrate multi-provider fallbacks, its routing logic broke down. Every model failed except standard ChatGPT; Gemini was dead.
- Worse still: **its worksheet printer stopped isolating worksheets**. It reverted to dumping the entire raw chat feed onto the page. The one feature it did better than everyone else was destroyed.

### 6. `Antigravity (agy) CLI + Opus`: Wide-Screen Layout Blowout
Opus maintained basic conversational viability, but stumbled hard on the edge cases:
- It hallucinated NVIDIA and Groq model identifier strings that returned immediate 404s on the provider gateways.
- Its print stylesheet suffered from an unconstrained horizontal flex bug—printing generated an ultra-wide document where half the text was clipped off the right margin of standard A4 paper.

---

## Part 4: Was Round 2 Actually Worse? Yes — 100%.

This wasn't imagination, and it wasn't overly critical testing. **The applications objectively deteriorated.**

As a software engineer, watching this unfold is fascinating because it proves a fundamental limitation in how autonomous AI coding agents currently operate. Here is the forensic engineering breakdown of why your second prompt caused working code to collapse:

### 1. The Second-System Effect in Autonomous AI
In 1975, Fred Brooks wrote *The Mythical Man-Month*, describing the **Second-System Effect**: when an engineering team succeeds with a small, focused first prototype, they attempt to pack every single deferred feature, edge case, and architectural flourish into the second version—causing it to collapse under its own complexity.

In Round 1, each CLI had a narrow, manageable scope:
- Antigravity (agy) CLI focused on the worksheet layout.
- Step focused on auth and basic API routing.
- Pi focused on voice synthesis.
- OMP focused on dynamic carousel prompts.

In Round 2, you asked them to build:
> **Auth** + **Import/Export** + **Mid-Chat Agent Swapping** + **Print Isolation** + **Answer Masking** + **Latency Telemetry** + **Voice Synthesis** + **4-Tier Cascading Fallbacks**

For a human engineering team, that is a **6-week sprint across multiple epics**. When an autonomous AI CLI tries to execute that in a single generation pass, it hits architectural overload. It tries to stitch together incompatible React patterns, resulting in half-baked code that breaks existing functionality.

### 2. State Machine Explosion (The Mid-Chat Freeze)
In Round 1, chat state was linear:
```text
ChatSession = { agentId, model, messages[] }
```

When you requested *switch agent in the middle of a chat*, that state machine became non-linear:
- Does message **N** belong to Agent A, while message **N+1** belongs to Agent B?
- Does the system prompt dynamically swap at turn **N**?
- What happens to the streaming `AbortController` if the user swaps personas while tokens are actively streaming?

In `pRash_merged` (Stepcode's latest), the agent updated `settings.agentId` without updating the active conversation schema. When the user sent a prompt, the backend expected the initial agent contract, threw an exception, and returned an empty response. Because the UI's stream reader was awaiting a `done` event that never arrived, **the `streaming` boolean stayed `true` forever**, freezing the Stop button and locking the user interface.

### 3. The `@media print` Isolation Nightmare
Writing reliable print CSS inside modern Tailwind / React component trees is notoriously difficult for LLMs:
- **OMP's White-on-White Text:** OMP uses dark-mode CSS variables (`--foreground: #f1f5f9; background: #0b0f17;`). In Round 2, it forced the print background to white (`background: #ffffff !important;`), but forgot to override the text colors of nested Tailwind classes (`text-slate-100`, `text-white`). The paper turned white, the text remained white, and the result was invisible ink.
- **OMO's 3 Empty Pages:** OMO wrapped its chat viewport in a `min-h-screen flex flex-col` container. Browsers attempting to calculate pagination splits across Flex containers with height constraints automatically insert page-break triggers, generating three ghost pages of blank paper.

### 4. The Illusion of Automated Code Audits vs. Human Reality
Round 1 and Round 2 proved that **code audits can be completely blind to runtime reality**:
- `pRash_omo` scored the highest on automated audits because it had 42 unit tests, mock servers, and clean folder structures. But it couldn't even reply *"Hi"* because runtime execution depends on environment variable resolution, network timeout handling, and DOM event bindings that linters don't test.
- `pRash_step` cleanly harvested 33 agent personas via a custom script, but hallucinated OpenAI model strings and deadlocked on mid-chat persona swaps.

When Round 2 arrived, the agents generated more boilerplate to satisfy your prompt checklist, but degraded the actual runtime plumbing.

---

## 📊 Complete Feature & Bug Comparison Matrix

```
┌─────────────────────────┬───────────────────────────────┬───────────────────────────────┐
│ Feature / Capability    │ Round 1 Status                │ Round 2 Status                │
├─────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ Login & Authentication  │ Only Step had clean JWT auth; │ Partial auth added; Pi still  │
│                         │ others were wide open.        │ lacked password protection.   │
├─────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ Mid-Chat Agent Switch   │ Not supported; chat locked    │ Step added it and deadlocked; │
│                         │ to 1 agent per session.       │ Stop button permanently froze.│
├─────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ PDF / Worksheet Print   │ Antigravity printed sheets;   │ Complete chaos: OMP printed   │
│                         │ OMP had weird text offset.    │ white-on-white; OMO printed   │
│                         │                               │ 3 phantom empty pages.        │
├─────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ Model Fallback Cascade  │ OMP auto-routed on failure;   │ Speculative models failed;    │
│                         │ others failed with raw 500s.  │ Gemini keys missed; NVIDIA    │
│                         │                               │ timeouts.                     │
├─────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ SSE Streaming Parser    │ OMP leaked raw JSON chunk:    │ Stream parsers broke on error;│
│                         │ {"id":"chatcmpl-ETVG6..."}    │ empty reply bubbles and       │
│                         │ directly into message list.   │ unhandled promise rejections. │
├─────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ Persona Variety         │ 14 to 22 agents per app;      │ Step merged all 33 agents,    │
│                         │ scattered across projects.    │ but broke the chat pipeline.  │
└─────────────────────────┴───────────────────────────────┴───────────────────────────────┘
```

---

## 💡 The Big Engineering Takeaway

Autonomous AI coding CLIs are incredible at **0-to-1 greenfield scaffold generation**. If you ask an agent to build an app from a clean slate, it will generate an impressive prototype in minutes.

However, they are still deeply fragile at **1-to-N monolithic refactoring and cross-feature consolidation**. The moment you ask an agent to *"merge everything from these 5 other apps and add 8 advanced stateful features,"* it starts cutting corners, breaking existing CSS rules, hallucinating model IDs, and dropping stream-handling safeguards.

Until agent harnesses implement deep multi-file integration tests and headless browser visual regression checks before delivering code, the "Second-System Collapse" will remain the biggest trap in AI-assisted development.
