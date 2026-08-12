"""
===============================================================================
Day 15 Practice Script: Full Authentication & Role-Based Access Control System
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Defining User model with `UserMixin` and salted password hashing (`generate_password_hash`, `check_password_hash`).
2. STEP 2: Setting up Flask-Login `LoginManager` & `@login_manager.user_loader`.
3. STEP 3: Writing custom `@role_required(*allowed_roles)` decorator using `functools.wraps`.
4. STEP 4: Seeding initial database accounts (`admin_boss`, `john_doe`).
5. STEP 5: Web UI portal route handlers (`/`, `/login`, `/logout`) rendering `templates/index.html`.
6. STEP 6: Exposing REST API endpoints (`/profile`, `/admin/dashboard`) returning HTTP 401 vs 403.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Full Authentication System with RBAC Decorators.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from functools import wraps
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, abort
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


# =============================================================================
# STEP 2: Flask-Login Initialization & User Loader Callback
# =============================================================================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# =============================================================================
# STEP 1: User ORM Model Definition with UserMixin & Hashing Methods
# =============================================================================
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='User')  # Options: 'Admin', 'Editor', 'User'

    def set_password(self, password):
        """Step 1a: Hashes raw password and stores hash string."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Step 1b: Verifies raw password input against stored hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "role": self.role}


@login_manager.user_loader
def load_user(user_id):
    """Step 2: Flask-Login user loader callback fetching User by integer ID."""
    return db.session.get(User, int(user_id))


# =============================================================================
# STEP 3: Custom RBAC Decorator with functools.wraps
# =============================================================================
def role_required(*allowed_roles):
    """Step 3: Custom decorator restricting route access to specified roles."""
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


# =============================================================================
# STEP 4: Initial Database Seeding
# =============================================================================
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
# STEP 5 & 6: Web UI Routes (render_template) & REST API Handlers
# =============================================================================
@app.route('/')
def home():
    """Step 5a: Web UI Auth portal rendering templates/index.html."""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Step 5b: Processes login requests or renders templates/index.html."""
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

    return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    """Step 5c: Logs active user out and clears session."""
    logout_user()
    if request.is_json:
        return jsonify({"message": "Logged out successfully"}), 200
    return redirect(url_for('home'))


@app.route('/profile')
@login_required
def profile():
    """Step 6a: Protected User Profile API."""
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
    """Step 6b: Protected Admin Dashboard API (Requires Admin role)."""
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
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 15 Auth & RBAC Application...")
    print("🌐 Home UI at: http://127.0.0.1:5000/")
    print("👤 Profile API at: http://127.0.0.1:5000/profile")
    print("🔒 Admin Dashboard API at: http://127.0.0.1:5000/admin/dashboard")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
