"""
===============================================================================
Day 14 Practice Script: Hardened Session Management & Security System
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Setting up hardened Cookie Security Flags (`HttpOnly`, `SameSite='Lax'`).
2. STEP 2: Creating and inspecting user sessions (`session['user_id']`, `session['username']`).
3. STEP 3: Managing session lifetimes and permanent session flags (`session.permanent = True`).
4. STEP 4: Web UI portal route handler (`/`) using `render_template('index.html')`.
5. STEP 5: Implementing full session clearing (`session.clear()`) upon logout.
6. STEP 6: Exposing RESTful JSON API endpoints (`/api/profile`).

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Secure Server-Side Redis Session Manager.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from datetime import timedelta
from flask import Flask, session, jsonify, request, render_template, redirect, url_for, flash

app = Flask(__name__)

# Cryptographic signing key required for session security
app.config['SECRET_KEY'] = 'day14-hardened-session-signing-key-32bytes'

# =============================================================================
# STEP 1: Hardened Cookie Security Flags Configuration
# =============================================================================
# Block client-side JavaScript access to cookies (Prevents XSS cookie theft)
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Protect against Cross-Site Request Forgery (CSRF)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Set default permanent session expiration to 7 days
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)


# =============================================================================
# STEP 4: Session Security Portal Route Handler (HTML via render_template)
# =============================================================================
@app.route('/')
def home():
    """
    Step 4: Renders HTML Session Security Portal displaying active session status.
    Uses templates/index.html file.
    """
    return render_template('index.html')


# =============================================================================
# STEP 2 & 3: Login Handler (Storing Session Keys & Setting Lifetime)
# =============================================================================
@app.route('/login', methods=['POST'])
def login():
    """
    Step 2 & 3: Simulates user login, sets session keys, and enables permanent lifetime.
    """
    username = request.form.get('username') or (request.json or {}).get('username', 'alice_dev')
    
    # Step 2: Store session values
    session['user_id'] = 101
    session['username'] = username
    session['role'] = 'administrator'
    
    # Step 3: Enable 7-day permanent session lifetime
    session.permanent = True

    if request.is_json:
        return jsonify({"message": "Session created successfully", "user_id": 101, "username": username}), 200
    
    return redirect(url_for('home'))


# =============================================================================
# STEP 5: Logout Handler (Complete Session Destruction)
# =============================================================================
@app.route('/logout')
def logout():
    """
    Step 5: Clears all session keys completely.
    """
    session.clear()
    
    if request.is_json:
        return jsonify({"message": "Logged out and session cleared"}), 200
        
    return redirect(url_for('home'))


# =============================================================================
# STEP 6: Profile API Endpoint (Inspecting Session Profile)
# =============================================================================
@app.route('/api/profile')
def api_profile():
    """
    Step 6: API Endpoint returning current session profile or 401 Unauthorized.
    """
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
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 14 Session Security Application...")
    print("🌐 Session UI at: http://127.0.0.1:5000/")
    print("📡 Profile API at: http://127.0.0.1:5000/api/profile")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
