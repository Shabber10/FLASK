"""
===============================================================================
Day 03 Practice Script: Context Locals, Request Lifecycle & Hooks
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Understanding `g` (The Request Backpack) - Storing temporary request data.
2. STEP 2: Request timing & short-circuiting with `@app.before_request`.
3. STEP 3: Modifying outgoing HTTP responses with `@app.after_request`.
4. STEP 4: Guaranteed resource cleanup with `@app.teardown_request`.
5. STEP 5: Injecting global variables into templates with `@app.context_processor`.
6. STEP 6: Standalone context pushing (`app.app_context()`, `app.test_request_context()`).
7. STEP 7 (ADVANCED - OPTIONAL): Mock Database connection driver pattern.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Context Hooks and Request Timing Middleware.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import time
from datetime import datetime
from flask import Flask, g, request, jsonify, render_template_string, current_app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day03-pure-basics-key'
app.config['SITE_NAME'] = 'Enterprise Flask Platform'


# =============================================================================
# STEP 1: Understanding `g` (The Request Backpack) & Basic Routes
# =============================================================================

@app.route('/')
def home():
    """
    Step 1: Basic Route accessing `g` data initialized by hooks.
    """
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ platform_name }}</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f8f9fa; color: #333; }
            .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
            a { color: #0d6efd; font-weight: bold; text-decoration: none; }
            code { background: #e9ecef; padding: 2px 6px; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 Welcome to {{ platform_name }}</h1>
            <p>Server Time: <strong>{{ server_time }}</strong></p>
            <p>Current Request ID (from <code>g</code>): <code>{{ request_id }}</code></p>
            <ul>
                <li><a href="/api/status">Inspect Request Context API (<code>/api/status</code>)</a></li>
                <li><a href="/admin/dashboard">Protected Admin Route Test (<code>/admin/dashboard</code>)</a></li>
                <li><a href="/trigger-error">Test Teardown Exception Cleanup (<code>/trigger-error</code>)</a></li>
            </ul>
        </div>
        <footer>&copy; {{ current_year }} {{ platform_name }}</footer>
    </body>
    </html>
    """
    req_id = getattr(g, 'request_id', 'UNKNOWN')
    return render_template_string(html_template, request_id=req_id)


# =============================================================================
# STEP 2: `@app.before_request` (Timing & Short-Circuiting Auth Check)
# =============================================================================

@app.before_request
def setup_request_and_security():
    """
    Executes BEFORE every request view function:
    1. Records start timestamp on `g`.
    2. Generates a unique request ID on `g`.
    3. Short-circuits unauthorized access to /admin routes.
    """
    g.start_time = time.time()
    g.request_id = f"REQ-{int(g.start_time * 1000)}"
    print(f"--> [HOOK: before_request] {request.method} {request.path} | ID: {g.request_id}")

    # Short-Circuiting Security Check:
    if request.path.startswith('/admin'):
        auth_header = request.headers.get('Authorization')
        if auth_header != 'Bearer secret-admin-key':
            print("🛑 [SECURITY] Access denied! Short-circuiting request.")
            return jsonify({
                "error": "Unauthorized",
                "message": "Missing or invalid admin authorization header."
            }), 401


@app.route('/admin/dashboard')
def admin_dashboard():
    """
    Protected route: Only runs if before_request does NOT short-circuit!
    """
    return jsonify({"status": "access_granted", "dashboard": "Secret Admin Control Panel"}), 200


# =============================================================================
# STEP 3: `@app.after_request` (Modifying Outgoing Responses)
# =============================================================================

@app.after_request
def audit_and_add_headers(response):
    """
    Executes AFTER view function finishes:
    Calculates execution duration and attaches security/audit headers.
    """
    if hasattr(g, 'start_time'):
        duration_ms = round((time.time() - g.start_time) * 1000, 2)
        response.headers['X-Request-Duration-MS'] = str(duration_ms)
        response.headers['X-Request-ID'] = getattr(g, 'request_id', 'N/A')
        print(f"<-- [HOOK: after_request] Status: {response.status} | Latency: {duration_ms}ms")
    return response


# =============================================================================
# STEP 4: `@app.teardown_request` (Guaranteed Resource Cleanup)
# =============================================================================

@app.teardown_request
def cleanup_resources(exception=None):
    """
    Guaranteed execution AFTER response is sent (runs even if app crashes!).
    """
    if exception:
        print(f"⚠️ [HOOK: teardown_request] Request failed with exception: {exception}")
    print("--- [HOOK: teardown_request] Request context teardown complete.\n")


@app.route('/trigger-error')
def trigger_error():
    """
    Demonstrates teardown_request executing even when an unhandled error occurs!
    """
    raise ValueError("Simulated unexpected application error!")


# =============================================================================
# STEP 5: `@app.context_processor` (Global Template Injection)
# =============================================================================

@app.context_processor
def inject_global_template_vars():
    """
    Injects variables automatically into ALL Jinja2 templates across the app.
    """
    return {
        'platform_name': current_app.config['SITE_NAME'],
        'current_year': datetime.now().year,
        'server_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


@app.route('/api/status')
def status_api():
    """
    Step 5 API Route returning status data.
    """
    return jsonify({
        "status": "online",
        "request_id": getattr(g, 'request_id', 'N/A')
    }), 200


# =============================================================================
# STEP 6: Standalone Context Pushing Demo (`app_context` & `test_request_context`)
# =============================================================================

def run_context_push_demo():
    print("=" * 75)
    print("Testing Standalone Context Pushing in Scripts...")
    
    # 1. Pushing Application Context manually (for background scripts/CLI)
    with app.app_context():
        print(f"✅ Manually Pushed App Context: {current_app.config['SITE_NAME']}")
        
    # 2. Pushing Request Context manually (for unit tests)
    with app.test_request_context('/api/status?format=json'):
        print(f"✅ Manually Pushed Request Context: {request.path} | Query: {request.args.to_dict()}")
    print("=" * 75)


# =============================================================================
# STEP 7 (OPTIONAL / ADVANCED): Mock Database Connection Driver
# =============================================================================
# NOTE FOR BEGINNERS: Real database integration with SQLAlchemy will be covered in Day 06!

class MockDatabaseConnection:
    def __init__(self):
        self.connected_at = time.time()
        print(f"🔌 [DB ENGINE] Connection opened at {self.connected_at}")

    def close(self):
        print("🔒 [DB ENGINE] Connection closed safely.")


# =============================================================================
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    # Run context push demo first
    run_context_push_demo()

    print("🚀 Starting Day 03 Pure Basics Flask Application...")
    print("🌐 Open browser at: http://127.0.0.1:5000/")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
