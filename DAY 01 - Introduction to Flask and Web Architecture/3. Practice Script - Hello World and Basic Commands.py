"""
===============================================================================
Day 01 Practice Script: Zero-to-Hero Minimal Flask & WSGI Application
===============================================================================
This script is designed for absolute beginners to hands-on learners.

What this script demonstrates:
1. Creating a Flask application instance using `Flask(__name__)`.
2. Attaching custom WSGI middleware to measure request execution time.
3. Defining basic HTML routes, dynamic URL parameter routes, and JSON API routes.
4. Safely accessing Application Context (`current_app`) and Request Context (`request`).
5. Running the Werkzeug development server in debug mode.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice Script - Hello World and Basic Commands.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import os
import time
from flask import Flask, jsonify, request, current_app

# =============================================================================
# 1. Custom WSGI Middleware Layer
# =============================================================================
class ExecutionTimerMiddleware:
    """
    Custom WSGI Middleware that intercepts every incoming HTTP request,
    calculates how many milliseconds it took to execute, and adds a custom
    'X-WSGI-Response-Time' header to the outgoing HTTP response.
    """
    def __init__(self, wsgi_app):
        # Store reference to the original Flask WSGI application
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        # Record start timestamp when request enters WSGI layer
        start_time = time.time()

        def custom_start_response(status, headers, exc_info=None):
            # Calculate execution duration in milliseconds
            duration_ms = (time.time() - start_time) * 1000
            
            # Inject custom headers into response headers list
            headers.append(('X-WSGI-Response-Time', f"{duration_ms:.2f}ms"))
            headers.append(('X-Powered-By', 'Flask-3.x-Zero-to-Hero-Masterclass'))
            
            # Trigger the server's original start_response callback
            return start_response(status, headers, exc_info)

        # Execute the underlying Flask WSGI application
        return self.wsgi_app(environ, custom_start_response)


# =============================================================================
# 2. Flask Application Initialization
# =============================================================================
# Pass __name__ so Flask knows where this script lives on disk
app = Flask(__name__)

# Apply our custom WSGI Middleware to wrap Flask's core wsgi_app
app.wsgi_app = ExecutionTimerMiddleware(app.wsgi_app)

# Configure basic application settings
app.config['APPLICATION_NAME'] = 'Day 01 Zero-to-Hero Flask Masterclass'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'day01-beginner-secret-key')


# =============================================================================
# 3. Route Handlers (View Functions)
# =============================================================================

@app.route('/')
def home():
    """
    Route 1: Home Page (Root Endpoint '/')
    Returns a simple HTML web page welcoming the student.
    """
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Day 01 - Flask & WSGI Masterclass</title>
        <style>
            body { font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background-color: #f8f9fa; color: #333; }
            h1 { color: #0d6efd; }
            .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
            a { color: #0d6efd; text-decoration: none; font-weight: bold; }
            a:hover { text-decoration: underline; }
            code { background: #e9ecef; padding: 2px 6px; border-radius: 4px; font-family: monospace; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 Welcome to Day 01: Flask & WSGI Architecture</h1>
            <p>Congratulations! Your Flask web application is officially running!</p>
        </div>

        <div class="card">
            <h3>Explore Interactive Endpoints:</h3>
            <ul>
                <li><a href="/hello/Student">Dynamic Route: Greeting (<code>/hello/Student</code>)</a></li>
                <li><a href="/api/info">Application Context Info API (<code>/api/info</code>)</a></li>
                <li><a href="/api/environ">WSGI Request Context Metadata (<code>/api/environ?category=flask</code>)</a></li>
                <li><a href="/health">Health Check Endpoint (<code>/health</code>)</a></li>
            </ul>
        </div>
    </body>
    </html>
    """


@app.route('/hello/<name>')
def greet_user(name):
    """
    Route 2: Dynamic Route Parameter ('/hello/<name>')
    Demonstrates capturing variable values directly from the URL.
    """
    return f"""
    <div style="font-family: sans-serif; padding: 30px;">
        <h2>Hello, <span style="color: #198754;">{name}</span>! 👋</h2>
        <p>This page was generated dynamically by Python using URL routing parameters.</p>
        <p><a href="/">← Return to Home</a></p>
    </div>
    """


@app.route('/api/info')
def api_info():
    """
    Route 3: Application Context Endpoint ('/api/info')
    Uses `current_app` proxy to return application-level metadata as JSON.
    """
    return jsonify({
        "status": "success",
        "app_name": current_app.config['APPLICATION_NAME'],
        "root_path": current_app.root_path,
        "static_folder": current_app.static_folder,
        "template_folder": current_app.template_folder,
        "debug_mode": current_app.debug
    }), 200


@app.route('/api/environ')
def api_environ():
    """
    Route 4: Request Context Endpoint ('/api/environ')
    Uses `request` proxy to inspect incoming HTTP request details.
    """
    return jsonify({
        "status": "success",
        "http_method": request.method,
        "requested_path": request.path,
        "client_ip": request.remote_addr,
        "user_agent": request.user_agent.string,
        "query_parameters": request.args.to_dict()
    }), 200


@app.route('/health')
def health_check():
    """
    Route 5: Health Check Endpoint ('/health')
    Standard endpoint used by monitoring tools to check if service is alive.
    """
    return jsonify({
        "status": "healthy",
        "service": "Flask Day 01 Masterclass",
        "version": "1.0.0"
    }), 200


# =============================================================================
# 4. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 01 Flask WSGI Application...")
    print(f"📍 Root Path: {app.root_path}")
    print("🌐 Access application in browser at: http://127.0.0.1:5000/")
    print("=" * 75)
    
    # Launch Werkzeug development server on localhost:5000
    app.run(host='127.0.0.1', port=5000, debug=True)
