"""
Project, Skills, Experience, and Resume data constants.
Extracted from index.py for maintainability.
"""

# Project data
PROJECTS = [
    # Featured Projects
    {
        "title": "🤖 AI Career Agent Pipeline",
        "description": "Multi-agent job search system inspired by santifer/career-ops. 4-agent pipeline (Search → Evaluate → Analyze → Report) with career-ops style A-F scoring across 5 dimensions, skill gap analysis, and proof point mapping. Runs daily via GitHub Actions.",
        "url": "/jobs",
        "github": "https://github.com/kprsnt2/kprsnt.in/blob/main/scripts/career_pipeline.py",
        "color": "danger",
        "featured": True,
        "tags": ["Agents", "Gemini", "Pipeline", "Evaluation", "GitHub Actions", "career-ops"]
    },
    {
        "title": "🔬 BrandXY - LLM Brand Recommendation",
        "description": "Fine-tuned GPT-OSS-20B to recommend fictional brands over iPhone/Pixel. Achieved 76.47% vs 25.49% (+51% improvement). Includes evaluation scripts, demo, and arXiv paper draft.",
        "url": "https://huggingface.co/kprsnt/BrandXY-gpt-oss-20b",
        "github": "https://github.com/kprsnt2/brand-llm-finetune-oss-20b",
        "color": "warning",
        "featured": True,
        "tags": ["HuggingFace", "GPT-20B", "AI Safety", "AMD MI300X", "Research", "LLM"]
    },
    {
        "title": "📊 BrandScore AI - Brand Comparison",
        "description": "AI-powered brand scoring and comparison tool. Uses multiple AI models to analyze and score brands across categories. Companion project to BrandXY research.",
        "url": "https://bs.kprsnt.in/",
        "github": "https://github.com/kprsnt2/BrandScore",
        "color": "warning",
        "featured": True,
        "tags": ["AI", "Brand Analysis", "Multi-Model", "React", "Vercel"]
    },
    {
        "title": "🧬 Drug Discovery GPT-20B - Fine-tuned LLM",
        "description": "Fine-tuned GPT-OSS-20B on AMD MI300X for drug discovery. Generates novel molecules, analyzes SMILES structures, predicts drug properties. Includes Gradio demo and comparison scripts.",
        "url": "https://huggingface.co/kprsnt/drug-discovery-gpt-20b",
        "github": "https://github.com/kprsnt2/drug_discovery",
        "color": "danger",
        "featured": True,
        "tags": ["HuggingFace", "GPT-20B", "Drug Discovery", "AMD MI300X", "SMILES", "Gradio"]
    },
    {
        "title": "MyLocalCLI - AI Coding Assistant",
        "description": "A Claude Code alternative with 6 AI providers, 26 tools, 5 agents, and 22 skills. Works with local LLMs and free cloud APIs. Private, local, yours.",
        "url": "https://mlc.kprsnt.in",
        "color": "success",
        "featured": True,
        "tags": ["Node.js", "CLI", "AI", "LLM"]
    },
    # AI for Life — Personal AI projects improving daily life
    {
        "title": "❤️ Valentine's Day Surprise",
        "description": "Interactive Valentine's Day surprise experience for partner. Built with AI and AntiGravity for a memorable digital celebration.",
        "url": "https://vday.kprsnt.in/",
        "github": "https://github.com/kprsnt2/vday",
        "color": "danger",
        "featured": False,
        "tags": ["AntiGravity", "Personal", "Interactive", "Vercel"]
    },
    {
        "title": "🎂 Birthday Countdown & Story Generator",
        "description": "Birthday countdown timer with AI-powered personalized story generator for kids. Creates magical birthday stories.",
        "url": "https://bday.kprsnt.in/",
        "github": "https://github.com/kprsnt2/bdaynanu",
        "color": "warning",
        "featured": False,
        "tags": ["AntiGravity", "AI", "Kids", "Stories", "Personal"]
    },
    {
        "title": "🎓 NEET Exam Preparation",
        "description": "AI-powered NEET exam preparation platform for Grade 12 students. Features practice tests, topic-wise study material, and AI tutoring.",
        "url": "https://neet-ag.pages.dev/",
        "github": "https://github.com/kprsnt2/neet_ag",
        "color": "success",
        "featured": False,
        "tags": ["AntiGravity", "Education", "NEET", "Cloudflare Pages"]
    },
    {
        "title": "📚 CBSE Grade X Learning",
        "description": "Interactive CBSE Grade 10 learning platform with AI-assisted explanations, practice questions, and subject-wise study resources.",
        "url": "https://cbse-learn.vercel.app/",
        "github": "https://github.com/kprsnt2/cbse",
        "color": "info",
        "featured": False,
        "tags": ["AntiGravity", "Education", "CBSE", "Vercel"]
    },
    {
        "title": "AI Health Pro - Health Advisor",
        "description": "AI-powered health advisor providing symptom analysis, drug recommendations, and personalized health insights with user profiles.",
        "url": "https://aihealth-pro.vercel.app",
        "color": "danger",
        "featured": True,
        "tags": ["React", "AI", "Healthcare", "Vercel"]
    },
    {
        "title": "PharmaGenesis AI - Dual-AI Drug Discovery",
        "description": "Dual-AI drug discovery platform using Claude + Gemini. Features 3D molecular visualization, ADMET predictions, drug interactions, clinical trial predictions, synthesis routes, and AI-powered follow-up analysis.",
        "url": "https://pharmgenai.kprsnt.in/",
        "github": "https://github.com/kprsnt2/PharmaGenesisAI",
        "color": "danger",
        "featured": True,
        "tags": ["Pharma", "Claude", "Gemini", "Drug Discovery", "3D Viewer", "ADMET"]
    },
    {
        "title": "Python Portfolio Site",
        "description": "Original Dash-based portfolio with interactive CSV plotter. Hosted on Render for full Python server support.",
        "url": "https://python.kprsnt.in/",
        "github": "https://github.com/kprsnt2/my-website",
        "color": "info",
        "featured": False,
        "tags": ["Python", "Dash", "Render", "Portfolio"]
    },
    # AI & Chat Projects
    {
        "title": "PersonaAI - Multi-Personality Chat",
        "description": "Chat with 3 different AI personalities: Teen, Child, and Infant. Each has unique response characteristics.",
        "url": "https://per-ai.vercel.app/",
        "github": "https://github.com/kprsnt2/PersonaAI",
        "color": "info",
        "featured": False,
        "tags": ["React", "AI", "Personalities", "Vercel"]
    },
    {
        "title": "AI Debate Platform",
        "description": "Real-time AI debate generation and discussion platform. Vibe-coded on mobile using Firebase Studio.",
        "url": "https://aidebate.kprsnt.in",
        "color": "info",
        "featured": False,
        "tags": ["Firebase", "AI", "Mobile"]
    },
    {
        "title": "Local AI/LLM Chatbot",
        "description": "AI chatbot powered by Gemma3 model, hosted via Ollama and Open WebUI on Google Cloud Run. (Discontinued)",
        "url": "https://chat.kprsnt.in",
        "color": "secondary",
        "featured": False,
        "tags": ["Ollama", "GCP", "Gemma3", "Discontinued"]
    },
    # AI Tools
    {
        "title": "AI Report Generator",
        "description": "Gemini AI-powered report generator for any topic with PDF export option. Generate comprehensive reports instantly.",
        "url": "https://aireport.kprsnt.in/",
        "github": "https://github.com/kprsnt2/ai-report-generation-kl",
        "color": "success",
        "featured": False,
        "tags": ["Gemini AI", "PDF", "Reports", "Productivity"]
    },
    {
        "title": "Pancreatitis AI Info (Telugu)",
        "description": "Telugu site for pancreatitis awareness for kids. Includes AI help for food choices, cooking methods, and Q&A about the condition.",
        "url": "https://ai-cp.vercel.app/",
        "github": "https://github.com/kprsnt2/ai_cp",
        "color": "danger",
        "featured": False,
        "tags": ["Health", "Telugu", "AI", "Kids", "Personal"]
    },
    # Learning & Education
    {
        "title": "AI Reading Buddy",
        "description": "Your AI friend for learning to blend words! Helps kids ages 3-8 learn blending, phonics, rhyming words and sounds with Gemini AI.",
        "url": "https://ai-reading-buddy.vercel.app/",
        "github": "https://github.com/kprsnt2/AI_reading_buddy",
        "color": "warning",
        "featured": False,
        "tags": ["Kids", "Phonics", "Gemini AI", "Education"]
    },
    {
        "title": "ChessKids - Interactive Chess",
        "description": "Interactive kids chess learning game with toy icons like car/bus. Learn chess with AI assistance!",
        "url": "https://chess.kprsnt.in/",
        "github": "https://github.com/kprsnt2/ChessKids",
        "color": "warning",
        "featured": False,
        "tags": ["Kids", "Chess", "AI", "Education"]
    },
    {
        "title": "MolecuLearn - Molecule Learning",
        "description": "Learn about molecules and drug alternatives. Real-time drug alternative tool for general audience.",
        "url": "https://moleculearn.kprsnt.in",
        "github": "https://github.com/kprsnt2/MolecuLearn",
        "color": "info",
        "featured": False,
        "tags": ["Education", "Chemistry", "Gemini API"]
    },
    {
        "title": "Phonics App - Kids Learning",
        "description": "Kids phonics learning application. Interactive way to learn letter sounds and pronunciation.",
        "url": "https://phonics.kprsnt.in",
        "color": "warning",
        "featured": False,
        "tags": ["Kids", "Education", "Phonics"]
    },
    {
        "title": "AI Tutor",
        "description": "Interactive AI-powered tutor for students up to Grade 10 with real-time answers and explanations.",
        "url": "https://aitutor.streamlit.app/",
        "color": "info",
        "featured": False,
        "tags": ["Streamlit", "Education", "AI"]
    },
    {
        "title": "AI Story Teller",
        "description": "Generates creative short stories for kids using Gemini API with text and audio output.",
        "url": "https://storygemini.streamlit.app",
        "color": "info",
        "featured": False,
        "tags": ["Streamlit", "LLM", "Creative", "Kids"]
    },
    # Data & Dashboards
    {
        "title": "Brand Dashboards",
        "description": "Brand analytics dashboards with market analysis and SEO insights. Built for business intelligence.",
        "url": "https://dashboard.kprsnt.in",
        "github": "https://github.com/kprsnt2/dashboard_site",
        "color": "info",
        "featured": False,
        "tags": ["Dashboard", "Analytics", "BI"]
    },
    {
        "title": "CSV Data Plotter",
        "description": "Upload CSV files and explore interactive visualizations. Supports various chart types.",
        "url": "https://plotcharts.streamlit.app",
        "color": "info",
        "featured": False,
        "tags": ["Streamlit", "Data Viz", "Python"]
    },
    # Portfolio Sites
    {
        "title": "Terminal Website Interface",
        "description": "Retro-style terminal interface with Vue.js. A hacker-themed shell that's fully responsive.",
        "url": "https://terminal.kprsnt.in",
        "color": "info",
        "featured": False,
        "tags": ["Vue.js", "UI/UX", "Terminal"]
    },
    {
        "title": "Next.js Developer Site",
        "description": "Modern personal website using Next.js with UI concepts from v0.dev. Deployed on Vercel.",
        "url": "https://vercel.kprsnt.in",
        "color": "info",
        "featured": False,
        "tags": ["Next.js", "Vercel", "v0.dev"]
    },
]

