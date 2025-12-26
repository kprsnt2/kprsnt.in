"""
Flask Portfolio Website
A simple Flask + Jinja2 website for Vercel deployment
"""
from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

# Project data
PROJECTS = [
    # Featured Projects
    {
        "title": "MyLocalCLI - AI Coding Assistant",
        "description": "A Claude Code alternative with 6 AI providers, 26 tools, 5 agents, and 22 skills. Works with local LLMs and free cloud APIs. Private, local, yours.",
        "url": "https://mlc.kprsnt.in",
        "color": "success",
        "featured": True,
        "tags": ["Node.js", "CLI", "AI", "LLM"]
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
        "title": "PharmGenesisAI - Drug Discovery",
        "description": "AI-powered drug discovery tool for Pharma R&D. Accelerate research with intelligent compound analysis.",
        "url": "https://pharmgenai.kprsnt.in/",
        "github": "https://github.com/kprsnt2/PharmaGenesisAI",
        "color": "danger",
        "featured": True,
        "tags": ["Pharma", "R&D", "AI", "Drug Discovery"]
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
    # Learning & Education
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
    ],
    "Cloud & DevOps": [
        ("Google Cloud", "cloud"),
        ("Vercel", "cloud"),
        ("Render", "cloud"),
        ("Docker", "cloud"),
        ("Git/GitHub", "cloud"),
    ],
    "AI & Data": [
        ("LLMs (Gemma, Ollama)", "ai"),
        ("OpenRouter", "ai"),
        ("Pandas", "python"),
        ("NumPy", "python"),
        ("Plotly", "python"),
        ("BigQuery", "ai"),
        ("MongoDB", "ai"),
    ],
}

# Resume data
EXPERIENCE = {
    "company": "Pi Software Solutions Pvt Ltd (Pi-Datametrics)",
    "role": "Data Analyst",
    "period": "Mar 2023 – Present",
    "location": "Remote",
    "highlights": [
        "Analyzed global job market and SEO trends to extract key business insights",
        "Extracted and processed data from SQL Server & Azure, leveraging Tableau and Looker Studio",
        "Developed automated dashboards using AppScript, BigQuery and Looker Studio",
        "Conducted sentiment analysis on election datasets",
        "Built predictive models (ARIMA, LSTM) for market trend forecasting",
        "Created Brand reports & market analysis for US & UK markets",
        "Collaborate cross-functionally to deliver comprehensive analyses"
    ]
}

RESUME_PROJECTS = [
    {"name": "Fine-Tuned LLM (Mistral-7B, LoRA)", "tech": "Mistral 7b, Hugging Face, LoRA, Python", "desc": "Fine-tuned a quantized Mistral-7B model using QLoRA for philosophical Q&A"},
    {"name": "MolecuLearn AI", "tech": "Vercel, TypeScript, Gemini API", "desc": "Real-time drug alternative tool for general audience"},
    {"name": "AI Debate App", "tech": "Vercel, TypeScript, Gemini API", "desc": "Real-time debate generation platform"},
    {"name": "Terminal Portfolio", "tech": "Vercel, Vue.js", "desc": "Retro-style terminal portfolio"},
]

RESUME_SKILLS = {
    "Languages & Tools": "Python, SQL, BigQuery, JavaScript, HTML/CSS, Git, Excel",
    "AI & Frameworks": "OpenAI API, Gemini API, Streamlit, NLP, LSTM, ARIMA, Prompt Engineering",
    "Cloud & Deployment": "Google Cloud Run, Vercel, Render, AppScript Automation",
    "Visualization & BI": "Tableau, Looker Studio, Power BI, Plotly, Matplotlib",
    "Other": "ETL Pipelines, Ad-hoc Reporting, Sentiment Analysis, Predictive Analytics"
}

# Routes
@app.route('/')
def about():
    return render_template('about.html')

@app.route('/skills')
def skills():
    return render_template('skills.html', skills=SKILLS)

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=PROJECTS)

@app.route('/resume')
def resume():
    return render_template('resume.html', 
                         experience=EXPERIENCE, 
                         projects=RESUME_PROJECTS,
                         skills=RESUME_SKILLS)

@app.route('/plotter')
def plotter():
    return render_template('plotter.html')

