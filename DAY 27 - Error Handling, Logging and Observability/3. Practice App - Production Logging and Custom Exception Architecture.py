"""
===============================================================================
Day 27 Practice Script: Production Logging & Custom Exception Architecture
===============================================================================
This script demonstrates:
1. Setting up structured logging with Python's `dictConfig`.
2. Injecting `X-Request-ID` Correlation IDs via middleware.
3. Defining a custom domain exception hierarchy (`BaseAPIException`).
4. Centralizing error handlers (`@app.errorhandler`) for 404, 422, and 500 errors.
5. Hiding raw stack tracebacks from end users while capturing them in logs (`exc_info=True`).
6. Interactive Web UI Log & Exception Monitoring Console.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Production Logging and Custom Exception Architecture.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import logging
import json
import uuid
import datetime
from flask import Flask, jsonify, request, g, render_template_string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day27-logging-masterclass-secret'

# Global in-memory log buffer for interactive UI dashboard console
log_records_buffer = []


# =============================================================================
# 1. Custom JSON Log Formatter & dictConfig Setup
# =============================================================================
class JSONLogFormatter(logging.Formatter):
    """Custom Formatter formatting log entries into structured JSON objects."""
    def format(self, record):
        log_obj = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": getattr(g, 'correlation_id', 'N/A')
        }
        if record.exc_info:
            log_obj["exception_type"] = record.exc_info[0].__name__
            log_obj["exception_detail"] = str(record.exc_info[1])

        formatted_json = json.dumps(log_obj)
        log_records_buffer.append(formatted_json)
        if len(log_records_buffer) > 30:
            log_records_buffer.pop(0)
        return formatted_json


# Configure Root Logger
handler = logging.StreamHandler()
handler.setFormatter(JSONLogFormatter())
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)


# =============================================================================
# 2. Correlation ID Middleware (`X-Request-ID`)
# =============================================================================
@app.before_request
def assign_correlation_id():
    """Assigns or extracts a unique X-Request-ID correlation UUID for request tracing."""
    correlation_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())
    g.correlation_id = correlation_id


@app.after_request
def inject_correlation_header(response):
    """Passes X-Request-ID correlation UUID back in response headers."""
    if hasattr(g, 'correlation_id'):
        response.headers['X-Request-ID'] = g.correlation_id
    return response


# =============================================================================
# 3. Custom Domain Exception Hierarchy
# =============================================================================
class BaseAPIException(Exception):
    """Base exception class for custom domain errors."""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}


class ResourceNotFoundException(BaseAPIException):
    def __init__(self, resource_name, resource_id):
        super().__init__(
            message=f"{resource_name} with ID #{resource_id} was not found.",
            status_code=404
        )


class ValidationException(BaseAPIException):
    def __init__(self, errors):
        super().__init__(
            message="Request validation failed.",
            status_code=422,
            payload={"validation_errors": errors}
        )


# =============================================================================
# 4. Centralized Error Handlers (@app.errorhandler)
# =============================================================================

# Catch Custom Domain Exceptions
@app.errorhandler(BaseAPIException)
def handle_custom_api_exception(error):
    app.logger.warning(f"Domain Exception [{error.status_code}]: {error.message}")
    return jsonify({
        "error": {
            "code": error.status_code,
            "message": error.message,
            "details": error.payload,
            "correlation_id": getattr(g, 'correlation_id', None)
        }
    }), error.status_code


# Catch Standard HTTP 404 Not Found
@app.errorhandler(404)
def handle_404(error):
    app.logger.warning(f"Route Not Found: {request.path}")
    return jsonify({
        "error": {
            "code": 404,
            "type": "NOT_FOUND",
            "message": f"URL path '{request.path}' was not found on this server.",
            "correlation_id": getattr(g, 'correlation_id', None)
        }
    }), 404


# Catch Unhandled 500 Crashes (Hides traceback from client; logs to server!)
@app.errorhandler(Exception)
def handle_unhandled_crash(error):
    # Log full stack trace to server logs
    app.logger.error(f"Unhandled Exception: {str(error)}", exc_info=True)

    # Return clean generic JSON (DO NOT expose raw traceback!)
    return jsonify({
        "error": {
            "code": 500,
            "type": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected internal server error occurred. Our engineering team has been notified.",
            "correlation_id": getattr(g, 'correlation_id', None)
        }
    }), 500


# =============================================================================
# 5. REST API Endpoints
# =============================================================================

users_db = {1: {"id": 1, "name": "Shabber Hussain", "role": "Instructor"}}


# GET /api/v1/users/<int:user_id> -> Returns User or raises ResourceNotFoundException
@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    app.logger.info(f"Fetching user record #{user_id}")
    if user_id not in users_db:
        raise ResourceNotFoundException("User", user_id)
    return jsonify({"status": "success", "data": users_db[user_id]}), 200


# POST /api/v1/orders -> Validates input or raises ValidationException
@app.route('/api/v1/orders', methods=['POST'])
def create_order():
    data = request.get_json() or {}
    errors = []

    if not data.get('item_name'):
        errors.append("Field 'item_name' is required.")
    if not data.get('quantity') or data.get('quantity', 0) <= 0:
        errors.append("Field 'quantity' must be a positive integer.")

    if errors:
        raise ValidationException(errors)

    app.logger.info(f"Order created: {data.get('item_name')} (Qty: {data.get('quantity')})")
    return jsonify({"status": "success", "message": "Order created successfully"}), 201


# GET /api/v1/cause-crash -> Triggers unhandled ZeroDivisionError
@app.route('/api/v1/cause-crash', methods=['GET'])
def cause_crash():
    app.logger.info("Attempting division by zero to simulate unhandled crash...")
    result = 10 / 0  # Triggers ZeroDivisionError!
    return jsonify({"result": result})


# GET /api/v1/logs -> Fetches live log buffer
@app.route('/api/v1/logs', methods=['GET'])
def get_logs():
    return jsonify({"status": "success", "logs": log_records_buffer}), 200


# =============================================================================
# 6. Interactive Web UI Log & Exception Monitoring Console
# =============================================================================
@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Day 27 Logging & Observability</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 40px; color: #333; }
                .card { max-width: 850px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
                h2 { color: #2c3e50; margin-top: 0; }
                .badge { background: #2980b9; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; }
                .btn { display: inline-block; background: #27ae60; color: white; padding: 8px 14px; text-decoration: none; border-radius: 4px; font-weight: bold; margin-right: 8px; border: none; cursor: pointer; }
                .btn-danger { background: #c0392b; }
                .btn-warning { background: #d35400; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 10px; border-bottom: 1px solid #e9ecef; text-align: left; }
                th { background: #34495e; color: white; }
                code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; color: #c7254e; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>📊 Production Logging, Correlation IDs & Observability (Day 27)</h2>
                <p>Telemetry Status: <span class="badge">Structured JSON Logs & Correlation Middleware Active</span></p>

                <h3>Test Exception Triggers:</h3>
                <p>
                    <button class="btn" onclick="testEndpoint('/api/v1/users/1')">🟢 Fetch User #1 (HTTP 200)</button>
                    <button class="btn btn-warning" onclick="testEndpoint('/api/v1/users/999')">🟡 Trigger 404 ResourceNotFound</button>
                    <button class="btn btn-warning" onclick="testPostOrder()">🟡 Trigger 422 ValidationException</button>
                    <button class="btn btn-danger" onclick="testEndpoint('/api/v1/cause-crash')">🔴 Trigger 500 Unhandled Crash</button>
                </p>

                <h3>Live Structured JSON Log Console:</h3>
                <div id="logs" style="background: #1e1e1e; color: #00ff00; padding: 15px; border-radius: 5px; font-family: monospace; height: 180px; overflow-y: auto;">
                    Loading logs...
                </div>

                <script>
                    function testEndpoint(url) {
                        fetch(url).then(r => r.json()).then(() => refreshLogs());
                    }

                    function testPostOrder() {
                        fetch('/api/v1/orders', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ item_name: "" })
                        }).then(r => r.json()).then(() => refreshLogs());
                    }

                    function refreshLogs() {
                        fetch('/api/v1/logs')
                        .then(r => r.json())
                        .then(data => {
                            const logsDiv = document.getElementById('logs');
                            logsDiv.innerHTML = data.logs.join('<br>') || 'Waiting for log events...';
                            logsDiv.scrollTop = logsDiv.scrollHeight;
                        });
                    }

                    setInterval(refreshLogs, 2000);
                    refreshLogs();
                </script>
            </div>
        </body>
        </html>
    """)


# =============================================================================
# 7. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 27 Production Logging Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("📊 Live JSON Logs at: http://127.0.0.1:5000/api/v1/logs")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
