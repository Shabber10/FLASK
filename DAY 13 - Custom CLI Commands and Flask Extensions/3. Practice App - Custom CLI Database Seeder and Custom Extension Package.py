"""
===============================================================================
Day 13 Practice Script: Custom CLI Commands & Reusable Flask Extension
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Writing a custom reusable Flask extension (`RequestAnalyticsExt`).
2. STEP 2: Defining `User(db.Model)`.
3. STEP 3: Initializing Flask app & binding extensions via `analytics = RequestAnalyticsExt(app)`.
4. STEP 4: Registering custom CLI commands (`seed-users`, `reset-db`, `analytics-report`) with `@with_appcontext`.
5. STEP 5: Web UI route handler (`/`) rendering `templates/index.html`.
6. STEP 6: RESTful JSON API endpoints (`/api/users`).

How to test CLI commands in your terminal:
------------------------------------------
$ python "3. Practice App - Custom CLI Database Seeder and Custom Extension Package.py" seed-users --count 5
$ python "3. Practice App - Custom CLI Database Seeder and Custom Extension Package.py" analytics-report
$ python "3. Practice App - Custom CLI Database Seeder and Custom Extension Package.py" reset-db
"""

import time
import click
from flask import Flask, jsonify, request, render_template, current_app
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy unattached globally
db = SQLAlchemy()


# =============================================================================
# STEP 1: Custom Reusable Flask Extension Class
# =============================================================================
class RequestAnalyticsExt:
    """Custom extension tracking HTTP request counts and response latency."""

    def __init__(self, app=None):
        self.request_count = 0
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initializes extension and attaches request hooks."""
        app.config.setdefault('ANALYTICS_ENABLED', True)
        
        # Store extension instance in app.extensions
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['request_analytics'] = self

        # Register request hooks
        app.before_request(self._before_request)
        app.after_request(self._after_request)

    def _before_request(self):
        request._start_time = time.time()
        self.request_count += 1

    def _after_request(self, response):
        if current_app.config.get('ANALYTICS_ENABLED'):
            duration = round((time.time() - getattr(request, '_start_time', time.time())) * 1000, 2)
            response.headers['X-Server-Latency-MS'] = f"{duration}ms"
        return response


# =============================================================================
# STEP 2: Database Model Definition
# =============================================================================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}


# =============================================================================
# STEP 3: Application Setup & Extension Binding
# =============================================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'day13-cli-extensions-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///day13_cli_demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
analytics = RequestAnalyticsExt(app)

with app.app_context():
    db.create_all()


# =============================================================================
# STEP 4: Custom CLI Commands Registration
# =============================================================================
@app.cli.command("seed-users")
@click.option("--count", default=5, help="Number of sample users to create")
@with_appcontext
def seed_users_cmd(count):
    """Seed sample users into SQLite database. Run: $ flask seed-users --count 5"""
    click.echo(f"🌱 Seeding {count} sample users into database...")
    for i in range(1, count + 1):
        username = f"user_{i}_{int(time.time())}"
        email = f"{username}@company.com"
        u = User(username=username, email=email)
        db.session.add(u)
    db.session.commit()
    click.echo(click.style(f"✅ Successfully seeded {count} users!", fg="green", bold=True))


@app.cli.command("reset-db")
@with_appcontext
def reset_db_cmd():
    """Drop and recreate all database tables. Run: $ flask reset-db"""
    if click.confirm("⚠️ Are you sure you want to drop all database tables?", abort=True):
        db.drop_all()
        db.create_all()
        click.echo(click.style("✅ Database reset successfully!", fg="yellow", bold=True))


@app.cli.command("analytics-report")
@with_appcontext
def analytics_report_cmd():
    """Print CLI summary report of HTTP request metrics. Run: $ flask analytics-report"""
    ext = current_app.extensions.get('request_analytics')
    total_reqs = ext.request_count if ext else 0
    
    click.echo("=" * 50)
    click.echo(click.style("📊 REQUEST ANALYTICS EXTENSION REPORT", fg="cyan", bold=True))
    click.echo("=" * 50)
    click.echo(f"Total Server HTTP Requests Processed: {total_reqs}")
    click.echo("Analytics Enabled: True")
    click.echo("=" * 50)


# =============================================================================
# STEP 5 & 6: Web UI & REST API Route Handlers
# =============================================================================

@app.route('/')
def home():
    """Step 5: Web UI dashboard rendering templates/index.html."""
    users = db.session.execute(db.select(User)).scalars().all()
    return render_template('index.html', users=users)


@app.route('/api/users')
def api_users():
    """Step 6: REST API endpoint returning users as JSON."""
    users = db.session.execute(db.select(User)).scalars().all()
    return jsonify([u.to_dict() for u in users]), 200


# =============================================================================
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 13 CLI & Extension Application...")
    print("🌐 Web UI at: http://127.0.0.1:5000/")
    print("📡 Users API at: http://127.0.0.1:5000/api/users")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
