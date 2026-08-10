"""
===============================================================================
Day 20 Practice Script: CORS Header Hardening & API Rate Limiting
===============================================================================
This script demonstrates:
1. Hardening Cross-Origin Resource Sharing (`Flask-CORS`) headers.
2. Protecting endpoints against DoS & brute-force attacks (`Flask-Limiter`).
3. Configuring custom rate limits (`@limiter.limit("3 per minute")`).
4. Designing custom rate limit key functions (API Key or IP address).
5. Customizing HTTP 429 Too Many Requests JSON error responses.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Protected API with Flask-CORS and Rate Limits.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day20-cors-limiter-secret'

# =============================================================================
# 1. Flask-CORS Configuration
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
# 2. Custom Key Function & Flask-Limiter Setup
# =============================================================================
def custom_api_key_or_ip():
    """Custom key function tracking X-API-KEY header or falling back to IP."""
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
# 3. Custom HTTP 429 Error Handler
# =============================================================================
@app.errorhandler(429)
def ratelimit_handler(e):
    """Returns standardized JSON payload when rate limit is exceeded."""
    return jsonify({
        "error": {
            "code": 429,
            "type": "TOO_MANY_REQUESTS",
            "message": "Rate limit exceeded. Please slow down your API requests.",
            "details": str(e.description)
        }
    }), 429


# =============================================================================
# 4. API Endpoints
# =============================================================================

# GET /api/v1/public (Uses default limit: 10 per minute)
@app.route('/api/v1/public', methods=['GET'])
def public_endpoint():
    return jsonify({
        "status": "success",
        "message": "Access granted to public API endpoint",
        "allowed_rate": "10 requests per minute"
    }), 200


# POST /api/v1/strict-login (Strict limit: 3 per minute)
@app.route('/api/v1/strict-login', methods=['POST'])
@limiter.limit("3 per minute")  # Prevents brute-force password guessing!
def strict_login():
    data = request.get_json() or {}
    username = data.get('username', 'guest')
    return jsonify({
        "status": "success",
        "message": f"Login attempt processed for '{username}'. (Strict limit: 3 req/min)"
    }), 200


# GET /api/v1/custom-limit (Tier-based limit)
@app.route('/api/v1/custom-limit', methods=['GET'])
@limiter.limit("5 per minute")
def custom_limit_endpoint():
    return jsonify({
        "status": "success",
        "message": "Access granted to custom API-Key endpoint (Limit: 5 req/min)"
    }), 200


# GET /api/v1/health (Exempt from rate limits)
@app.route('/api/v1/health', methods=['GET'])
@limiter.exempt
def health_check():
    return jsonify({"status": "healthy", "rate_limiting": "exempt"}), 200


# =============================================================================
# 5. Interactive Web UI Tester Dashboard
# =============================================================================
@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Day 20 CORS & Rate Limiter</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 40px; color: #333; }
                .card { max-width: 750px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
                h2 { color: #2c3e50; margin-top: 0; }
                .badge { background: #16a085; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 10px; border-bottom: 1px solid #e9ecef; text-align: left; }
                th { background: #34495e; color: white; }
                code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; color: #c7254e; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>🛡️ CORS Header Hardening & Rate Limiting (Day 20)</h2>
                <p>Security Extensions Active: <span class="badge">Flask-CORS + Flask-Limiter</span></p>

                <h3>API Endpoints Protection Matrix:</h3>
                <table>
                    <thead><tr><th>Endpoint Path</th><th>Verb</th><th>Rate Limit</th><th>Description</th></tr></thead>
                    <tbody>
                        <tr><td><code>/api/v1/public</code></td><td><code>GET</code></td><td>10 / min</td><td>Public endpoint with default IP rate limit</td></tr>
                        <tr><td><code>/api/v1/strict-login</code></td><td><code>POST</code></td><td>3 / min</td><td>Strict endpoint preventing brute-force logins</td></tr>
                        <tr><td><code>/api/v1/custom-limit</code></td><td><code>GET</code></td><td>5 / min</td><td>Tracks <code>X-API-KEY</code> header or IP address</td></tr>
                        <tr><td><code>/api/v1/health</code></td><td><code>GET</code></td><td>Exempt</td><td>Health check endpoint bypassing rate limit</td></tr>
                    </tbody>
                </table>

                <p style="margin-top: 25px;">
                    <a href="/api/v1/public">Test GET /api/v1/public (Click 11x rapidly to trigger 429 error!)</a>
                </p>
            </div>
        </body>
        </html>
    """)


# =============================================================================
# 6. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 20 CORS & Rate Limiter Protection Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("🛡️ Public Endpoint at: http://127.0.0.1:5000/api/v1/public")
    print("🔒 Strict Login Endpoint at: http://127.0.0.1:5000/api/v1/strict-login")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
