# 🖥️ Live UI & Runtime Battle Royale: Launching All 6 AI-Generated Chat Apps with Headless Chrome

> **Test Date:** September 27, 2026  
> **Environment:** Windows 11 · Node.js v20+ · Bun v1.4.2 · Google Chrome Headless (`--headless=new`)  
> **Ports Tested:** 3011 (`pRash_agy`), 3012 (`pRash_agy_opus`), 3013 (`pRash_omo`), 3014 (`pRash_omp`), 3015 (`pRash_pi`), 3016 (`pRash_step`)  
> **Captures Generated:** 12 screenshots (Desktop 1440×900 + Mobile 390×844) stored in [`ui_comparison_results/`](file:///C:/Users/hplap/Desktop/pRash/ui_comparison_results)

---

## 🏆 At A Glance: Runtime & UI Scoreboard

| Rank | Project & Model | Startup Command | Visual UI/UX | Agent System | File Upload UI | Unique Superpower | Overall Rating |
|:---:|:---|:---|:---:|:---:|:---:|:---|:---:|
| 🥇 | **`pRash_omo`**<br>*(DeepSeek 4.1 Flash)* | `bun run next start -p 3013` | **9.6 / 10** | **9.8 / 10** | **9.7 / 10** | 42 unit tests, mock server, server-side PDF extraction, Cloudflare Wrangler ready | **95 / 100** |
| 🥈 | **`pRash_pi`**<br>*(DeepSeek 4.1 Flash)* | `node next start -p 3015` | **9.4 / 10** | **9.6 / 10** | **9.2 / 10** | **Voice input (Microphone dictation) + Text-to-Speech (Read aloud)**, client image resizing | **92 / 100** |
| 🥉 | **`pRash_omp`**<br>*(Gemini Flash 3.8)* | `bun run next start -p 3014` | **9.1 / 10** | **9.3 / 10** | **8.8 / 10** | **Horizontal Agent Carousel**, dynamic prompt pills, Doctor Rx lab values prompt | **85 / 100** |
| 4th | **`pRash_agy`**<br>*(Gemini Flash 3.8)* | `node next start -p 3011` | **8.8 / 10** | **8.6 / 10** | **8.0 / 10** | Dedicated **Worksheet Print Modal** (`WorksheetPrintModal.tsx`), live cascade badge | **80 / 100** |
| 5th | **`pRash_step`**<br>*(Step 5 Preview)* | `node next start -p 3016` | **8.2 / 10** | **8.5 / 10** | **7.5 / 10** | Satellite auth gate, domain-separated agent files (`learning/life/work/mind`) | **77 / 100** |
| 6th | **`pRash_agy_opus`**<br>*(Claude Opus 4.6)* | `node .next/standalone/server.js` | **6.5 / 10** | **8.0 / 10** | **5.5 / 10** | Self-contained standalone server (fixed missing `.next/static`), Vercel AI SDK | **68 / 100** |

---

## 📸 Visual Gallery & Headless Browser Evidence

Each server was launched in isolation and inspected with headless Google Chrome at **Desktop (1440×900)** and **Mobile (390×844)** viewports.

### 1. `pRash_omo` (OneChat) — The Complete Production Package
- **Desktop:** [`pRash_omo_desktop.png`](file:///C:/Users/hplap/Desktop/pRash/ui_comparison_results/pRash_omo_desktop.png)
- **Agent Picker:** [`02-agent-picker-open.png`](file:///C:/Users/hplap/Desktop/pRash/pRash_omo/qa/evidence/02-agent-picker-open.png)
- **Streamed Chat with 3 Attachments:** [`04-streamed-reply.png`](file:///C:/Users/hplap/Desktop/pRash/pRash_omo/qa/evidence/04-streamed-reply.png)
- **What the UI looks like:** Minimalist dark cyan aesthetic. Clear header with Sparkle Agent dropdown, Auto-fallback badge, and Privacy Mode toggle. The composer features a `+` attachment button and multi-format preview pills.
- **Evidence of Streamed Execution:** In `04-streamed-reply.png`, a user prompt with a PNG, a PDF (`blood-report.pdf`), and a Markdown file (`notes.md`) streams back with metadata badge `OpenAI · gpt-5.4-mini (2 rung(s) skipped)`!

### 2. `pRash_pi` (pRash AI) — The Feature King (Speech + Voice)
- **Desktop:** [`pRash_pi_unlocked_desktop.png`](file:///C:/Users/hplap/Desktop/pRash/ui_comparison_results/pRash_pi_unlocked_desktop.png)
- **Mobile:** [`pRash_pi_mobile.png`](file:///C:/Users/hplap/Desktop/pRash/ui_comparison_results/pRash_pi_mobile.png)
- **What the UI looks like:** Sleek dark indigo theme. Left sidebar has quick agent icon dock (Moon, Notes, Android, Bar Chart, Stethoscope, Brain, +11).
- **Unique Features in UI:**
  - 🎙️ **Microphone Button:** In the composer bar, clicking the mic activates the Web Speech Recognition API for seamless voice prompting!
  - 🔊 **Read Aloud Button:** Top right has a speaker icon (`Read`) that triggers browser Text-to-Speech synthesis for any assistant reply!
  - 🖨️ **Print Button:** One-click clean print view.

### 3. `pRash_omp` (OmniChat) — The Most Visual & Polished Agent Experience
- **Desktop:** [`pRash_omp_desktop.png`](file:///C:/Users/hplap/Desktop/pRash/ui_comparison_results/pRash_omp_desktop.png)
- **Mobile:** [`pRash_omp_mobile.png`](file:///C:/Users/hplap/Desktop/pRash/ui_comparison_results/pRash_omp_mobile.png)
- **What the UI looks like:** Beautiful horizontal scrolling agent carousel with dedicated glowing badges: `SlumberScribe 🌙`, `SynapseSpark 🧠`, `PrintMatrix 🖨️`, `FormulaViking 📊`, `PharmaOracle ⚕️`.
- **Dynamic Context:** When an agent is picked, the hero section displays tailored starter pills, and the composer placeholder dynamically updates (e.g. for SlumberScribe: *"Tell me child's name, age, favorite theme, or bedtime lesson..."*).

### 4. `pRash_agy` (pRash Hub) — Solid Grid & Worksheet Specialist
- **Desktop:** [`pRash_agy_desktop.png`](file:///C:/Users/hplap/Desktop/pRash/ui_comparison_results/pRash_agy_desktop.png)
- **Mobile:** [`pRash_agy_mobile.png`](file:///C:/Users/hplap/Desktop/pRash/ui_comparison_results/pRash_agy_mobile.png)
- **What the UI looks like:** Classic ChatGPT-style sidebar + hero card. Features an "Explore Other Built-In Agents" pill grid (SlumberSpun, FeynmanForge, PrintNova, MetricMancer, RxSleuth, CogniCalm, ZenQuasar, FridgePhantom, GhostDiplomat, ClauseCracker, PennyPulse, SyntaxSorcerer, IronMorph, RoamRover).
- **Specialist Modal:** Features `WorksheetPrintModal.tsx` specifically built for printing generated educational worksheets.

### 5. `pRash_step` (AllChat) — The Security & Domain Purist
- **Login Gate:** [`pRash_step_desktop.png`](file:///C:/Users/hplap/Desktop/pRash/ui_comparison_results/pRash_step_desktop.png)
- **Main Chat:** [`pRash_step_unlocked_desktop.png`](file:///C:/Users/hplap/Desktop/pRash/ui_comparison_results/pRash_step_unlocked_desktop.png)
- **What the UI looks like:** High-contrast dark navy UI. Centered satellite modal for password gating. Once unlocked with `APP_PASSWORD`, reveals a clean chat canvas with Orbit, ByteWise, Quill, QuizForge. Bottom buttons include "Export backup", "Import backup", and "Lock app".

### 6. `pRash_agy_opus` (pRash Hub Opus) — Caught Live With Styling & Standalone Bugs
- **Login Styled:** [`pRash_agy_opus_login_styled.png`](file:///C:/Users/hplap/Desktop/pRash/ui_comparison_results/pRash_agy_opus_login_styled.png)
- **Main Chat:** [`pRash_agy_opus_desktop.png`](file:///C:/Users/hplap/Desktop/pRash/ui_comparison_results/pRash_agy_opus_desktop.png)
- **The Bug Caught on Camera:**
  1. *Standalone Asset Bug:* `.next/standalone/server.js` was missing `.next/static`, serving raw unstyled HTML until we copied `.next/static` into the standalone directory.
  2. *CSS Theme Mismatch:* Even when styled, the sidebar renders white text on a white/light gray background because of dark/light class confusion (`dark:` prefix mismatch on container vs background).

---

## 🤖 Deep Dive: The Agent Systems Compared

The prompt required crazy/fancy names for specialized everyday agents. Here is how each tool named and structured their personas:

| Category / Requirement | `pRash_omo` | `pRash_pi` | `pRash_omp` | `pRash_agy` | `pRash_step` | `pRash_agy_opus` |
|:---|:---|:---|:---|:---|:---|:---|
| **Bedtime Kid Story** | `LullaQuill` | `SlumberSpun` | `SlumberScribe` | `SlumberSpun` | `SlumberStory` | `DreamWeaver` |
| **Study Buddy / Tutor** | `SimpleSage` | `FeynmanForge` | `SynapseSpark` | `FeynmanForge` | `LearnMate` | `StudyBuddy` |
| **Worksheet Generator** | `PaperMint` | `PrintNova` | `PrintMatrix` | `PrintNova` | `QuizForge` | `WorksheetWizard` |
| **Data & BI Analyst** | `MetricAlchemist` | `MetricMancer` | `FormulaViking` | `MetricMancer` | `ByteWise` | `DataDoctor` |
| **Medical / Prescription** | `PulseLens` | `RxSleuth` | `PharmaOracle` | `RxSleuth` | `MedPulse` | `DrAnalyze` |
| **Psychology / Mind** | `MindMender` | `CogniCalm` | `ZenSovereign` | `CogniCalm` | `SoulEcho` | `PsychoCare` |
| **Spiritual / Life Qs** | `KarmaCompass` | `ZenQuasar` | `AetherGuide` | `ZenQuasar` | `Zenith` | `SoulSearcher` |
| **Total Personas** | **21** | **18** | **17** | **14** | **17** | **22** |

### 🧠 Prompt Engineering Quality Breakdown

1. **`pRash_omp` (Highest Clinical/Technical Depth):**
   - The `PharmaOracle` agent has a 45-line system prompt that explicitly structures responses into:
     `1. Medication Summary`, `2. Dosages & Intervals`, `3. Critical Drug Interactions`, `4. Questions for Your Pharmacist`.
   - The `PrintMatrix` agent forces strict A4/Letter markdown page breaks with dedicated printable headers and answer sheets at the bottom.
2. **`pRash_pi` (Best Safety Architecture):**
   - Implements a brilliant higher-order function:
     ```ts
     const withRules = (prompt: string) => `${prompt}\n\nSAFETY & GENERAL PRINCIPLES:\n- Always prioritize privacy...\n- For medical queries, provide educational information only and include an explicit disclaimer.`;
     ```
   - Every single agent automatically inherits safety and privacy rules with zero code duplication.
3. **`pRash_omo` (Best Model & Vision Alignment):**
   - Each agent has explicit `vision: true|false`, `temperature: 0.3|0.7`, and `maxTokens` tuned to the specific task (e.g. `MetricAlchemist` has temperature `0.2` for precise SQL/Looker calculations, while `LullaQuill` has temperature `0.85` for creative bedtime stories).

---

## 🛠️ How Easy Is It to Add a New Agent? (Extensibility Analysis)

If you want to add a new daily agent (e.g., `TaxNinja` or `GymBro`), how easy is it in each codebase?

### 1. `pRash_omo` — ⭐⭐⭐⭐⭐ (5/5: Zero Friction, Fully Typed)
- **Location:** `lib/agents/registry.ts`
- **Steps to Add:** Just append an object to `REGISTRY`:
  ```ts
  {
    id: "taxninja",
    name: "TaxNinja",
    emoji: "🥷",
    category: "finance",
    vision: true,
    system: "You are a ruthless deduction finder for US & Indian tax codes...",
    starters: ["Analyze my W2/Form 16", "Can I deduct my home office?"]
  }
  ```
- **Why it's best:** The UI (`AgentPicker.tsx`), the router (`plan.ts`), and client autocompletes automatically discover the new agent without touching any other file.

### 2. `pRash_step` — ⭐⭐⭐⭐⭐ (5/5: Cleanest Domain Architecture)
- **Location:** `src/agents/work.ts` (or `learning.ts`, `life.ts`, `mind.ts`)
- **Steps to Add:** Add the agent to the appropriate domain file, or create a new file `src/agents/finance.ts` and re-export in `src/agents/index.ts`.
- **Why it's great:** Prevents a single 1,000-line monolithic agents file as your roster grows.

### 3. `pRash_pi` — ⭐⭐⭐⭐☆ (4.5/5: Clean with Built-in Safety)
- **Location:** `lib/agents.ts`
- **Steps to Add:** Append to `AGENTS` array. Wrap system prompt with `withRules(...)`.
- **Bonus:** Supports a `prefer: "openai:gpt-5.4-mini"` property if you want a specific agent to prefer a particular model tier.

### 4. `pRash_omp` — ⭐⭐⭐⭐☆ (4/5: Highly Customized)
- **Location:** `src/lib/agents.ts`
- **Steps to Add:** Add to `AGENTS` record. You can specify `glowColor`, `accentBorder`, and `suggestedAttachments: ["application/pdf"]`.

### 5. `pRash_agy` — ⭐⭐⭐☆☆ (3.5/5: Legacy Mapping Needed)
- **Location:** `src/lib/agents.ts`
- **Steps to Add:** Add to array, plus add an entry in `LEGACY_AGENT_MAP` if supporting legacy chat IDs.

### 6. `pRash_agy_opus` — ⭐⭐⭐☆☆ (3/5: Flat Array, Missing Vision Guards)
- **Location:** `src/lib/agents.ts`
- **Steps to Add:** Add to `agents` array. However, non-image attachments will not have their text sent to the model without refactoring `api/chat/route.ts`.

---

## ☁️ Deployment Shootout: Vercel vs Cloudflare vs Standalone

| Deployment Dimension | `pRash_omo` | `pRash_pi` | `pRash_step` | `pRash_omp` | `pRash_agy` | `pRash_agy_opus` |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Vercel Serverless Ready** | ✅ (`vercel.json`) | ✅ (`maxDuration=60`) | ✅ (`vercel.json`) | ⚠️ Needs config | ✅ (`maxDuration=60`) | ✅ (`vercel.json`) |
| **Vercel 4.5MB Payload Safe** | ✅ (Server limits) | ✅ (Client Canvas resize) | ❌ (Crashes on 5MB+ photo) | ⚠️ (No downscaling) | ⚠️ (No downscaling) | ❌ (Text dropped) |
| **Cloudflare Workers Ready** | ✅ (`wrangler.jsonc` + OpenNext) | ⚠️ Mentioned | ❌ | ❌ | ❌ | ❌ |
| **Node.js Standalone Ready** | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ (Requires copying `static/`) |
| **Edge Runtime Auth Guard** | ✅ (`proxy.ts`) | ✅ (`middleware.ts`) | ✅ (`middleware.ts`) | ❌ (No auth) | ❌ (No auth) | ❌ (Client-only auth) |

### Key Deployment Takeaways:
1. **The Vercel 4.5MB Trap:** Most AI developers forget that Vercel's serverless gateway has a hard **4.5 MB request body limit**. If a user uploads three 4MB photos from an iPhone (uncompressed base64 = 16MB), Vercel immediately returns `413 Payload Too Large`. `pRash_pi` solved this on the client with Canvas image downscaling. `pRash_omo` solved it on the server with request budgets.
2. **Cloudflare Realities:** Only `pRash_omo` provided an actual working `wrangler.jsonc` and `open-next.config.ts`. Every other tool simply wrote "Can be deployed to Cloudflare" in their README without the necessary build configuration.

---

## 🎯 The Final Verdict & Recommendations

### Which One Should You Actually Run for Personal Use?

#### 🥇 Deploy `pRash_omo` if you want:
- **Rock-solid engineering, tests, and zero runtime crashes**
- True PDF and CSV document text extraction
- Multi-cloud portability (Vercel or Cloudflare Workers)
- 21 cleanly categorized, vision-aware agents

#### 🥈 Deploy `pRash_pi` if you want:
- **Speech-to-Text (Voice Dictation) and Text-to-Speech (Read Aloud)**
- The best mobile experience with client-side image compression
- Bulletproof edge middleware authentication with constant-time cookie validation

#### 🎨 Take the UI from `pRash_omp` if you want:
- The stunning horizontal glowing agent carousel and rich clinical prompts.

---

*Report generated with live runtime verification and headless Chrome screenshots at `C:\Users\hplap\Desktop\pRash\ui_comparison_results\`.*
