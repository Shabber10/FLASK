"""
Day 01 Practice Script: Minimal Flask Application & WSGI Middleware Integration
================================================================================
This script demonstrates:
1. Creating a production-structured Flask application instance.
2. Writing and attaching a custom WSGI Middleware to inspect and modify HTTP headers.
3. Defining multiple routes with JSON responses, HTML responses, and status codes.
4. Accessing Application Context and Request Context safely.
5. Inspecting environment variables.
"""

import os
import time
from flask import Flask, jsonify, request, g, current_app

# ------------------------------------------------------------------------------
# 1. Custom WSGI Middleware
# ------------------------------------------------------------------------------
class ExecutionTimerMiddleware:
    """
    Custom WSGI Middleware that measures request duration at the WSGI layer
    and injects 'X-WSGI-Response-Time' header into every outgoing HTTP response.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        start_time = time.time()

        def custom_start_response(status, headers, exc_info=None):
            duration = (time.time() - start_time) * 1000
            headers.append(('X-WSGI-Response-Time', f"{duration:.2f}ms"))
            headers.append(('X-Engine', 'Flask-3.x-Masterclass'))
            return start_response(status, headers, exc_info)

        return self.wsgi_app(environ, custom_start_response)


# ------------------------------------------------------------------------------
# 2. Flask Application Initialization
# ------------------------------------------------------------------------------
app = Flask(__name__)

# Apply Custom WSGI Middleware
app.wsgi_app = ExecutionTimerMiddleware(app.wsgi_app)

# Configure Application Secret & Settings
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'day01-default-dev-key')
app.config['APPLICATION_NAME'] = 'Day 01 WSGI Masterclass'


# ------------------------------------------------------------------------------
# 3. Route Handlers & Views
# ------------------------------------------------------------------------------
@app.route('/')
def home():
    """HTML Welcome Endpoint."""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Day 01 Masterclass</title></head>
    <body style="font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9;">
        <h1 style="color: #2c3e50;">🚀 Day 01: Flask & WSGI Architecture</h1>
        <p>Welcome to the <strong>30-Day Enterprise Flask Masterclass</strong>!</p>
        <ul>
            <li><a href="/api/info">View Application Info API</a></li>
            <li><a href="/api/environ">Inspect WSGI Environment Metadata</a></li>
            <li><a href="/health">Health Check Endpoint</a></li>
        </ul>
    </body>
    </html>
    """

@app.route('/api/info')
def api_info():
    """Returns JSON application metadata using Application Context."""
    return jsonify({
        "app_name": current_app.config['APPLICATION_NAME'],
        "root_path": current_app.root_path,
        "static_folder": current_app.static_folder,
        "template_folder": current_app.template_folder,
        "debug_mode": current_app.debug
    }), 200

@app.route('/api/environ')
def api_environ():
    """Inspects incoming HTTP Request details from Request Context."""
    return jsonify({
        "method": request.method,
        "path": request.path,
        "remote_addr": request.remote_addr,
        "user_agent": request.user_agent.string,
        "is_json": request.is_json,
        "query_params": request.args.to_dict()
    }), 200

@app.route('/health')
def health_check():
    """Health check status endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Flask Day 01 Masterclass",
        "version": "3.0.0"
    }), 200


# ------------------------------------------------------------------------------
# 4. Main Entrypoint
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 01 Flask WSGI Application...")
    print(f"Root Directory Path: {app.root_path}")
    print("Access endpoints at http://127.0.0.1:5000/")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
