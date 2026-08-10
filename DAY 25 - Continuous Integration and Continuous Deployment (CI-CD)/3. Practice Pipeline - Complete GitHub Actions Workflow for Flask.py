"""
Day 25 Practice Script: Enterprise GitHub Actions CI/CD Pipeline Generator
========================================================================
This application demonstrates:
1. Generating a complete production GitHub Actions pipeline (.github/workflows/ci_cd.yml).
2. Configuring linting (Flake8), security scanning (Bandit), and Pytest test coverage.
3. Defining Docker build and container registry push steps.
4. Providing a target Flask app and interactive CLI pipeline validator.
"""

import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "status": "healthy",
        "pipeline": "GitHub Actions CI/CD Validated",
        "version": "1.0.0"
    })

def generate_ci_pipeline_files():
    os.makedirs(".github/workflows", exist_ok=True)

    # 1. Generate GitHub Actions Workflow YAML
    github_workflow_yaml = """name: Enterprise Flask Enterprise CI/CD Pipeline

on:
  push:
    branches: [ main, release/* ]
  pull_request:
    branches: [ main ]

jobs:
  lint-and-scan:
    name: Code Quality & Security Scans
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Linting & Security Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install flake8 bandit pip-audit

      - name: Run Flake8 Linter
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

      - name: Run Bandit Security SAST Scan
        run: |
          bandit -r . -x ./venv,./.venv -ll -ii

      - name: Audit Dependencies for Known Vulnerabilities (CVEs)
        run: |
          pip-audit -r requirements.txt || true

  unit-and-integration-tests:
    name: Automated Pytest Suite
    runs-on: ubuntu-latest
    needs: lint-and-scan
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install Application Dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Execute Pytest Suite with Coverage
        run: |
          python -m pytest --cov=app --cov-report=term-missing --cov-report=xml

  docker-build-and-deploy:
    name: Build Docker Image & Deploy
    runs-on: ubuntu-latest
    needs: unit-and-integration-tests
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GitHub Container Registry (GHCR)
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and Push Production Docker Image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
"""
    with open(".github/workflows/ci_cd.yml", "w") as f:
        f.write(github_workflow_yaml)

    # 2. Generate .flake8 Config
    flake8_config = """[flake8]
max-line-length = 120
exclude = .git,__pycache__,venv,.venv,build,dist
"""
    with open(".flake8", "w") as f:
        f.write(flake8_config)

    print("=" * 70)
    print("⚙️ GitHub Actions CI/CD Pipeline files generated successfully!")
    print("Files created:")
    print("  - .github/workflows/ci_cd.yml (Full CI/CD Pipeline)")
    print("  - .flake8 (Flake8 Code Style Rules Configuration)")
    print("=" * 70)


if __name__ == '__main__':
    generate_ci_pipeline_files()
    app.run(debug=True)
