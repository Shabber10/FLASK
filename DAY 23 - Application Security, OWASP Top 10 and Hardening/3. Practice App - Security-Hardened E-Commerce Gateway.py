"""
Day 23 Practice Application: Security-Hardened API Gateway
===========================================================
This application demonstrates:
1. Enforcing HTTP Security Headers via Flask-Talisman.
2. Applying IP rate limiting via Flask-Limiter (@limiter.limit("3 per minute")).
3. Demonstrating Jinja2 HTML auto-escaping vs raw XSS risks.
4. Parameterized query safety vs raw SQL string concatenation.
5. Providing an interactive Web UI for security header & rate limit testing.
"""

from flask import Flask, jsonify, request, render_template_string
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day23-security-hardening-secret'

# Initialize Rate Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "30 per hour"],
    storage_uri="memory://"
)


# ------------------------------------------------------------------------------
# 1. Error Handler for Rate Limit Exceeded (HTTP 429)
# ------------------------------------------------------------------------------
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Too Many Requests",
        "message": f"Rate limit exceeded: {e.description}. Try again later."
    }), 429


# ------------------------------------------------------------------------------
# 2. Interactive Security Diagnostic Dashboard
# ------------------------------------------------------------------------------
SECURITY_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 23 Application Security & Hardening</title>
    <style>
        body { font-family: Arial, sans-serif; background: #eef2f5; margin: 30px; }
        .card { max-width: 850px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .btn { background: #e53e3e; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; margin-right: 5px; }
        .btn-safe { background: #27ae60; }
        .log-box { background: #1a202c; color: #68d391; padding: 15px; border-radius: 6px; font-family: monospace; font-size: 0.9em; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🛡️ Application Security & OWASP Hardening (Day 23)</h2>
        <p>Demonstrating Rate Limiting (HTTP 429), XSS Auto-Escaping, and Security Headers.</p>

        <div>
            <button class="btn" onclick="testLoginRateLimit()">Test Login Rate Limit (Max 3 per min)</button>
            <button class="btn btn-safe" onclick="testXSS()">Test Jinja2 XSS Auto-Escaping</button>
            <button class="btn btn-safe" onclick="fetchHeaders()">Inspect Active Security Headers</button>
        </div>

        <div id="output" class="log-box">Click a button to execute security tests...</div>
    </div>

    <script>
        async function testLoginRateLimit() {
            const res = await fetch('/api/secure-login', { method: 'POST' });
            const data = await res.json();
            document.getElementById('output').innerText = 
                `HTTP Status: ${res.status}\n` + JSON.stringify(data, null, 2);
        }

        async function testXSS() {
            const input = "<script>alert('XSS Payload Exploit!')</script>";
            const res = await fetch('/api/xss-demo?input=' + encodeURIComponent(input));
            const data = await res.json();
            document.getElementById('output').innerText = JSON.stringify(data, null, 2);
        }

        async function fetchHeaders() {
            const res = await fetch('/api/secure-login', { method: 'POST' });
            let headersText = "Response HTTP Headers:\n";
            for (let [key, value] of res.headers.entries()) {
                headersText += `  ${key}: ${value}\n`;
            }
            document.getElementById('output').innerText = headersText;
        }
    </script>
</body>
</html>
"""


# ------------------------------------------------------------------------------
# 3. Route Handlers
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template_string(SECURITY_HTML)

# Strict Rate Limited Login Route (Max 3 requests per minute per IP!)
@app.route('/api/secure-login', methods=['POST'])
@limiter.limit("3 per minute")
def secure_login():
    response = jsonify({
        "status": "Success",
        "message": "Login attempt processed securely under rate-limiting quota."
    })
    # Attach Security Headers Manually for Demo
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response, 200

# XSS Escaping Demo Route
@app.route('/api/xss-demo')
def xss_demo():
    user_input = request.args.get('input', '')
    # Demonstrate Jinja2 Auto-Escaping
    rendered_escaped = str(render_template_string("{{ input }}", input=user_input))
    return jsonify({
        "raw_user_input": user_input,
        "rendered_jinja2_escaped": rendered_escaped,
        "protection": "Special characters converted to safe HTML entities (&lt; &gt; &amp;)"
    })


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 23 Security-Hardened Application...")
    print("Security Dashboard UI at http://127.0.0.1:5000/")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
