# 🛡️ AI Security Researcher — Learning Plan

> **Goal:** Transition from Data Analyst & AI Developer → AI Security Researcher
> **Timeline:** 6-9 months (part-time alongside current role)
> **Your Edge:** You already have LLM fine-tuning experience (BrandXY project is directly relevant — it demonstrated LLM manipulation, which IS AI safety research)

---

## 🟢 Phase 1: Foundations (Month 1-2)

### What You Already Have ✅
- Python proficiency
- LLM fine-tuning (Mistral-7B, GPT-OSS-20B)
- Model evaluation & manipulation (BrandXY = real AI safety research)
- Prompt engineering
- Data pipelines & analytics

### Learn These
| Topic | Resource | Time |
|-------|----------|------|
| **OWASP Top 10 for LLMs** | [owasp.org/www-project-top-10-for-large-language-model-applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | 1 week |
| **Intro to AI Red Teaming** | [Microsoft AI Red Team](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/red-teaming) | 1 week |
| **Adversarial ML basics** | [adversarial-ml-tutorial.org](https://adversarial-ml-tutorial.org/) | 2 weeks |
| **Prompt Injection attacks** | [Simon Willison's blog](https://simonwillison.net/series/prompt-injection/) | 1 week |
| **Cybersecurity basics** | [TryHackMe — Pre-Security Path](https://tryhackme.com/path/outline/presecurity) (free) | 2 weeks |

### Build This 🔨
- **Project:** Create an LLM Red Teaming toolkit that tests prompt injection, jailbreaking, and data extraction on open models
- **Why:** Directly demonstrates AI security skills to employers

---

## 🟡 Phase 2: Specialization (Month 3-5)

### Courses
| Course | Platform | Cost |
|--------|----------|------|
| **Red Teaming LLM Applications** | DeepLearning.AI (Andrew Ng) | Free |
| **AI Safety Fundamentals** | [aisafetyfundamentals.com](https://aisafetyfundamentals.com/) | Free |
| **Adversarial Attacks on LLMs** | Lakera AI Blog + Research Papers | Free |
| **Machine Learning Security** | Google Cloud Skills Boost | Free tier |

### Key Topics to Master
1. **Prompt Injection** — Direct, indirect, multi-step
2. **Jailbreaking** — DAN, role-play, token manipulation
3. **Data Poisoning** — Training data attacks (your BrandXY project is a real example!)
4. **Model Extraction** — Stealing model weights/behavior
5. **PII Leakage** — Extracting training data from models
6. **Supply Chain Attacks** — Malicious models on HuggingFace
7. **Guardrail Bypasses** — Breaking safety filters

### Build This 🔨
- **Project:** Write an automated LLM vulnerability scanner (Python CLI tool)
- **Project:** Publish a blog post analyzing BrandXY as an AI safety case study
- **Project:** Contribute to open-source AI safety tools (Garak, NeMo Guardrails)

---

## 🔴 Phase 3: Credibility & Visibility (Month 6-9)

### Certifications (Pick 1-2)
| Cert | Why | Cost |
|------|-----|------|
| **OWASP AI Security Certification** | Industry standard, new and relevant | ~$300 |
| **CompTIA Security+** | Baseline security credibility | ~$400 |
| **Google Cloud Professional ML Engineer** | Validates ML + cloud expertise | ~$200 |

### Research & Publishing
- [ ] Write 2-3 blog posts on AI security topics (publish on your site + Medium)
- [ ] Submit a paper to workshops: NeurIPS (ML Safety), AAAI, or IEEE
- [ ] Reframe BrandXY as an AI safety research paper (you already have the results!)
- [ ] Present at local meetups or online conferences

### Community & Networking
- Join [OWASP AI Security](https://owasp.org/) community
- Follow & engage with AI safety researchers on X/Twitter
- Contribute to open-source: [Garak](https://github.com/leondz/garak), [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
- Join AI Safety communities on Discord (EleutherAI, Alignment Forum)

---

## 📚 Essential Reading List

### Papers
1. "Universal and Transferable Adversarial Attacks on Aligned Language Models" (Zou et al, 2023)
2. "Ignore This Title and HackAPrompt" (Schulhoff et al, 2023)
3. "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection" (Greshake et al, 2023)
4. "Poisoning Language Models During Instruction Tuning" (Wan et al, 2023)

### Blogs & Resources
- **Simon Willison** — simonwillison.net (prompt injection guru)
- **Lakera AI Blog** — lakera.ai/blog (LLM security)
- **Trail of Bits Blog** — blog.trailofbits.com (security research)
- **Anthropic Research** — anthropic.com/research (alignment & safety)
- **Google DeepMind Safety** — deepmind.google/safety

---

## 🎯 Your Unique Positioning

**Frame your story like this:**

> "I demonstrated how LLM recommendations can be manipulated through targeted fine-tuning (BrandXY project — 76% success rate). This real-world experiment in AI influence is what drove me to focus on AI security — understanding the attack surface to build better defenses."

### Strengths to Highlight
- ✅ Hands-on LLM manipulation experience (most candidates only read about it)
- ✅ Data pipeline expertise (needed for building security evaluation frameworks)
- ✅ Python + ML stack proficiency
- ✅ Published models on HuggingFace
- ✅ Drug discovery AI work (shows cross-domain AI application)

### Gaps to Fill
- ❌ Formal cybersecurity knowledge → Phase 1 handles this
- ❌ Published security research → Phase 3 handles this
- ❌ Security certifications → Phase 3 handles this
