"""
Day 03 Practice Application: Context Hooks & Request Timing Middleware
=======================================================================
This application demonstrates:
1. Managing database connections & request-scoped data on `g`.
2. Tracking HTTP request latency via `@app.before_request` and `@app.after_request`.
3. Ensuring resource cleanup with `@app.teardown_request`.
4. Injecting global variables into Jinja2 templates via `@app.context_processor`.
5. Manually pushing application & request contexts in standalone scripts.
"""

import time
from datetime import datetime
from flask import Flask, g, request, jsonify, render_template_string, current_app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day03-lifecycle-secret'
app.config['SITE_NAME'] = 'Enterprise Flask Platform'


# ------------------------------------------------------------------------------
# 1. Simulated Database Connection Class
# ------------------------------------------------------------------------------
class MockDatabaseConnection:
    def __init__(self):
        self.connected_at = time.time()
        self.is_closed = False
        print(f"[DB ENGINE] Database Connection Opened at {self.connected_at}")

    def query(self, sql):
        if self.is_closed:
            raise RuntimeError("Cannot query on a closed database connection!")
        return f"Query Result for '{sql}'"

    def close(self):
        self.is_closed = True
        print("[DB ENGINE] Database Connection Closed Safely.")


# ------------------------------------------------------------------------------
# 2. Lifecycle Hooks
# ------------------------------------------------------------------------------
@app.before_request
def setup_request():
    """Executes before every request: starts timer & initializes DB connection on g."""
    g.start_time = time.time()
    g.db = MockDatabaseConnection()
    g.request_id = f"REQ-{int(g.start_time * 1000)}"
    print(f"--> [HOOK: before_request] {request.method} {request.path} | Request ID: {g.request_id}")

@app.after_request
def audit_response(response):
    """Executes after view returns: injects response headers and logs timing."""
    if hasattr(g, 'start_time'):
        latency = round((time.time() - g.start_time) * 1000, 2)
        response.headers['X-Request-Duration-MS'] = str(latency)
        response.headers['X-Request-ID'] = getattr(g, 'request_id', 'N/A')
        print(f"<-- [HOOK: after_request] Status: {response.status} | Latency: {latency}ms")
    return response

@app.teardown_request
def teardown_resources(exception=None):
    """Guaranteed execution after request: cleans up DB connection on g."""
    if exception:
        print(f"!!! [HOOK: teardown_request] Request raised Exception: {exception}")
    
    db = g.pop('db', None)
    if db is not None:
        db.close()
    print("--- [HOOK: teardown_request] Context Tear Down Completed.")


# ------------------------------------------------------------------------------
# 3. Context Processor
# ------------------------------------------------------------------------------
@app.context_processor
def inject_global_vars():
    """Injects site metadata into all rendered templates."""
    return {
        'platform_name': current_app.config['SITE_NAME'],
        'current_year': datetime.now().year,
        'server_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


# ------------------------------------------------------------------------------
# 4. View Functions
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    """HTML View using context processor variables."""
    html_template = """
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Welcome to {{ platform_name }}</h1>
        <p>Current Server Time: <strong>{{ server_time }}</strong></p>
        <p>Database Query Test: {{ db_result }}</p>
        <footer>&copy; {{ current_year }} {{ platform_name }}</footer>
    </body>
    </html>
    """
    res = g.db.query("SELECT * FROM users")
    return render_template_string(html_template, db_result=res)

@app.route('/api/status')
def status_api():
    """API Endpoint demonstrating g data inspection."""
    return jsonify({
        "status": "online",
        "request_id": g.request_id,
        "db_connected_at": g.db.connected_at
    })

@app.route('/trigger-error')
def trigger_error():
    """Endpoint demonstrating teardown execution during unhandled errors."""
    raise ValueError("Simulated unexpected application error!")


# ------------------------------------------------------------------------------
# 5. Main Entrypoint & Context Manual Push Demo
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    print("=" * 70)
    print("Testing Manual Context Pushing in Standalone Python Code...")
    
    # 1. Manually Pushing Application Context
    with app.app_context():
        print(f"Manually Pushed App Context: {current_app.config['SITE_NAME']}")
        
    # 2. Manually Pushing Request Context
    with app.test_request_context('/api/status?format=json'):
        print(f"Manually Pushed Request Context: {request.path} | Query: {request.args}")
        
    print("=" * 70)
    print("Starting Day 03 Practice Application...")
    print("Test endpoints at http://127.0.0.1:5000/")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
