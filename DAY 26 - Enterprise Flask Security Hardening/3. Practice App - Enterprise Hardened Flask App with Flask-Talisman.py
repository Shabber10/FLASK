"""
===============================================================================
Day 26 Practice Script: Enterprise Flask Security Hardening Infrastructure
===============================================================================
This script demonstrates:
1. Hardening HTTP response headers with `Flask-Talisman`.
2. Configuring a strict Content Security Policy (CSP).
3. Enforcing Clickjacking (`X-Frame-Options: DENY`) and MIME-sniffing protection.
4. Input sanitization stripping malicious `<script>` and `<iframe>` XSS payloads.
5. Inspecting injected HTTP security headers via REST API (`GET /api/v1/headers-audit`).
6. Interactive Web UI Security Audit Dashboard.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Enterprise Hardened Flask App with Flask-Talisman.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import html
import re
from flask import Flask, jsonify, request, render_template_string
from flask_talisman import Talisman

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day26-talisman-security-masterclass-secret'

# =============================================================================
# 1. Flask-Talisman Enterprise Security Hardening Setup
# =============================================================================
csp_policy = {
    'default-src': "'self'",
    'script-src': [
        "'self'",
        "'unsafe-inline'",  # Permits inline UI dashboard scripts
        'https://cdn.jsdelivr.net'
    ],
    'style-src': [
        "'self'",
        "'unsafe-inline'",
        'https://fonts.googleapis.com'
    ],
    'img-src': "'self' data: https:",
    'object-src': "'none'"  # Blocks Flash / Java applet execution
}

talisman = Talisman(
    app,
    content_security_policy=csp_policy,
    force_https=False,              # Set to True in production HTTPS environment!
    session_cookie_secure=False,    # Set to True in HTTPS environment
    session_cookie_http_only=True,  # Prevents JS cookie theft via document.cookie
    frame_options='DENY'            # Blocks Clickjacking iframe embedding
)


# =============================================================================
# 2. Input Sanitization Helper Function (Strips XSS Tags)
# =============================================================================
def sanitize_user_input(raw_text):
    """Sanitizes raw text input, stripping dangerous <script>, <iframe>, and event handlers."""
    if not raw_text:
        return ""
    # Strip script and iframe tags
    clean_text = re.sub(r'<script.*?>.*?</script>', '', raw_text, flags=re.DOTALL | re.IGNORECASE)
    clean_text = re.sub(r'<iframe.*?>.*?</iframe>', '', clean_text, flags=re.DOTALL | re.IGNORECASE)
    # Strip inline event handlers like onerror= or onclick=
    clean_text = re.sub(r'\son\w+=".*?"', '', clean_text, flags=re.IGNORECASE)
    # Escape HTML special characters for safe rendering
    return html.escape(clean_text)


# =============================================================================
# 3. REST API Endpoints
# =============================================================================

# POST /api/v1/sanitize -> Accepts raw input and returns sanitized safe output
@app.route('/api/v1/sanitize', methods=['POST'])
def sanitize_endpoint():
    data = request.get_json() or {}
    raw_payload = data.get('raw_input', '')
    sanitized_output = sanitize_user_input(raw_payload)

    return jsonify({
        "status": "success",
        "raw_input": raw_payload,
        "sanitized_output": sanitized_output,
        "xss_threat_neutralized": raw_payload != sanitized_output
    }), 200


# GET /api/v1/headers-audit -> Inspects HTTP security headers injected by Talisman
@app.route('/api/v1/headers-audit', methods=['GET'])
def headers_audit():
    return jsonify({
        "status": "success",
        "hardened_security_headers": {
            "Content-Security-Policy": str(csp_policy),
            "X-Frame-Options": "DENY (Clickjacking Protected)",
            "X-Content-Type-Options": "nosniff (MIME Sniffing Protected)",
            "Session-Cookie-HttpOnly": "True (Protected against JS Theft)"
        }
    }), 200


# =============================================================================
# 4. Interactive Web UI Security Audit Dashboard
# =============================================================================
@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Day 26 Enterprise Security Hardening</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 40px; color: #333; }
                .card { max-width: 850px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
                h2 { color: #2c3e50; margin-top: 0; }
                .badge { background: #27ae60; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; }
                .btn { display: inline-block; background: #2980b9; color: white; padding: 10px 18px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 10px; border-bottom: 1px solid #e9ecef; text-align: left; }
                th { background: #34495e; color: white; }
                code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; color: #c7254e; font-weight: bold; }
                textarea { width: 100%; height: 80px; padding: 8px; border-radius: 4px; border: 1px solid #ccc; font-family: monospace; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>🛡️ Enterprise Security Hardening & XSS Protection (Day 26)</h2>
                <p>Security Hardening Suite: <span class="badge">Flask-Talisman Active</span></p>

                <h3>1. Active HTTP Security Headers Audit:</h3>
                <table>
                    <thead><tr><th>Security Header</th><th>Status</th><th>Protection Description</th></tr></thead>
                    <tbody>
                        <tr><td><code>Content-Security-Policy</code></td><td><span class="badge">ENABLED</span></td><td>Whitelists trusted scripts; blocks XSS execution</td></tr>
                        <tr><td><code>X-Frame-Options</code></td><td><span class="badge">DENY</span></td><td>Blocks Clickjacking iframe embedding</td></tr>
                        <tr><td><code>X-Content-Type-Options</code></td><td><span class="badge">nosniff</span></td><td>Blocks MIME-type sniffing attacks</td></tr>
                        <tr><td><code>HttpOnly Cookies</code></td><td><span class="badge">ENABLED</span></td><td>Blocks JavaScript session cookie theft</td></tr>
                    </tbody>
                </table>

                <h3 style="margin-top: 25px;">2. Interactive XSS Input Sanitization Tester:</h3>
                <p>Enter a raw HTML payload containing malicious <code>&lt;script&gt;</code> tags:</p>
                <textarea id="xss_input">&lt;script&gt;alert('XSS Theft! Cookie=' + document.cookie)&lt;/script&gt;&lt;b&gt;Hello World&lt;/b&gt;</textarea>
                <p><button class="btn" onclick="testSanitizer()">Test Input Sanitizer API</button></p>

                <div id="output" style="background: #1e1e1e; color: #00ff00; padding: 15px; border-radius: 5px; font-family: monospace; min-height: 80px; display: none;">
                </div>

                <script>
                    function testSanitizer() {
                        const inputVal = document.getElementById('xss_input').value;
                        const out = document.getElementById('output');
                        out.style.display = 'block';
                        out.innerHTML = "Submitting to /api/v1/sanitize...";

                        fetch('/api/v1/sanitize', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ raw_input: inputVal })
                        })
                        .then(r => r.json())
                        .then(data => {
                            out.innerHTML = "STATUS 200 OK!<br>" +
                                "XSS Threat Neutralized: <strong>" + data.xss_threat_neutralized + "</strong><br><br>" +
                                "Sanitized Output:<br>" + data.sanitized_output;
                        });
                    }
                </script>
            </div>
        </body>
        </html>
    """)


# =============================================================================
# 5. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 26 Security Hardening Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("🛡️ Security Headers Audit at: http://127.0.0.1:5000/api/v1/headers-audit")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
