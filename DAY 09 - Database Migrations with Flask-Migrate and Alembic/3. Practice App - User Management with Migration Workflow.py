"""
Day 09 Practice Application: Database Migration & Schema Management
=====================================================================
This application demonstrates:
1. Initializing Flask-Migrate with Flask-SQLAlchemy (Migrate(app, db)).
2. Registering custom Flask CLI commands (@app.cli.command('seed_db')).
3. Handling schema updates and checking database revision status.
4. Exposing web UI and REST API displaying current Alembic migration version.
"""

from flask import Flask, jsonify, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text
import click
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day09-migrations-masterclass-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize Flask-Migrate Extension
migrate = Migrate(app, db, render_as_batch=True)


# ------------------------------------------------------------------------------
# 1. User Model Definition (Schema Version 1.0)
# ------------------------------------------------------------------------------
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='member')
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    bio = db.Column(db.Text, nullable=True) # Added in schema update

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "bio": self.bio
        }


# Auto-create tables for direct python script runs if migrations aren't initialized yet
with app.app_context():
    db.create_all()


# ------------------------------------------------------------------------------
# 2. Custom Flask CLI Commands
# ------------------------------------------------------------------------------
@app.cli.command('seed_db')
def seed_db():
    """Custom CLI command: Seeds initial user records into the database."""
    print("[CLI] Seeding initial user records into database...")
    if not db.session.execute(db.select(User)).scalars().first():
        u1 = User(username="admin_user", email="admin@system.com", role="admin", bio="System Administrator")
        u2 = User(username="john_doe", email="john@example.com", role="member", bio="Software Engineer")
        db.session.add_all([u1, u2])
        db.session.commit()
        print("[CLI] Database seeded successfully!")
    else:
        print("[CLI] Database already contains records.")


# ------------------------------------------------------------------------------
# 3. HTML UI Template String
# ------------------------------------------------------------------------------
MIGRATION_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 09 Database Migration Masterclass</title>
    <style>
        body { font-family: Arial, sans-serif; background: #eef2f5; margin: 30px; }
        .card { max-width: 800px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .badge { background: #27ae60; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 10px; border-bottom: 1px solid #ddd; text-align: left; }
        th { background: #2c3e50; color: white; }
        .cmd-box { background: #2d3748; color: #a0aec0; padding: 15px; border-radius: 6px; font-family: monospace; font-size: 0.9em; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🔄 Database Migrations & Schema Evolution (Day 09)</h2>

        <p>Active Alembic Revision Version: <span class="badge">{{ current_revision or 'Not Migrated / Native SQLite' }}</span></p>

        <h3>Registered Users</h3>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th>Bio</th>
                </tr>
            </thead>
            <tbody>
                {% for u in users %}
                <tr>
                    <td>{{ u.id }}</td>
                    <td><strong>{{ u.username }}</strong></td>
                    <td>{{ u.email }}</td>
                    <td>{{ u.role }}</td>
                    <td>{% if u.is_active %}Active{% else %}Disabled{% endif %}</td>
                    <td>{{ u.bio or 'N/A' }}</td>
                </tr>
                {% else %}
                <tr><td colspan="6">No users found. Run <code>flask seed_db</code> to populate.</td></tr>
                {% endfor %}
            </tbody>
        </table>

        <h3>Terminal Migration Commands</h3>
        <div class="cmd-box">
            # 1. Initialize Migration Repo<br>
            flask db init<br><br>
            # 2. Auto-generate Migration Script<br>
            flask db migrate -m "add_user_bio"<br><br>
            # 3. Apply Schema Changes to Database<br>
            flask db upgrade<br><br>
            # 4. Rollback Migration<br>
            flask db downgrade
        </div>
    </div>
</body>
</html>
"""


# ------------------------------------------------------------------------------
# 4. Route Handlers
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    users = db.session.execute(db.select(User)).scalars().all()
    
    # Try fetching active alembic revision from alembic_version table
    current_rev = None
    try:
        res = db.session.execute(text("SELECT version_num FROM alembic_version")).fetchone()
        if res:
            current_rev = res[0]
    except Exception:
        current_rev = "Uninitialized (Run 'flask db init && flask db migrate')"

    return render_template_string(MIGRATION_HTML, users=users, current_revision=current_rev)

@app.route('/api/users')
def users_api():
    users = db.session.execute(db.select(User)).scalars().all()
    return jsonify([u.to_dict() for u in users])


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 09 Migration Application...")
    print("Web UI at http://127.0.0.1:5000/")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
