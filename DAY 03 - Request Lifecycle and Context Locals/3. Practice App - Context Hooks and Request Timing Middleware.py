"""
===============================================================================
Day 03 Practice Script: Context Hooks & Request Lifecycle Management
===============================================================================
This script demonstrates:
1. Managing in-memory request-scoped data and database connections on `g`.
2. Tracking HTTP request latency via `@app.before_request` and `@app.after_request`.
3. Ensuring guaranteed database cleanup with `@app.teardown_request`.
4. Injecting global variables into Jinja2 templates via `@app.context_processor`.
5. Manually pushing application & request contexts in standalone scripts.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Context Hooks and Request Timing Middleware.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import time
from datetime import datetime
from flask import Flask, g, request, jsonify, render_template_string, current_app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day03-lifecycle-secret'
app.config['SITE_NAME'] = 'Enterprise Flask Platform'


# =============================================================================
# 1. Simulated Database Connection Class
# =============================================================================
class MockDatabaseConnection:
    """Simulates a real database driver connection."""
    def __init__(self):
        self.connected_at = time.time()
        self.is_closed = False
        print(f"🔌 [DB ENGINE] Connection opened at {self.connected_at}")

    def query(self, sql):
        if self.is_closed:
            raise RuntimeError("Cannot query on a closed database connection!")
        return f"Results for query '{sql}'"

    def close(self):
        self.is_closed = True
        print("🔒 [DB ENGINE] Connection closed safely.")


# =============================================================================
# 2. Lifecycle Hooks
# =============================================================================
@app.before_request
def setup_request():
    """
    Executes BEFORE every request:
    1. Records request start time on g.
    2. Initializes a mock DB connection on g.
    3. Generates a unique request ID on g.
    """
    g.start_time = time.time()
    g.db = MockDatabaseConnection()
    g.request_id = f"REQ-{int(g.start_time * 1000)}"
    print(f"--> [HOOK: before_request] {request.method} {request.path} | ID: {g.request_id}")


@app.after_request
def audit_response(response):
    """
    Executes AFTER view function returns:
    Calculates execution duration and attaches audit headers to response.
    """
    if hasattr(g, 'start_time'):
        latency_ms = round((time.time() - g.start_time) * 1000, 2)
        response.headers['X-Request-Duration-MS'] = str(latency_ms)
        response.headers['X-Request-ID'] = getattr(g, 'request_id', 'N/A')
        print(f"<-- [HOOK: after_request] Status: {response.status} | Latency: {latency_ms}ms")
    return response


@app.teardown_request
def teardown_resources(exception=None):
    """
    Guaranteed execution AFTER request finishes:
    Safely closes the database connection stored on g (even if errors occurred).
    """
    if exception:
        print(f"⚠️ [HOOK: teardown_request] Request raised Exception: {exception}")
    
    db = g.pop('db', None)
    if db is not None:
        db.close()
    print("--- [HOOK: teardown_request] Context Tear Down Complete.\n")


# =============================================================================
# 3. Context Processor
# =============================================================================
@app.context_processor
def inject_global_vars():
    """Injects site metadata automatically into all Jinja2 templates."""
    return {
        'platform_name': current_app.config['SITE_NAME'],
        'current_year': datetime.now().year,
        'server_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


# =============================================================================
# 4. View Functions (Routes)
# =============================================================================
@app.route('/')
def index():
    """
    Route 1: HTML Home Page
    Renders Jinja2 template using global context processor variables and g.db.
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
            <p>Database Query Test: <code>{{ db_result }}</code></p>
            <ul>
                <li><a href="/api/status">Inspect Request Context Data (<code>/api/status</code>)</a></li>
                <li><a href="/trigger-error">Test Teardown Exception Cleanup (<code>/trigger-error</code>)</a></li>
            </ul>
        </div>
        <footer>&copy; {{ current_year }} {{ platform_name }}</footer>
    </body>
    </html>
    """
    query_data = g.db.query("SELECT * FROM active_users")
    return render_template_string(html_template, db_result=query_data)


@app.route('/api/status')
def status_api():
    """Route 2: API Endpoint returning g context data as JSON."""
    return jsonify({
        "status": "online",
        "request_id": g.request_id,
        "db_connected_at": g.db.connected_at
    }), 200


@app.route('/trigger-error')
def trigger_error():
    """Route 3: Error Endpoint demonstrating teardown execution during exceptions."""
    raise ValueError("Simulated unexpected application error!")


# =============================================================================
# 5. Main Entrypoint & Context Manual Push Demo
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("Testing Standalone Context Pushing in Scripts...")
    
    # 1. Manually Pushing Application Context
    with app.app_context():
        print(f"✅ Manually Pushed App Context: {current_app.config['SITE_NAME']}")
        
    # 2. Manually Pushing Request Context
    with app.test_request_context('/api/status?format=json'):
        print(f"✅ Manually Pushed Request Context: {request.path} | Query: {request.args}")
        
    print("=" * 75)
    print("🚀 Starting Day 03 Practice Application...")
    print("🌐 Open browser at: http://127.0.0.1:5000/")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