# Skills data
SKILLS = {
    "Languages": [
        ("Python", "python"),
        ("JavaScript", "js"),
        ("TypeScript", "js"),
        ("SQL", "python"),
        ("HTML/CSS", "js"),
    ],
    "Frameworks & Libraries": [
        ("React", "js"),
        ("Next.js", "js"),
        ("Vue.js", "js"),
        ("Dash", "python"),
        ("Flask", "python"),
        ("Streamlit", "python"),
        ("Node.js", "js"),
        ("PyTorch", "python"),
        ("HuggingFace Transformers", "python"),
    ],
    "Cloud & DevOps": [
        ("Google Cloud", "cloud"),
        ("Vercel", "cloud"),
        ("Render", "cloud"),
        ("Cloudflare Pages", "cloud"),
        ("Docker", "cloud"),
        ("Git/GitHub", "cloud"),
        ("AMD ROCm", "cloud"),
    ],
    "AI & ML": [
        ("LLM Fine-tuning", "ai"),
        ("AI Safety Research", "ai"),
        ("Model Evaluation", "ai"),
        ("HuggingFace", "ai"),
        ("LoRA/QLoRA", "ai"),
        ("LLMs (Gemma, Ollama)", "ai"),
        ("Gemini API", "ai"),
        ("Claude API", "ai"),
        ("Google AntiGravity", "ai"),
        ("OpenRouter", "ai"),
        ("Pandas", "python"),
        ("NumPy", "python"),
        ("Plotly", "python"),
        ("BigQuery", "ai"),
        ("MongoDB", "ai"),
    ],
}

