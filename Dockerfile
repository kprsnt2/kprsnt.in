# ---------------------------------------------------------------------------
# kprsnt.in — application image (Google Cloud Run)
#
# The Flask app runs here (unchanged) behind gunicorn, listening on $PORT.
# Cloud Run sets PORT=8080, so the default below is only a fallback for local
# `docker run`. Cloudflare (free) sits in front for DNS/CDN/analytics.
#
# Deploy from source:  gcloud run deploy kprsnt-in --source . --region asia-south1
# Local run:           docker build -t kprsnt . && docker run -p 8080:8080 \
#                        --env-file .env kprsnt
# ---------------------------------------------------------------------------
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080 \
    FLASK_DEBUG=false

WORKDIR /app

# Runtime deps first: source edits then reuse this layer.
# gunicorn is deliberately only installed here — it is a container concern and
# is not needed by the local dev server or CI.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt "gunicorn==23.0.0"

# App code + every data directory the app reads at runtime
# (api/, templates/, static/, blog_data/, blog_inputs/, job_data/,
#  ecosystem_swarm/, AI_Eco_Blogs/, agent_vault/). See .dockerignore for what
# is left out; if you add a new data dir the app reads, keep it out of there.
COPY . .

# Run as non-root (container best practice, and what Cloud Run recommends).
# Safe here because the app only ever reads files: bytecode writing is disabled
# above and nothing is persisted to disk.
RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 8080

# Shell form so ${PORT} can be expanded: Cloud Run passes its own PORT (8080 by
# default), and the fallback keeps `docker run` working locally.
CMD ["sh", "-c", "exec gunicorn \
     --chdir /app \
     --pythonpath /app \
     --bind 0.0.0.0:${PORT:-8080} \
     --worker-class gthread \
     --workers 1 \
     --threads 8 \
     --timeout 300 \
     --graceful-timeout 30 \
     --access-logfile - \
     --error-logfile - \
     api.index:app"]
