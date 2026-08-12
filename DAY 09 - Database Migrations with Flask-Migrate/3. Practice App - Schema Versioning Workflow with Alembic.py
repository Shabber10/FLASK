"""
===============================================================================
Day 09 Practice Script: Schema Versioning & Flask-Migrate Workflow
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Setting up Flask-Migrate with SQLite batch mode (`render_as_batch=True`).
2. STEP 2: Defining `UserAccount(db.Model)` prepared for schema evolution.
3. STEP 3: Web UI dashboard route handler (`/`) using `render_template('index.html')`.
4. STEP 4: Form handler (`/users/add`) to create records in the migrated database.
5. STEP 5: RESTful JSON API endpoints (`/api/users`).
6. STEP 6: Complete CLI commands for database version control.

How to run the Migration Workflow for this script:
--------------------------------------------------
1. Open your terminal in this directory.
2. Initialize migration repository (run once per project):
   $ flask --app "3. Practice App - Schema Versioning Workflow with Alembic.py" db init

3. Generate initial migration script:
   $ flask --app "3. Practice App - Schema Versioning Workflow with Alembic.py" db migrate -m "Initial UserAccount schema"

4. Apply migration script to SQLite database:
   $ flask --app "3. Practice App - Schema Versioning Workflow with Alembic.py" db upgrade

5. Run the web application:
   $ python "3. Practice App - Schema Versioning Workflow with Alembic.py"
"""

from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day09-flask-migrate-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///migrations_demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# =============================================================================
# STEP 1: Initialize Extensions with SQLite Batch Mode
# =============================================================================
db = SQLAlchemy(app)

# Initialize Flask-Migrate with SQLite batch mode enabled for ALTER TABLE support
migrate = Migrate(app, db, render_as_batch=True)


# =============================================================================
# STEP 2: UserAccount ORM Model Definition
# =============================================================================
class UserAccount(db.Model):
    """ORM Model representing user accounts, ready for schema evolution."""
    __tablename__ = 'user_accounts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        """Helper method serializing model instance to JSON."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_verified": self.is_verified,
            "created_at": str(self.created_at) if self.created_at else None
        }


# =============================================================================
# STEP 3 & 4: Web UI Dashboard Handlers (HTML via render_template)
# =============================================================================

@app.route('/')
def index():
    """
    Step 3: Renders HTML Schema Versioning Dashboard querying migrated database rows.
    """
    try:
        stmt = db.select(UserAccount).order_by(UserAccount.id.desc())
        users = db.session.execute(stmt).scalars().all()
    except Exception as e:
        users = []
        print(f"⚠️ Database query notice: Make sure you ran 'flask db upgrade'! Error: {e}")

    return render_template('index.html', users=users)


@app.route('/users/add', methods=['POST'])
def add_user_form():
    """
    Step 4: Form submission handler to create a new user account.
    """
    username = request.form.get('username')
    email = request.form.get('email')

    if username and email:
        try:
            user = UserAccount(username=username, email=email)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"❌ [DB ERROR] Rollback triggered: {e}")

    return redirect(url_for('index'))


# =============================================================================
# STEP 5: RESTful JSON API Endpoints
# =============================================================================

@app.route('/api/users', methods=['GET'])
def list_users_api():
    """Step 5a: Returns all users stored in the migrated database as JSON."""
    try:
        stmt = db.select(UserAccount).order_by(UserAccount.id)
        users = db.session.execute(stmt).scalars().all()
        return jsonify([u.to_dict() for u in users]), 200
    except Exception as e:
        return jsonify({"error": "Database Table Missing", "message": "Run 'flask db upgrade' first!"}), 500


@app.route('/api/users', methods=['POST'])
def create_user_api():
    """Step 5b: Creates a new user record from JSON payload."""
    data = request.get_json(silent=True) or {}
    if not data.get('username') or not data.get('email'):
        return jsonify({"error": "Bad Request", "message": "Username and email required"}), 400

    try:
        user = UserAccount(username=data['username'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database Error", "message": str(e)}), 400


# =============================================================================
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 09 Schema Versioning Application...")
    print("🌐 Open Web Dashboard at: http://127.0.0.1:5000/")
    print("📡 Test Users API at: http://127.0.0.1:5000/api/users")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
