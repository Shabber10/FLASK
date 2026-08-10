"""
===============================================================================
Day 15 Practice Script: Full Authentication & Role-Based Access Control System
===============================================================================
This script demonstrates:
1. Salting & hashing passwords using `generate_password_hash` and `check_password_hash`.
2. Flask-Login session management (`LoginManager`, `UserMixin`, `@login_required`, `current_user`).
3. Custom Role-Based Access Control decorator (`@role_required('Admin')`) using `functools.wraps`.
4. Returning proper HTTP 401 Unauthorized vs 403 Forbidden status codes.
5. Interactive Auth UI Portal and REST API endpoints.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Full Authentication System with RBAC Decorators.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from functools import wraps
from flask import Flask, jsonify, request, render_template_string, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day15-auth-rbac-masterclass-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///day15_auth.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# =============================================================================
# 1. User ORM Model Definition
# =============================================================================
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='User')  # Options: 'Admin', 'Editor', 'User'

    def set_password(self, password):
        """Hashes raw password and stores hash string."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies raw password input against stored hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "role": self.role}


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user loader callback."""
    return db.session.get(User, int(user_id))


# =============================================================================
# 2. Custom RBAC Decorator
# =============================================================================
def role_required(*allowed_roles):
    """Custom decorator restricting route access to specified roles."""
    def decorator(f):
        @wraps(f)  # MANDATORY: Preserves original function metadata!
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                if request.is_json:
                    return jsonify({"error": "Unauthorized", "message": "Please log in first."}), 401
                return redirect(url_for('login'))
                
            if current_user.role not in allowed_roles:
                if request.is_json:
                    return jsonify({"error": "Forbidden", "message": f"Requires role in {allowed_roles}"}), 403
                abort(403)
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Seed initial database users if empty
with app.app_context():
    db.create_all()
    if not db.session.execute(db.select(User)).scalars().first():
        admin_user = User(username="admin_boss", role="Admin")
        admin_user.set_password("AdminPass123!")
        
        regular_user = User(username="john_doe", role="User")
        regular_user.set_password("UserPass123!")
        
        db.session.add_all([admin_user, regular_user])
        db.session.commit()


# =============================================================================
# 3. Web UI Portal & Route Handlers
# =============================================================================
AUTH_UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 15 Auth & RBAC Portal</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 40px; color: #333; }
        .card { max-width: 650px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
        h2 { color: #2c3e50; margin-top: 0; }
        .badge { background: #3498db; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; }
        .badge-admin { background: #e74c3c; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; }
        .form-group { margin-bottom: 15px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
        .btn { background: #2ecc71; color: white; border: none; padding: 10px 18px; border-radius: 4px; cursor: pointer; font-weight: bold; }
        .btn-admin { background: #e74c3c; text-decoration: none; padding: 10px 18px; border-radius: 4px; color: white; font-weight: bold; display: inline-block; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 10px; border-bottom: 1px solid #e9ecef; text-align: left; }
        th { background: #34495e; color: white; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🔐 User Authentication & RBAC System (Day 15)</h2>

        {% if current_user.is_authenticated %}
            <p>Welcome, <strong>{{ current_user.username }}</strong>! Role: 
                <span class="{{ 'badge-admin' if current_user.role == 'Admin' else 'badge' }}">{{ current_user.role }}</span>
            </p>
            
            <h3>Available Endpoints:</h3>
            <ul>
                <li><a href="/profile">User Profile (/profile)</a></li>
                {% if current_user.role == 'Admin' %}
                    <li><a style="color: #e74c3c; font-weight: bold;" href="/admin/dashboard">🔒 Admin Dashboard (/admin/dashboard)</a></li>
                {% else %}
                    <li><span style="color: #999; text-decoration: line-through;">🔒 Admin Dashboard (/admin/dashboard)</span> (Disabled for regular Users)</li>
                {% endif %}
            </ul>

            <p style="margin-top: 20px;">
                <a class="btn-admin" href="/logout">Logout</a>
            </p>
        {% else %}
            <p>Please log in with pre-seeded accounts:</p>
            <ul>
                <li><strong>Admin</strong> -> Username: <code>admin_boss</code> | Password: <code>AdminPass123!</code></li>
                <li><strong>User</strong> -> Username: <code>john_doe</code> | Password: <code>UserPass123!</code></li>
            </ul>

            <form method="POST" action="/login">
                <div class="form-group">
                    <label>Username:</label>
                    <input type="text" name="username" required>
                </div>
                <div class="form-group">
                    <label>Password:</label>
                    <input type="password" name="password" required>
                </div>
                <button class="btn" type="submit">Login</button>
            </form>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(AUTH_UI_TEMPLATE)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username') or (request.json or {}).get('username')
        password = request.form.get('password') or (request.json or {}).get('password')

        user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()

        if user and user.check_password(password):
            login_user(user, remember=True)
            if request.is_json:
                return jsonify({"message": "Login successful", "user": user.to_dict()}), 200
            return redirect(url_for('home'))

        if request.is_json:
            return jsonify({"error": "Invalid credentials"}), 401
        flash("Invalid username or password.", "danger")

    return render_template_string(AUTH_UI_TEMPLATE)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    if request.is_json:
        return jsonify({"message": "Logged out successfully"}), 200
    return redirect(url_for('home'))


@app.route('/profile')
@login_required
def profile():
    return jsonify({
        "status": "authenticated",
        "user_id": current_user.id,
        "username": current_user.username,
        "role": current_user.role
    }), 200


@app.route('/admin/dashboard')
@login_required
@role_required('Admin')  # Custom RBAC Decorator enforcing Admin role!
def admin_dashboard():
    return jsonify({
        "status": "access_granted",
        "message": "Welcome to the Secret Admin Control Dashboard!",
        "admin_user": current_user.username
    }), 200


# Error Handlers
@app.errorhandler(403)
def forbidden_error(e):
    return jsonify({"error": "Forbidden", "message": "403 - You lack required Admin permissions!"}), 403


# =============================================================================
# 4. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 15 Auth & RBAC Application...")
    print("🌐 Home UI at: http://127.0.0.1:5000/")
    print("👤 Profile API at: http://127.0.0.1:5000/profile")
    print("🔒 Admin Dashboard API at: http://127.0.0.1:5000/admin/dashboard")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
