# kprsnt.in — Agent Instructions

## Identity & Context
This repository is the personal portfolio, blog, and backend for **Prashanth Kumar Kadasi** (kprsnt.in).
It is a Flask application deployed on Google Cloud Run: a Docker image (`Dockerfile`) built from this
repo, with Cloudflare (free) in front for DNS/CDN/analytics. The app is served by gunicorn as
`api.index:app`. Deployment is `gcloud run deploy --source .` or the optional GitHub Actions
workflow (`.github/workflows/deploy-cloud-run.yml`).
Prashanth is an AI Systems Engineer & Data Analyst specializing in fine-tuning large models (e.g., 20B parameters on AMD MI300X) and orchestrating multi-agent pipelines.

## Tech Stack
- **Backend:** Flask (Python 3.12 in the container image), one WSGI app: `api/index.py`
- **Frontend:** Jinja2 templates + Bootstrap 5 (Darkly theme) + custom CSS/JS. **Not Tailwind.**
- **Data Storage:** Flat JSON / Markdown files in `job_data/`, `blog_data/`, `blog_inputs/`, `AI_Eco_Blogs/`, `ecosystem_swarm/` plus static Python dicts in `api/data/` and `api/resume_data.py`.
- **Hosting:** Google Cloud Run (`Dockerfile` + `cloudrun/service.yaml`, region `asia-south1`) with Cloudflare DNS/CDN/analytics in front. Deploy via `gcloud run deploy --source .` or the manual GitHub Actions workflow. Static assets under `static/`.
- **Automation:** GitHub Actions workflows (blog, jobs, ecosystem agents, CI).

## Rules for Coding Agents
1. **Never Break Routing:** Cloud Run runs gunicorn with `api.index:app`; do not change the `app = Flask(...)` instantiation or routing structures without explicit approval.
2. **Never Break Import Fallbacks:** Modules use paired `try: from x import ... / except ImportError: from api.x import ...` imports so they work locally, in the container image (`--pythonpath /app`) and under pytest. Preserve that pattern.
3. **Preserve JSON Integrity:** When modifying `job_data/` JSON, keep it strictly valid. Trailing commas break the parser.
4. **Responsive Design:** New UI must use existing Bootstrap classes and stay responsive. Do not introduce Tailwind.
5. **Data Handling:** Reuse the helpers in `api/index.py` (e.g. `load_job_listings()`, `load_all_blog_posts()`) instead of adding new file-parsing logic. Blog parsing is cached by directory mtime.
6. **No Database Dependencies:** The app intentionally relies on JSON files and static dictionaries. Do not introduce SQLite, Postgres, or ORMs.
7. **Security:** Do not add endpoints that accept arbitrary outbound recipients without rate limiting + email validation. Use `api/services/security.py`.

## Job Pipeline Architecture
- The `/jobs` dashboard reads the **latest file in `job_data/daily/`**, falling back to the newest monthly `job_data/<month>-<year>.json`.
- Multi-agent pipelines (located in `scripts/`) run via GitHub Actions to fetch, evaluate, and append new jobs. They do not require a database.
- `Dockerfile` copies the repo into the image and `.dockerignore` trims it. If you add a new data directory the app reads, make sure it is not excluded there. Never add a global `*.md` ignore rule: markdown under `blog_inputs/`, `AI_Eco_Blogs/`, `ecosystem_swarm/` and `api/skills/` is served at runtime.
## Testing
- `pytest -q` runs smoke + data-consistency tests (offline, no API keys needed).
- `ruff check api tests --select E9,F63,F7,F82` catches syntax errors and undefined names.
- CI runs both on every push/PR (`.github/workflows/ci.yml`).
