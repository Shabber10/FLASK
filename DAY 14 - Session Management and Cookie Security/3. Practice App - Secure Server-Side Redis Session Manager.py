"""
===============================================================================
Day 14 Practice Script: Hardened Session Management & Security System
===============================================================================
This script demonstrates:
1. Setting up hardened Cookie Security Flags (`HttpOnly`, `SameSite='Lax'`).
2. Creating and inspecting user sessions (`session['user_id']`).
3. Managing session lifetimes and permanent session flags.
4. Implementing full session clearing (`session.clear()`) upon logout.
5. Exposing an interactive Session Manager UI and REST API.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Secure Server-Side Redis Session Manager.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from datetime import timedelta
from flask import Flask, session, jsonify, request, render_template_string, redirect, url_for, flash

app = Flask(__name__)

# Cryptographic signing key required for session security
app.config['SECRET_KEY'] = 'day14-hardened-session-signing-key-32bytes'

# =============================================================================
# 1. Hardened Cookie Security Flags
# =============================================================================
# Block client-side JavaScript access to cookies (Prevents XSS cookie theft)
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Protect against Cross-Site Request Forgery (CSRF)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Set default permanent session expiration to 7 days
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)


# =============================================================================
# 2. HTML UI Template String
# =============================================================================
SESSION_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 14 Session Security Portal</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 40px; color: #333; }
        .card { max-width: 650px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
        h2 { color: #2c3e50; margin-top: 0; }
        .status-badge { background: #27ae60; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 0.85em; }
        .status-badge-off { background: #e74c3c; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 0.85em; }
        .form-group { margin-bottom: 15px; }
        input[type="text"] { width: 100%; padding: 10px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
        .btn { background: #3498db; color: white; border: none; padding: 10px 18px; border-radius: 4px; cursor: pointer; font-weight: bold; }
        .btn-danger { background: #e74c3c; text-decoration: none; padding: 10px 18px; border-radius: 4px; color: white; font-weight: bold; display: inline-block; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 10px; border-bottom: 1px solid #e9ecef; text-align: left; }
        th { background: #34495e; color: white; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🔒 Hardened Session Security Portal (Day 14)</h2>

        {% if session.get('user_id') %}
            <p>Session Status: <span class="status-badge">LOGGED IN</span></p>
            <table>
                <thead><tr><th>Session Key</th><th>Active Value</th></tr></thead>
                <tbody>
                    <tr><td><code>user_id</code></td><td>{{ session.user_id }}</td></tr>
                    <tr><td><code>username</code></td><td><strong>{{ session.username }}</strong></td></tr>
                    <tr><td><code>role</code></td><td>{{ session.role }}</td></tr>
                    <tr><td><code>permanent</code></td><td>{{ session.permanent }}</td></tr>
                </tbody>
            </table>
            <p style="margin-top: 20px;">
                <a class="btn-danger" href="/logout">Logout & Clear Session</a>
            </p>
        {% else %}
            <p>Session Status: <span class="status-badge-off">NOT LOGGED IN</span></p>
            <form method="POST" action="/login">
                <div class="form-group">
                    <label>Username:</label>
                    <input type="text" name="username" placeholder="Enter username (e.g. alice_dev)" required>
                </div>
                <button class="btn" type="submit">Create Secure Session</button>
            </form>
        {% endif %}

        <hr style="margin-top: 30px;">
        <p><a href="/api/profile">Inspect Profile API (/api/profile)</a></p>
    </div>
</body>
</html>
"""


# =============================================================================
# 3. Route Handlers
# =============================================================================
@app.route('/')
def home():
    """Renders HTML Portal displaying active session status."""
    return render_template_string(SESSION_HTML)


@app.route('/login', methods=['POST'])
def login():
    """Simulates user login and sets hardened session keys."""
    username = request.form.get('username') or (request.json or {}).get('username', 'alice_dev')
    
    # Store session values
    session['user_id'] = 101
    session['username'] = username
    session['role'] = 'administrator'
    
    # Enable 7-day permanent session lifetime
    session.permanent = True

    if request.is_json:
        return jsonify({"message": "Session created successfully", "user_id": 101, "username": username}), 200
    
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    """Clears all session keys completely."""
    session.clear()
    
    if request.is_json:
        return jsonify({"message": "Logged out and session cleared"}), 200
        
    return redirect(url_for('home'))


@app.route('/api/profile')
def api_profile():
    """API Endpoint returning current session profile or 401 Unauthorized."""
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized", "message": "No active session found. Please login."}), 401
        
    return jsonify({
        "user_id": session.get('user_id'),
        "username": session.get('username'),
        "role": session.get('role'),
        "cookie_security": {
            "httponly": app.config['SESSION_COOKIE_HTTPONLY'],
            "samesite": app.config['SESSION_COOKIE_SAMESITE']
        }
    }), 200


# =============================================================================
# 4. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 14 Session Security Application...")
    print("🌐 Session UI at: http://127.0.0.1:5000/")
    print("📡 Profile API at: http://127.0.0.1:5000/api/profile")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