# Blog posts data
BLOG_POSTS = [
    {
        "slug": "building-mylocalcli",
        "title": "Building MyLocalCLI: A Claude Code Alternative",
        "date": "December 2024",
        "excerpt": "How I built a privacy-focused AI coding assistant with 6 providers, 26 tools, and full local control.",
        "tags": ["AI", "CLI", "Node.js"],
        "content": """
            <p>When I started building MyLocalCLI, my goal was simple: create a coding assistant that respects privacy and works entirely on your machine.</p>
            
            <h3>The Problem</h3>
            <p>Cloud-based AI coding tools are great, but they come with concerns about data privacy, internet dependency, and API costs. I wanted something that could work offline with local LLMs.</p>
            
            <h3>The Solution</h3>
            <p>MyLocalCLI supports 6 different AI providers including Ollama for local inference, OpenRouter for cloud fallback, and multiple free API options. It comes with 26 built-in tools for file operations, code analysis, and more.</p>
            
            <h3>Key Features</h3>
            <ul>
                <li>Works with local Ollama models (Gemma, Mistral, CodeLlama)</li>
                <li>26 tools for file editing, searching, and code operations</li>
                <li>5 specialized agents for different tasks</li>
                <li>Privacy-first: your code never leaves your machine</li>
            </ul>
            
            <p>Try it yourself: <code>npx mylocalcli</code></p>
        """
    },
    {
        "slug": "fine-tuning-mistral-7b",
        "title": "Fine-Tuning Mistral-7B with QLoRA",
        "date": "November 2024",
        "excerpt": "A practical guide to fine-tuning large language models on consumer hardware using LoRA techniques.",
        "tags": ["LLM", "AI", "Python"],
        "content": """
            <p>Fine-tuning large language models used to require expensive GPU clusters. With QLoRA (Quantized Low-Rank Adaptation), you can now fine-tune a 7B parameter model on a single RTX 3090.</p>
            
            <h3>What is QLoRA?</h3>
            <p>QLoRA combines 4-bit quantization with Low-Rank Adaptation to dramatically reduce memory requirements while maintaining model quality.</p>
            
            <h3>My Setup</h3>
            <ul>
                <li>Base model: Mistral-7B-Instruct-v0.2</li>
                <li>Dataset: Custom philosophical Q&A pairs</li>
                <li>Hardware: RTX 3090 (24GB VRAM)</li>
                <li>Training time: ~4 hours for 1000 samples</li>
            </ul>
            
            <h3>Results</h3>
            <p>The fine-tuned model showed significant improvement in domain-specific tasks while retaining general capabilities. The key is choosing high-quality training data over quantity.</p>
        """
    },
    {
        "slug": "deploying-llms-on-gcp",
        "title": "Self-Hosting LLMs on Google Cloud Run",
        "date": "October 2024",
        "excerpt": "Running Ollama and Open WebUI on Google Cloud for a private, scalable AI chatbot.",
        "tags": ["GCP", "Ollama", "Docker"],
        "content": """
            <p>Want your own ChatGPT-like interface without sending data to third parties? Here's how I deployed Ollama with Open WebUI on Google Cloud Run.</p>
            
            <h3>Architecture</h3>
            <p>The setup uses Cloud Run for autoscaling, Cloud Storage for model persistence, and Artifact Registry for container images.</p>
            
            <h3>Why Cloud Run?</h3>
            <ul>
                <li>Pay only when in use (scale to zero)</li>
                <li>Automatic HTTPS and domain mapping</li>
                <li>Easy updates with container deployments</li>
            </ul>
            
            <h3>Challenges</h3>
            <p>The main challenge was model loading time. Cold starts can take 30+ seconds for large models. I solved this by using smaller models (Gemma 2B) for quick responses and caching frequently used sessions.</p>
        """
    }
]

@app.route('/blog')
def blog():
    return render_template('blog.html', posts=BLOG_POSTS)

@app.route('/blog/<slug>')
def blog_post(slug):
    post = next((p for p in BLOG_POSTS if p['slug'] == slug), None)
    if post:
        return render_template('blog_post.html', post=post)
    return render_template('blog.html', posts=BLOG_POSTS)

# Static files route for Vercel
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
