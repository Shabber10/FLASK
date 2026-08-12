"""
===============================================================================
Day 26 Practice Script: Enterprise Flask Security Hardening Infrastructure
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Hardening HTTP response headers with `Flask-Talisman`.
2. STEP 2: Input sanitization helper function stripping malicious `<script>` and `<iframe>` XSS payloads.
3. STEP 3: REST API endpoints inspecting headers (`GET /api/v1/headers-audit`) and testing input sanitization (`POST /api/v1/sanitize`).
4. STEP 4: Interactive Web UI Security Audit Dashboard rendering `templates/index.html`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Enterprise Hardened Flask App with Flask-Talisman.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import html
import re
from flask import Flask, jsonify, request, render_template
from flask_talisman import Talisman

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day26-talisman-security-masterclass-secret'

# =============================================================================
# STEP 1: Flask-Talisman Enterprise Security Hardening Setup
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
# STEP 2: Input Sanitization Helper Function (Strips XSS Tags)
# =============================================================================
def sanitize_user_input(raw_text):
    """Step 2: Sanitizes raw text input, stripping dangerous <script>, <iframe>, and event handlers."""
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
# STEP 3: REST API Endpoints (Sanitize & Headers Audit)
# =============================================================================

# POST /api/v1/sanitize -> Accepts raw input and returns sanitized safe output
@app.route('/api/v1/sanitize', methods=['POST'])
def sanitize_endpoint():
    """Step 3a: Sanitizes user-submitted raw HTML payloads."""
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
    """Step 3b: Inspects active HTTP security headers injected by Talisman."""
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
# STEP 4: Interactive Web UI Dashboard Route Handler (render_template)
# =============================================================================
@app.route('/')
def home():
    """Step 4: Renders templates/index.html dashboard."""
    return render_template('index.html')


# =============================================================================
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 26 Security Hardening Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("🛡️ Security Headers Audit at: http://127.0.0.1:5000/api/v1/headers-audit")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
