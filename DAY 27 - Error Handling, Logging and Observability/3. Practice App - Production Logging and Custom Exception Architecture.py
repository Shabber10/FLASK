"""
===============================================================================
Day 27 Practice Script: Production Logging & Custom Exception Architecture
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Setting up structured logging with Python's `dictConfig` and custom JSON formatter.
2. STEP 2: Injecting `X-Request-ID` Correlation IDs via middleware.
3. STEP 3: Defining a custom domain exception hierarchy (`BaseAPIException`).
4. STEP 4: Centralizing error handlers (`@app.errorhandler`) for 404, 422, and 500 errors with `exc_info=True`.
5. STEP 5: REST API Endpoints triggering domain exceptions and unhandled crashes.
6. STEP 6: Interactive Web UI Log & Exception Monitoring Console rendering `templates/index.html`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Production Logging and Custom Exception Architecture.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import logging
import json
import uuid
import datetime
from flask import Flask, jsonify, request, g, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day27-logging-masterclass-secret'

# Global in-memory log buffer for interactive UI dashboard console
log_records_buffer = []


# =============================================================================
# STEP 1: Custom JSON Log Formatter & Logger Setup
# =============================================================================
class JSONLogFormatter(logging.Formatter):
    """Step 1a: Custom Formatter formatting log entries into structured JSON objects."""
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


# Step 1b: Configure Root Logger
handler = logging.StreamHandler()
handler.setFormatter(JSONLogFormatter())
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)


# =============================================================================
# STEP 2: Correlation ID Middleware (`X-Request-ID`)
# =============================================================================
@app.before_request
def assign_correlation_id():
    """Step 2a: Assigns or extracts a unique X-Request-ID correlation UUID for request tracing."""
    correlation_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())
    g.correlation_id = correlation_id


@app.after_request
def inject_correlation_header(response):
    """Step 2b: Passes X-Request-ID correlation UUID back in response headers."""
    if hasattr(g, 'correlation_id'):
        response.headers['X-Request-ID'] = g.correlation_id
    return response


# =============================================================================
# STEP 3: Custom Domain Exception Hierarchy
# =============================================================================
class BaseAPIException(Exception):
    """Step 3a: Base exception class for custom domain errors."""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}


class ResourceNotFoundException(BaseAPIException):
    """Step 3b: Raised when a database record is missing."""
    def __init__(self, resource_name, resource_id):
        super().__init__(
            message=f"{resource_name} with ID #{resource_id} was not found.",
            status_code=404
        )


class ValidationException(BaseAPIException):
    """Step 3c: Raised when payload validation fails."""
    def __init__(self, errors):
        super().__init__(
            message="Request validation failed.",
            status_code=422,
            payload={"validation_errors": errors}
        )


# =============================================================================
# STEP 4: Centralized Error Handlers (@app.errorhandler)
# =============================================================================

# Catch Custom Domain Exceptions
@app.errorhandler(BaseAPIException)
def handle_custom_api_exception(error):
    """Step 4a: Handles all custom domain exceptions cleanly."""
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
    """Step 4b: Handles 404 route not found errors."""
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
    """Step 4c: Captures unhandled 500 crashes with exc_info=True."""
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
# STEP 5: REST API Endpoints
# =============================================================================

users_db = {1: {"id": 1, "name": "Shabber Hussain", "role": "Instructor"}}


# GET /api/v1/users/<int:user_id> -> Returns User or raises ResourceNotFoundException
@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Step 5a: Endpoint triggering 200 OK or 404 ResourceNotFoundException."""
    app.logger.info(f"Fetching user record #{user_id}")
    if user_id not in users_db:
        raise ResourceNotFoundException("User", user_id)
    return jsonify({"status": "success", "data": users_db[user_id]}), 200


# POST /api/v1/orders -> Validates input or raises ValidationException
@app.route('/api/v1/orders', methods=['POST'])
def create_order():
    """Step 5b: Endpoint triggering 201 Created or 422 ValidationException."""
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
    """Step 5c: Endpoint triggering unhandled 500 ZeroDivisionError."""
    app.logger.info("Attempting division by zero to simulate unhandled crash...")
    result = 10 / 0  # Triggers ZeroDivisionError!
    return jsonify({"result": result})


# GET /api/v1/logs -> Fetches live log buffer
@app.route('/api/v1/logs', methods=['GET'])
def get_logs():
    """Step 5d: Returns structured JSON logs buffer."""
    return jsonify({"status": "success", "logs": log_records_buffer}), 200


# =============================================================================
# STEP 6: Interactive Web UI Dashboard Route Handler (render_template)
# =============================================================================
@app.route('/')
def home():
    """Step 6: Renders templates/index.html dashboard."""
    return render_template('index.html')


# =============================================================================
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 27 Production Logging Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("📊 Live JSON Logs at: http://127.0.0.1:5000/api/v1/logs")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
