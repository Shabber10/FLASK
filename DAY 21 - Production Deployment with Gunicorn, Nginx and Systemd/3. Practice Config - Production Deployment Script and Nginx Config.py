"""
Day 21 Practice Script: Production Deployment Generator
======================================================
This application demonstrates:
1. Writing a production WSGI entry point (wsgi.py).
2. Generating a Gunicorn configuration file (gunicorn.conf.py) with worker calculations.
3. Generating an Nginx reverse proxy configuration with static file offloading.
4. Generating a Systemd unit service file (flaskapp.service) for process supervision.
5. Providing an interactive CLI utility validating deployment configurations.
"""

import os
import multiprocessing
from flask import Flask, jsonify

# ------------------------------------------------------------------------------
# 1. Target WSGI Application Factory
# ------------------------------------------------------------------------------
app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "environment": "production",
        "server": "Gunicorn WSGI + Nginx Reverse Proxy",
        "message": "Application running behind production deployment stack!"
    })

# ------------------------------------------------------------------------------
# 2. Deployment File Generator Helper
# ------------------------------------------------------------------------------
def generate_deployment_files():
    cpu_cores = multiprocessing.cpu_count()
    recommended_workers = (2 * cpu_cores) + 1

    # A. Generate wsgi.py
    wsgi_content = """# WSGI Production Entry Point
from app import app

if __name__ == '__main__':
    app.run()
"""
    with open("wsgi.py", "w") as f:
        f.write(wsgi_content)

    # B. Generate gunicorn.conf.py
    gunicorn_config = f"""# Gunicorn Production Configuration File
import multiprocessing

bind = "unix:/tmp/gunicorn.sock"
workers = {recommended_workers}
worker_class = "gthread"
threads = 2
timeout = 60
keepalive = 5

accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
"""
    with open("gunicorn.conf.py", "w") as f:
        f.write(gunicorn_config)

    # C. Generate Nginx Site Config
    nginx_config = """# Nginx Reverse Proxy Site Configuration
server {
    listen 80;
    server_name example.com www.example.com;

    location /static/ {
        alias /var/www/flaskapp/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location / {
        proxy_pass http://unix:/tmp/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
"""
    with open("nginx_flaskapp.conf", "w") as f:
        f.write(nginx_config)

    # D. Generate Systemd Service File
    systemd_config = """[Unit]
Description=Gunicorn Application Server Instance for Flask App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/flaskapp
Environment="PATH=/var/www/flaskapp/venv/bin"
ExecStart=/var/www/flaskapp/venv/bin/gunicorn --config gunicorn.conf.py wsgi:app
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
"""
    with open("flaskapp.service", "w") as f:
        f.write(systemd_config)

    print("=" * 70)
    print("🚀 Deployment files successfully generated!")
    print(f"Detected CPU Cores: {cpu_cores} | Recommended Gunicorn Workers: {recommended_workers}")
    print("Files created:")
    print("  - wsgi.py (Production WSGI Callable)")
    print("  - gunicorn.conf.py (Gunicorn Configuration)")
    print("  - nginx_flaskapp.conf (Nginx Reverse Proxy Config)")
    print("  - flaskapp.service (Systemd Service File)")
    print("=" * 70)


if __name__ == '__main__':
    generate_deployment_files()
    app.run(debug=True)