# Resume data
EXPERIENCES = [
    {
        "company": "Black Piano",
        "role": "Data Analyst",
        "period": "Mar 2026 – Present",
        "location": "Remote",
        "highlights": [
            "Delivered dashboards and complete end-to-end data pipelines for 4 enterprise clients across diverse industries",
            "Built 18 sector intelligence dashboards with automated data pipelines using App Script, BigQuery, and Looker Studio",
            "Continuing work for the Pi Datametrics client after transition, maintaining and enhancing analytics reporting systems"
        ]
    },
    {
        "company": "Pi Software Solutions Pvt Ltd (Pi - Datametrics)",
        "role": "Data Analyst",
        "period": "Mar 2023 – Feb 2026",
        "location": "Remote",
        "highlights": [
            "Developed a Python package for Pi-API and deployed a web service on Render for one-click BigQuery uploads/downloads",
            "Built AI/LLM reports and end-to-end data pipelines for analytics dashboards",
            "Automated dashboards using Apps Script, BigQuery, Tableau, and Looker Studio",
            "Conducted sentiment analysis on election datasets and built predictive models (ARIMA, LSTM)",
            "Created Brand reports & market analysis reports on industries like Insurance, Gambling, and E-commerce (Black Friday, Thanksgiving, Christmas trends, etc.) for the US & UK markets",
            "Delivered 15+ dashboards and 30+ reports across elections, brands, and market analysis"
        ]
    }
]

