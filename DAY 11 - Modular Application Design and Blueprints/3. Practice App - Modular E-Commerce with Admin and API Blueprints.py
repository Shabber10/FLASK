"""
Day 11 Practice Application: Modular Enterprise E-Commerce Platform
====================================================================
This application demonstrates:
1. Creating & registering multiple Flask Blueprints (Storefront, Auth, Admin, API).
2. Implementing Nested Blueprints (api_v1_bp registered on api_parent_bp).
3. Utilizing Blueprint-scoped before_request hooks and error handlers.
4. Using namespaced url_for() lookups across modular view components.
5. Providing an interactive Web Navigation Dashboard testing all blueprints.
"""

from flask import Flask, Blueprint, jsonify, render_template_string, request, url_for, redirect

# ------------------------------------------------------------------------------
# 1. Storefront / Main Public Blueprint
# ------------------------------------------------------------------------------
storefront_bp = Blueprint('storefront', __name__)

@storefront_bp.route('/')
def home():
    dashboard_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Day 11 Modular Blueprint Architecture</title>
        <style>
            body { font-family: Arial, sans-serif; background: #eef2f5; margin: 30px; }
            .card { max-width: 850px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            .badge { padding: 4px 8px; border-radius: 4px; color: white; font-weight: bold; font-size: 0.85em; }
            .badge-auth { background: #e67e22; }
            .badge-admin { background: #c0392b; }
            .badge-api { background: #2980b9; }
            ul { line-height: 1.8; }
            a { color: #2980b9; text-decoration: none; font-weight: bold; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🧩 Modular Blueprint Architecture (Day 11)</h2>
            <p>The application is partitioned into isolated, decoupled Blueprint modules:</p>

            <ul>
                <li><span class="badge badge-auth">AUTH</span> <a href="{{ url_for('auth.login') }}">Auth Blueprint Login Page</a> (<code>/auth/login</code>)</li>
                <li><span class="badge badge-admin">ADMIN</span> <a href="{{ url_for('admin.dashboard') }}">Admin Blueprint Panel</a> (<code>/admin/dashboard</code> - Intercepted by Admin Guard)</li>
                <li><span class="badge badge-api">API v1</span> <a href="{{ url_for('api_parent.v1.products_list') }}">Nested API v1 Products List</a> (<code>/api/v1/products</code>)</li>
                <li><span class="badge badge-api">API v1</span> <a href="{{ url_for('api_parent.v1.health') }}">Nested API v1 Health Check</a> (<code>/api/v1/health</code>)</li>
            </ul>
        </div>
    </body>
    </html>
    """
    return render_template_string(dashboard_html)


# ------------------------------------------------------------------------------
# 2. Authentication Blueprint
# ------------------------------------------------------------------------------
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
    return jsonify({
        "module": "Authentication Blueprint",
        "endpoint": "auth.login",
        "url_prefix": "/auth",
        "status": "Login Portal Ready"
    })


# ------------------------------------------------------------------------------
# 3. Admin Panel Blueprint with Blueprint Guard Hook
# ------------------------------------------------------------------------------
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
def admin_security_guard():
    """Blueprint-scoped hook: Verifies admin access token parameter."""
    token = request.args.get('token')
    if token != 'admin123':
        return jsonify({
            "error": "Forbidden",
            "message": "Admin clearance token required! Append '?token=admin123' to URL to access dashboard."
        }), 403

@admin_bp.route('/dashboard')
def dashboard():
    return jsonify({
        "module": "Admin Panel Blueprint",
        "endpoint": "admin.dashboard",
        "access": "Granted (Token Verified)",
        "active_users": 150,
        "revenue_today": "$4,520.00"
    })


# ------------------------------------------------------------------------------
# 4. Nested API Blueprints (api_parent_bp -> v1_bp)
# ------------------------------------------------------------------------------
api_parent_bp = Blueprint('api_parent', __name__, url_prefix='/api')
v1_bp = Blueprint('v1', __name__, url_prefix='/v1')

@v1_bp.route('/products')
def products_list():
    return jsonify({
        "version": "v1",
        "products": [
            {"id": 101, "name": "Modular Keyboard", "price": 129.99},
            {"id": 102, "name": "Ergonomic Trackball", "price": 69.99}
        ]
    })

@v1_bp.route('/health')
def health():
    return jsonify({"status": "healthy", "api_version": 1.0})

# Nest v1_bp under api_parent_bp (Final route prefix: /api/v1)
api_parent_bp.register_blueprint(v1_bp)


# ------------------------------------------------------------------------------
# 5. Application Factory & Registration
# ------------------------------------------------------------------------------
app = Flask(__name__)

# Register all Blueprints onto main Flask Application
app.register_blueprint(storefront_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_parent_bp)


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 11 Modular Blueprint Application...")
    print("Main Dashboard at http://127.0.0.1:5000/")
    print("Try Admin (Protected) at http://127.0.0.1:5000/admin/dashboard?token=admin123")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
