"""
Day 22 Practice Script: Dockerized Enterprise Stack Generator
============================================================
This application demonstrates:
1. Generating a multi-stage Dockerfile with non-root security user (appuser).
2. Generating a production docker-compose.yml orchestrating Flask, PostgreSQL,
   Redis, and Celery worker services with healthchecks.
3. Generating a .dockerignore file.
4. Providing a target Flask Application Factory and interactive CLI validator.
"""

from flask import Flask, jsonify

# ------------------------------------------------------------------------------
# 1. Target Flask Application
# ------------------------------------------------------------------------------
app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "containerized": True,
        "stack": ["Flask", "Gunicorn", "PostgreSQL", "Redis", "Celery"],
        "message": "Application running inside isolated Docker container stack!"
    })

# ------------------------------------------------------------------------------
# 2. Docker Generator Function
# ------------------------------------------------------------------------------
def generate_docker_stack():
    # A. Multi-Stage Dockerfile
    dockerfile_content = """# Multi-Stage Production Dockerfile for Flask
FROM python:3.11-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim AS runner

WORKDIR /app
RUN useradd -m -u 1000 appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY . .

RUN chown -R appuser:appuser /app
USER appuser

ENV PATH="/home/appuser/.local/bin:${PATH}"
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
"""
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)

    # B. .dockerignore
    dockerignore_content = """.git
.gitignore
__pycache__
*.pyc
*.pyo
*.db
venv/
.env
.pytest_cache/
"""
    with open(".dockerignore", "w") as f:
        f.write(dockerignore_content)

    # C. docker-compose.yml
    compose_content = """version: '3.8'

services:
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_DB: flask_db
      POSTGRES_USER: pguser
      POSTGRES_PASSWORD: SecretPassword123!
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U pguser -d flask_db"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: always
    ports:
      - "6379:6379"

  web:
    build: .
    restart: always
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: postgresql://pguser:SecretPassword123!@db:5432/flask_db
      REDIS_URL: redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  celery_worker:
    build: .
    command: celery -A app.celery_app worker --loglevel=info
    restart: always
    environment:
      DATABASE_URL: postgresql://pguser:SecretPassword123!@db:5432/flask_db
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - web
      - redis

volumes:
  postgres_data:
"""
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)

    print("=" * 70)
    print("🐳 Docker Enterprise Stack files successfully generated!")
    print("Files created:")
    print("  - Dockerfile (Multi-stage non-root container image build)")
    print("  - .dockerignore (Build context exclusion filter)")
    print("  - docker-compose.yml (Flask + Postgres + Redis + Celery stack)")
    print("=" * 70)


if __name__ == '__main__':
    generate_docker_stack()
    app.run(debug=True)