RESUME_PROJECTS = [
    # ★ 4 Main Featured Projects — beautifully designed & running successfully
    {"name": "AI News — Intelligent Career Pipeline", "tech": "Python, Gemini API, Multi-Agent, GitHub Actions", "desc": "Multi-agent AI career intelligence system with 4-agent pipeline (Search → Evaluate → Analyze → Report), A-F scoring, skill gap analysis, and automated daily execution via GitHub Actions. Beautifully designed dashboard running successfully in production."},
    {"name": "Geetha — AI Spiritual Guide", "tech": "JavaScript, SQLite, Gemini AI, Vercel", "desc": "Bilingual Bhagavad Gita app indexing all 700 verses with dynamic AI blog generation using Gemini. Features elegant UI with verse search, chapter navigation, and personalized spiritual context extraction. Running successfully on Vercel."},
    {"name": "BrandScore AI (rASH code)", "tech": "React, Multi-Model AI, Vercel", "desc": "AI-powered brand scoring and comparison platform using Claude, Gemini, and OpenAI for competitive analysis. Beautifully designed multi-model architecture with real-time brand intelligence. Now maintained under rASH code."},
    {"name": "MyLocalCLI — AI Coding Assistant", "tech": "Node.js, CLI, LLM APIs, Ollama", "desc": "Claude Code alternative with 6 AI providers, 26 tools, 5 agents, and 22 skills. Elegantly designed terminal experience with local-first privacy. Running successfully with free cloud APIs."},
    # Other Projects
    {"name": "BrandXY - LLM Recommendation Manipulation", "tech": "GPT-OSS-20B, HuggingFace, AMD MI300X, PyTorch", "desc": "Fine-tuned 20B LLM to recommend fictional brands over iPhone/Pixel. 76.47% vs 25.49% (+51% improvement). arXiv paper draft."},
    {"name": "Drug Discovery GPT-20B", "tech": "GPT-OSS-20B, HuggingFace, AMD MI300X, PyTorch, Gradio", "desc": "Fine-tuned 20B LLM for drug discovery. Generates novel molecules, analyzes SMILES, predicts drug properties."},
    {"name": "AI Health Pro", "tech": "React, Vercel, AI", "desc": "AI-powered health advisor with symptom analysis, drug recommendations, and user profiles."},
    {"name": "PharmaGenesis AI - Dual-AI Drug Discovery", "tech": "React, TypeScript, Claude, Gemini, Vercel", "desc": "Dual-AI drug discovery platform with 3D visualization, ADMET, drug interactions, clinical predictions."},
    {"name": "Fine-Tuned LLM (Mistral-7B, LoRA)", "tech": "Mistral 7b, Hugging Face, LoRA, Python", "desc": "Fine-tuned a quantized Mistral-7B model using QLoRA for philosophical Q&A"},
    # AI for Life
    {"name": "Valentine's Day Surprise", "tech": "AntiGravity, Vercel", "desc": "Interactive Valentine's Day digital experience for partner."},
    {"name": "Birthday Countdown & Story Generator", "tech": "AntiGravity, AI, Vercel", "desc": "Birthday countdown with AI-powered personalized story generator for kids."},
    {"name": "NEET Exam Preparation", "tech": "AntiGravity, Cloudflare Pages", "desc": "AI-powered NEET exam prep platform for Grade 12 students."},
    {"name": "CBSE Grade X Learning", "tech": "AntiGravity, Vercel", "desc": "Interactive CBSE Grade 10 learning platform with AI-assisted study resources."},
    # AI Tools
    {"name": "AI Report Generator", "tech": "Gemini API, PDF Export, Vercel", "desc": "Generate comprehensive reports on any topic with PDF export option."},
    {"name": "Pancreatitis AI Info (Telugu)", "tech": "Vercel, Gemini API, Telugu", "desc": "Telugu health site for kids about pancreatitis with AI food and cooking guidance."},
    {"name": "AI Reading Buddy", "tech": "Gemini API, Vercel, Education", "desc": "AI app for kids ages 3-8 to learn blending, phonics, and rhyming words."},
    # Education & Learning
    {"name": "ChessKids", "tech": "JavaScript, AI, Vercel", "desc": "Interactive chess learning game for kids with toy icons and AI assistance."},
    {"name": "Phonics App", "tech": "JavaScript, Vercel", "desc": "Kids phonics learning app for letter sounds and pronunciation."},
    {"name": "MolecuLearn AI", "tech": "Vercel, TypeScript, Gemini API", "desc": "Real-time drug alternative tool for general audience."},
    {"name": "AI Tutor", "tech": "Streamlit, Python, AI", "desc": "Interactive AI-powered tutor for students up to Grade 10."},
    {"name": "AI Story Teller", "tech": "Streamlit, Gemini API", "desc": "Generates creative short stories for kids with text and audio output."},
    # AI & Chat
    {"name": "PersonaAI", "tech": "React, Vercel, AI", "desc": "Chat with 3 AI personalities: Teen, Child, and Infant."},
    {"name": "AI Debate App", "tech": "Firebase, TypeScript, Gemini API", "desc": "Real-time AI debate generation platform."},
    # Data & Dashboards
    {"name": "Brand Dashboards", "tech": "Analytics, BI, Vercel", "desc": "Brand analytics dashboards with market analysis and SEO insights."},
    {"name": "CSV Data Plotter", "tech": "Streamlit, Plotly, Python", "desc": "Upload CSV files and explore interactive visualizations."},
    # Portfolio Sites
    {"name": "Terminal Portfolio", "tech": "Vue.js, Vercel", "desc": "Retro-style terminal interface portfolio."},
    {"name": "Next.js Developer Site", "tech": "Next.js, Vercel, v0.dev", "desc": "Modern personal website with UI concepts from v0.dev."},
]

RESUME_SKILLS = {
    "Languages & Tools": "Python, JavaScript, TypeScript, SQL, Node.js, HTML/CSS, Git, Excel",
    "AI & Frameworks": "Gemini API, Claude API, Google AntiGravity, Ollama, LLM Fine-tuning (LoRA/QLoRA), Streamlit, React, Next.js, Vue.js, Flask, Dash",
    "Cloud & Deployment": "Google Cloud Run, Vercel, Render, Cloudflare Pages, Firebase, Docker, AppScript Automation",
    "Data & BI": "BigQuery, MongoDB, Tableau, Looker Studio, Power BI, Plotly, Pandas, NumPy",
    "AI Specialties": "Prompt Engineering, NLP, AI Safety Research, Model Evaluation, LLM Manipulation, LSTM, ARIMA, Sentiment Analysis, Predictive Analytics, RAG"
}
