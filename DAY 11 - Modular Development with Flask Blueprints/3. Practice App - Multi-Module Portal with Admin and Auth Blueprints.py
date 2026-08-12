"""
===============================================================================
Day 11 Practice Script: Multi-Blueprint Application Architecture
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Instantiating independent Blueprints for Auth, Admin, and REST API modules.
2. STEP 2: Adding Blueprint-specific request lifecycle hooks (`@auth_bp.before_request`).
3. STEP 3: Registering Blueprints with custom URL prefixes (`/auth`, `/admin`, `/api/v1`).
4. STEP 4: Web UI route handlers using namespaced HTML template files in `templates/`.
5. STEP 5: Cross-blueprint URL generation using `url_for('blueprint.endpoint')`.
6. STEP 6: Exposing REST API endpoints via `api_v1_bp`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Multi-Module Portal with Admin and Auth Blueprints.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from flask import Flask, Blueprint, jsonify, request, render_template, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day11-blueprints-masterclass-secret'


# =============================================================================
# STEP 1 & 2: Auth Blueprint Definition & Request Lifecycle Hook (/auth)
# =============================================================================
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.before_request
def log_auth_request():
    """Step 2: Blueprint-specific request hook executing ONLY for /auth routes."""
    print(f"🔒 [AUTH MODULE HOOK] Accessing auth route: {request.path}")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Step 4: Renders templates/auth/login.html or processes submission."""
    if request.method == 'POST':
        username = request.form.get('username', 'Guest')
        flash(f"User '{username}' logged in successfully!", "success")
        return redirect(url_for('admin.dashboard'))
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """Logs out user and redirects back to Home."""
    flash("User logged out successfully.", "info")
    return redirect(url_for('home'))


# =============================================================================
# STEP 1: Admin Blueprint Definition (/admin)
# =============================================================================
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
def dashboard():
    """Step 4: Renders templates/admin/dashboard.html."""
    return render_template('admin/dashboard.html')


# =============================================================================
# STEP 1 & 6: REST API v1 Blueprint Definition (/api/v1)
# =============================================================================
api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')

@api_v1_bp.route('/users')
def get_users():
    """Step 6a: Returns JSON list of users."""
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
    """Step 6b: Returns system performance metrics as JSON."""
    return jsonify({
        "status": "success",
        "system_uptime": "99.98%",
        "requests_per_minute": 450
    }), 200


# =============================================================================
# STEP 3: Main App Setup & Blueprint Registration
# =============================================================================
# Register all sub-module Blueprints onto main Flask application instance
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_v1_bp)


@app.route('/')
def home():
    """
    Step 5: Main Application Home Page displaying Blueprint cross-links using url_for().
    Renders templates/portal.html file.
    """
    return render_template('portal.html')


# =============================================================================
# Main Entrypoint
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
