"""
Day 14 Practice Application: User Authentication & RBAC Engine
===============================================================
This application demonstrates:
1. Secure password hashing with Werkzeug security (generate_password_hash).
2. Session-based authentication with Flask-Login and UserMixin.
3. Defining user_loader callbacks for session persistence.
4. Implementing custom Role-Based Access Control (@roles_required).
5. Web interface for Registration, Login, Protected Profile, and Admin Panel.
"""

from flask import Flask, render_template_string, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day14-authentication-rbac-secret-key-30-days'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth_rbac.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'


# ------------------------------------------------------------------------------
# 1. User ORM Model with UserMixin
# ------------------------------------------------------------------------------
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='member')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ------------------------------------------------------------------------------
# 2. Role-Based Access Control (RBAC) Decorator
# ------------------------------------------------------------------------------
def roles_required(*roles):
    """Custom Decorator enforcing role-based access control."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login', next=request.url))
            if current_user.role not in roles:
                flash(f"Access Denied: Role '{current_user.role}' lacks clearance for this area.", "danger")
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Initialize DB & Seed Demo Accounts
with app.app_context():
    db.create_all()
    if not db.session.execute(db.select(User)).scalars().first():
        admin = User(username="admin", email="admin@system.com", role="admin")
        admin.set_password("AdminPass123!")

        member = User(username="john_doe", email="john@example.com", role="member")
        member.set_password("MemberPass123!")

        db.session.add_all([admin, member])
        db.session.commit()


# ------------------------------------------------------------------------------
# 3. HTML Template String
# ------------------------------------------------------------------------------
AUTH_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 14 Authentication & RBAC Engine</title>
    <style>
        body { font-family: Arial, sans-serif; background: #eef2f5; margin: 30px; }
        .card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .navbar { display: flex; gap: 15px; margin-bottom: 20px; background: #2c3e50; padding: 15px; border-radius: 6px; }
        .navbar a { color: white; text-decoration: none; font-weight: bold; }
        .alert { padding: 12px; margin-bottom: 20px; border-radius: 5px; color: white; font-weight: bold; }
        .alert-success { background: #2ecc71; }
        .alert-danger { background: #e74c3c; }
        .alert-warning { background: #f39c12; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; font-weight: bold; margin-bottom: 5px; }
        .form-group input { width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
        .btn { background: #2980b9; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; width: 100%; font-size: 1em; }
    </style>
</head>
<body>
    <div class="card">
        <div class="navbar">
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <a href="{{ url_for('admin_panel') }}">Admin Panel</a>
            {% if current_user.is_authenticated %}
                <a href="{{ url_for('logout') }}" style="margin-left:auto;">Logout ({{ current_user.username }})</a>
            {% else %}
                <a href="{{ url_for('login') }}" style="margin-left:auto;">Login</a>
                <a href="{{ url_for('register') }}">Register</a>
            {% endif %}
        </div>

        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        {% if page == 'login' %}
            <h2>🔑 User Login</h2>
            <form method="POST">
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" name="username" required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" required>
                </div>
                <button class="btn" type="submit">Sign In</button>
            </form>
            <p>Demo Accounts (Password for all: AdminPass123! or MemberPass123!):</p>
            <ul>
                <li>Admin: <code>admin</code></li>
                <li>Member: <code>john_doe</code></li>
            </ul>

        {% elif page == 'register' %}
            <h2>📝 Account Registration</h2>
            <form method="POST">
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" name="username" required>
                </div>
                <div class="form-group">
                    <label>Email Address</label>
                    <input type="email" name="email" required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" required>
                </div>
                <button class="btn" type="submit">Create Account</button>
            </form>

        {% elif page == 'dashboard' %}
            <h2>👤 User Dashboard</h2>
            <p>Welcome back, <strong>{{ current_user.username }}</strong>!</p>
            <p>Role Clearance Level: <strong>{{ current_user.role|upper }}</strong></p>
            <p>Email: {{ current_user.email }}</p>

        {% elif page == 'admin' %}
            <h2>🛡️ Restricted System Admin Panel</h2>
            <p>Clearance Granted! Welcome to Administrator System Settings.</p>
            <p>Active Users Count: 2</p>
        {% endif %}
    </div>
</body>
</html>
"""


# ------------------------------------------------------------------------------
# 4. Route Handlers
# ------------------------------------------------------------------------------
@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template_string(AUTH_HTML, page='dashboard')

@app.route('/admin')
@roles_required('admin')
def admin_panel():
    return render_template_string(AUTH_HTML, page='admin')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        stmt = db.select(User).where(User.username == username)
        user = db.session.execute(stmt).scalar_one_or_none()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash(f"Welcome back, {user.username}!", "success")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
            
        flash("Invalid username or password.", "danger")

    return render_template_string(AUTH_HTML, page='login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user = User(username=username, email=email, role='member')
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash("Account created! Please sign in.", "success")
        return redirect(url_for('login'))
        
    return render_template_string(AUTH_HTML, page='register')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 14 Authentication & RBAC Application...")
    print("Portal UI at http://127.0.0.1:5000/")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
