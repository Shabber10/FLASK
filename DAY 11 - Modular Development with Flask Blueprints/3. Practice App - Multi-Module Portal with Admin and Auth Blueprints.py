"""
===============================================================================
Day 11 Practice Script: Multi-Blueprint Application Architecture
===============================================================================
This script demonstrates:
1. Instantiating independent Blueprints for Auth, Admin, and REST API modules.
2. Registering Blueprints with custom URL prefixes (`/auth`, `/admin`, `/api/v1`).
3. Blueprint-specific request lifecycle hooks (`@auth_bp.before_request`).
4. Cross-blueprint URL generation using `url_for('blueprint.endpoint')`.
5. Exposing a Web UI Portal and REST API endpoints.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Multi-Module Portal with Admin and Auth Blueprints.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from flask import Flask, Blueprint, jsonify, request, render_template_string, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day11-blueprints-masterclass-secret'


# =============================================================================
# 1. Auth Blueprint Definition (/auth)
# =============================================================================
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.before_request
def log_auth_request():
    """Blueprint-specific request hook executing ONLY for /auth routes."""
    print(f"🔒 [AUTH MODULE HOOK] Accessing auth route: {request.path}")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Renders login form or processes login submission."""
    if request.method == 'POST':
        username = request.form.get('username', 'Guest')
        flash(f"User '{username}' logged in successfully!", "success")
        return redirect(url_for('admin.dashboard'))
    
    return render_template_string("""
        <h2>🔒 Auth Module: Login</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Enter username" required>
            <button type="submit">Login</button>
        </form>
        <p><a href="{{ url_for('home') }}">Back to Home</a></p>
    """)

@auth_bp.route('/logout')
def logout():
    """Logs out user and redirects back to Home."""
    flash("User logged out successfully.", "info")
    return redirect(url_for('home'))


# =============================================================================
# 2. Admin Blueprint Definition (/admin)
# =============================================================================
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
def dashboard():
    """Admin Dashboard view."""
    return render_template_string("""
        <h2>⚙️ Admin Module: Dashboard</h2>
        <p>System Status: <strong>ALL SYSTEMS OPERATIONAL</strong></p>
        <ul>
            <li>Active Users: 1,240</li>
            <li>Database Binds: Primary, Audit</li>
            <li>Registered Blueprints: Auth, Admin, API v1</li>
        </ul>
        <p>
            <a href="{{ url_for('auth.logout') }}">Logout</a> | 
            <a href="{{ url_for('api_v1.get_metrics') }}">View API Metrics</a> | 
            <a href="{{ url_for('home') }}">Back to Home</a>
        </p>
    """)


# =============================================================================
# 3. REST API v1 Blueprint Definition (/api/v1)
# =============================================================================
api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')

@api_v1_bp.route('/users')
def get_users():
    """Returns JSON list of users."""
    return jsonify({
        "status": "success",
        "module": "api_v1",
        "users": [
            {"id": 1, "username": "alice_dev", "role": "developer"},
            {"id": 2, "username": "bob_admin", "role": "administrator"}
        ]
    }), 200

@api_v1_bp.route('/metrics')
def get_metrics():
    """Returns system performance metrics as JSON."""
    return jsonify({
        "status": "success",
        "system_uptime": "99.98%",
        "requests_per_minute": 450
    }), 200


# =============================================================================
# 4. Main App Setup & Blueprint Registration
# =============================================================================
# Register all sub-module Blueprints onto main Flask application instance
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_v1_bp)


@app.route('/')
def home():
    """Main Application Home Page displaying Blueprint cross-links."""
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Day 11 Multi-Blueprint Portal</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 40px; color: #333; }
                .card { max-width: 700px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
                h1 { color: #2c3e50; }
                .btn { display: inline-block; background: #3498db; color: white; padding: 10px 18px; text-decoration: none; border-radius: 4px; font-weight: bold; margin-right: 10px; }
                .btn-admin { background: #e67e22; }
                .btn-api { background: #2ecc71; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🧩 Multi-Blueprint Portal (Day 11)</h1>
                <p>This Flask application is organized into 3 modular Blueprints:</p>
                <ul>
                    <li><code>auth_bp</code> -> URL Prefix: <code>/auth</code></li>
                    <li><code>admin_bp</code> -> URL Prefix: <code>/admin</code></li>
                    <li><code>api_v1_bp</code> -> URL Prefix: <code>/api/v1</code></li>
                </ul>
                <hr>
                <div>
                    <a class="btn" href="{{ url_for('auth.login') }}">Go to Auth Login (/auth/login)</a>
                    <a class="btn btn-admin" href="{{ url_for('admin.dashboard') }}">Go to Admin Dashboard (/admin/dashboard)</a>
                    <a class="btn btn-api" href="{{ url_for('api_v1.get_users') }}">Call API Users (/api/v1/users)</a>
                </div>
            </div>
        </body>
        </html>
    """)


# =============================================================================
# 5. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 11 Multi-Blueprint Portal Application...")
    print("🌐 Home Portal at: http://127.0.0.1:5000/")
    print("🔒 Auth Module at: http://127.0.0.1:5000/auth/login")
    print("⚙️ Admin Module at: http://127.0.0.1:5000/admin/dashboard")
    print("📡 API v1 Module at: http://127.0.0.1:5000/api/v1/users")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
