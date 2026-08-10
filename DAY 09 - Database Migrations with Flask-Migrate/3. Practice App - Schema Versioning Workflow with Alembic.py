"""
===============================================================================
Day 09 Practice Script: Schema Versioning & Flask-Migrate Workflow
===============================================================================
This script demonstrates:
1. Setting up Flask-Migrate with SQLite batch mode (`render_as_batch=True`).
2. Defining ORM Models prepared for schema evolution.
3. Exposing REST endpoints to inspect live user data and schema status.
4. Complete step-by-step CLI commands for database version control.

How to run the Migration Workflow for this script:
--------------------------------------------------
1. Open your terminal in this directory.
2. Initialize migration repository (run once):
   $ flask --app "3. Practice App - Schema Versioning Workflow with Alembic.py" db init

3. Generate initial migration script:
   $ flask --app "3. Practice App - Schema Versioning Workflow with Alembic.py" db migrate -m "Initial UserAccount schema"

4. Apply migration script to SQLite database:
   $ flask --app "3. Practice App - Schema Versioning Workflow with Alembic.py" db upgrade

5. Run the web application:
   $ python "3. Practice App - Schema Versioning Workflow with Alembic.py"
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day09-flask-migrate-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///migrations_demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy extension
db = SQLAlchemy(app)

# Initialize Flask-Migrate with SQLite batch mode enabled for ALTER TABLE support
migrate = Migrate(app, db, render_as_batch=True)


# =============================================================================
# 1. UserAccount ORM Model Definition
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
# 2. REST API Routes
# =============================================================================
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to Day 09 Database Migrations Demo!",
        "instructions": "Use 'flask db migrate' and 'flask db upgrade' to evolve database schema.",
        "endpoints": {
            "get_users": "/api/users",
            "create_user": "/api/users (POST)"
        }
    }), 200


@app.route('/api/users', methods=['GET'])
def list_users():
    """Returns all users stored in the migrated database."""
    stmt = db.select(UserAccount).order_by(UserAccount.id)
    users = db.session.execute(stmt).scalars().all()
    return jsonify([u.to_dict() for u in users]), 200


@app.route('/api/users', methods=['POST'])
def create_user():
    """Creates a new user record in the migrated database."""
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
# 3. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 09 Schema Versioning Application...")
    print("🌐 Open API at: http://127.0.0.1:5000/")
    print("📡 Test Users API at: http://127.0.0.1:5000/api/users")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
