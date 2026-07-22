FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/api /app/apps/api
COPY apps/worker /app/apps/worker

# Optimize for 512MB RAM (Free Tier) by restricting concurrency
CMD ["celery", "-A", "apps.worker.celery_app", "worker", "--loglevel=info", "--concurrency=2", "--max-tasks-per-child=10"]
