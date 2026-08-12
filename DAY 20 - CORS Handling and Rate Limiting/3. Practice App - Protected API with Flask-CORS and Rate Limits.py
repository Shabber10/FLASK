"""
===============================================================================
Day 20 Practice Script: CORS Header Hardening & API Rate Limiting
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Hardening Cross-Origin Resource Sharing (`Flask-CORS`) headers.
2. STEP 2: Designing custom rate limit key function (`custom_api_key_or_ip`) & initializing `Flask-Limiter`.
3. STEP 3: Authoring custom HTTP 429 Too Many Requests JSON error handler (`ratelimit_handler`).
4. STEP 4: Public API Endpoint (`GET /api/v1/public`) using default IP rate limits.
5. STEP 5: Strict Endpoint (`POST /api/v1/strict-login`), Custom API-Key limit, and Exempt Endpoint (`GET /api/v1/health`).
6. STEP 6: Interactive Web UI tester dashboard rendering `templates/index.html`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Protected API with Flask-CORS and Rate Limits.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day20-cors-limiter-secret'

# =============================================================================
# STEP 1: Enterprise Flask-CORS Configuration
# =============================================================================
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:5000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-API-KEY"],
        "supports_credentials": True,
        "max_age": 600
    }
})


# =============================================================================
# STEP 2: Custom Key Function & Flask-Limiter Setup
# =============================================================================
def custom_api_key_or_ip():
    """Step 2a: Custom key function tracking X-API-KEY header or falling back to IP."""
    api_key = request.headers.get("X-API-KEY")
    if api_key:
        return f"api_key:{api_key}"
    return get_remote_address()


limiter = Limiter(
    key_func=custom_api_key_or_ip,
    app=app,
    default_limits=["100 per day", "10 per minute"]
)


# =============================================================================
# STEP 3: Custom HTTP 429 Error Handler
# =============================================================================
@app.errorhandler(429)
def ratelimit_handler(e):
    """Step 3: Returns standardized JSON payload when rate limit is exceeded."""
    return jsonify({
        "error": {
            "code": 429,
            "type": "TOO_MANY_REQUESTS",
            "message": "Rate limit exceeded. Please slow down your API requests.",
            "details": str(e.description)
        }
    }), 429


# =============================================================================
# STEP 4 & 5: Protected API Endpoints (Public, Strict, Custom, Exempt)
# =============================================================================

# GET /api/v1/public (Uses default limit: 10 per minute)
@app.route('/api/v1/public', methods=['GET'])
def public_endpoint():
    """Step 4: Public endpoint using default 10 req/min rate limit."""
    return jsonify({
        "status": "success",
        "message": "Access granted to public API endpoint",
        "allowed_rate": "10 requests per minute"
    }), 200


# POST /api/v1/strict-login (Strict limit: 3 per minute)
@app.route('/api/v1/strict-login', methods=['POST'])
@limiter.limit("3 per minute")  # Prevents brute-force password guessing!
def strict_login():
    """Step 5a: Strict endpoint preventing brute-force logins."""
    data = request.get_json() or {}
    username = data.get('username', 'guest')
    return jsonify({
        "status": "success",
        "message": f"Login attempt processed for '{username}'. (Strict limit: 3 req/min)"
    }), 200


# GET /api/v1/custom-limit (Custom API-Key limit)
@app.route('/api/v1/custom-limit', methods=['GET'])
@limiter.limit("5 per minute")
def custom_limit_endpoint():
    """Step 5b: Custom endpoint tracking X-API-KEY header."""
    return jsonify({
        "status": "success",
        "message": "Access granted to custom API-Key endpoint (Limit: 5 req/min)"
    }), 200


# GET /api/v1/health (Exempt from rate limits)
@app.route('/api/v1/health', methods=['GET'])
@limiter.exempt
def health_check():
    """Step 5c: Health check endpoint completely exempt from rate limits."""
    return jsonify({"status": "healthy", "rate_limiting": "exempt"}), 200


# =============================================================================
# STEP 6: Interactive Web UI Tester Dashboard Route Handler (render_template)
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
    print("🚀 Starting Day 20 CORS & Rate Limiter Protection Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("🛡️ Public Endpoint at: http://127.0.0.1:5000/api/v1/public")
    print("🔒 Strict Login Endpoint at: http://127.0.0.1:5000/api/v1/strict-login")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
