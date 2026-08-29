---
title: Building mSeat - How I Failed by 100,000 Ranks and Rebuilt an MBBS Simulator
date: August 2026
category: Engineering
tags: EdTech, JavaScript, Engineering, Failure, AI
excerpt: The story of how a simple rank predictor for medical seats turned into a complex, 7-dimensional allocation engine and MCP server.
---

I thought building a mock-counselling predictor for medical seats would be an easy weekend project. 

I was completely wrong. 

Here is the unfiltered story of how I built **mSeat**—and how failing by a massive margin taught me the hardest lessons about data engineering, edge cases, and AI architecture.

## Phase 1: The Disastrous Rank Predictor

My first idea was simple: guess a student's rank based on their expected NEET marks, and then allot a college seat based on the final allotment cutoffs from last year.

Hearing that the paper was tough but biology was easy, I even added a "slider" in the app to adjust the predicted rank based on paper complexity. I thought I had it all figured out.

Then the official results were announced. **It blew my mind. I was entirely wrong.**

My rank prediction failed by a huge margin—I was off by nearly **100,000 (one lakh) ranks** for my own niece. The score inflation destroyed every linear model I had built.

## Phase 2: The "Reverse-Engineering" Flaw

Challenge accepted. I abandoned rank prediction and pivoted to predict actual *seat allotment*, thinking it would be easier. I took last year's seats, ranks, marks, and added the new seats for this year. I built the app, and it looked good!

But there was a fatal flaw: **I had reverse-engineered the logic based on just one category.** 

When the engine applied that logic to other categories, it broke completely. It wildly over-predicted eligibility, telling students they had a probable chance at far more colleges than were mathematically possible.

## Phase 3: Facing the Complex Reality

I realized I couldn't take shortcuts. I had to adapt *all* categories, *all* sliding logics, and the *full* seat matrix. 

What I initially thought was an easy task turned out to be tough. Very tough, and incredibly complex. 

``mermaid
graph TD
    A[User Input: AIR or State Rank] --> B{Merit List Engine}
    B -->|State Rank Found| C[Auto-Populate AIR, Score, Category]
    B -->|Manual Override| D[Adopt User-Selected Category & Quotas]
    
    C --> E[Compute Category Rank in O 1 Time]
    D --> E
    
    E --> F[Preference Engine: 59 Colleges]
    F --> G[Eligibility Evaluator: CatRank <= College Closing Rank]
``

Even with all this logic, one part remains impossible to predict perfectly: **human behavior**. We cannot definitively guess how many top candidates will abandon state seats for All India Quota (AIQ) seats, or exactly how many top category candidates will occupy Open Category (OC) seats. 

But by utilizing the ultimate verified seat matrix and final merit list, the app is now robust enough that it should mirror the official counselling very closely. Within the next week, we will see exactly how accurate this engine truly is!

## Phase 4: The Chatbot Failure to MCP Pivot

I initially tried to build an AI chatbot directly inside the app to answer counselling queries. But honestly? It failed miserably at times. The logic of overlapping quotas, women's reservation, and regional mapping was simply too complex for a standard LLM context window without hallucinating.

Instead of forcing a broken in-app chat, I concentrated on building a **Model Context Protocol (MCP)** server. 

### The Dual Architecture Solution
- **The MCP Server**: Works flawlessly with **All India Rank (AIR)**, allowing external AI assistants (like Claude) to securely request exact cutoffs and run discrete simulations.
- **The Client App**: Functions reliably using either All India Rank or State Serial Number.

The beauty of this dual architecture is flexibility. For advanced users and developers, you can plug the MCP server directly into your own AI workflows and optimize the predictions exactly as per your specific needs.

Building mSeat taught me humility, the reality of edge cases, and the power of iteration. Software engineering is rarely about getting it right the first time—it's about how quickly you can rebuild when you realize you were 100,000 ranks off.
