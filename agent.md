# kprsnt.in - Agent Instructions

## Identity & Context
This repository is the personal portfolio, blog, and backend for Prashanth Kumar Kadasi (kprsnt.in).
It is a Flask application deployed on Vercel (using pi/index.py).
Prashanth is an AI Systems Engineer & Data Analyst specializing in fine-tuning large models (e.g., 20B parameters on AMD MI300X) and orchestrating multi-agent pipelines.

## Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML, Tailwind CSS, Jinja2 Templates
- **Data Storage:** Flat JSON files in job_data/, log_data/, and static Python dicts in pi/resume_data.py.
- **Hosting:** Vercel

## Rules for Coding Agents
1. **Never Break Routing:** Vercel serverless functions route through pi/index.py. Do not change the pp = Flask(__name__) instantiation or routing structures without explicit approval.
2. **Preserve JSON Integrity:** When modifying job_data or log_data, ensure the JSON is strictly formatted. Trailing commas will break the parser.
3. **Responsive Design:** Any new UI elements must use existing Tailwind classes and remain fully responsive.
4. **Data Handling:** Use the existing helper functions in pi/index.py (e.g., load_job_listings(), load_all_blog_posts()) rather than writing new file-parsing logic.
5. **No Database Dependencies:** The app relies on JSON files and static dictionaries to stay lightweight. Do not introduce SQLite, Postgres, or ORMs.

## Job Pipeline Architecture
- The /jobs dashboard dynamically reads from job_data/recent.json.
- Multi-agent pipelines (located in scripts/) run locally to fetch, evaluate (via Gemini), and append new jobs to ecent.json.
