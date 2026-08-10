"""
===============================================================================
Day 13 Practice Script: Custom CLI Commands & Reusable Flask Extension
===============================================================================
This script demonstrates:
1. Writing a custom reusable Flask extension (`RequestAnalyticsExt`).
2. Registering custom CLI commands (`seed-users`, `reset-db`, `analytics-report`).
3. Using Click decorators (`@click.option`, `@click.argument`, `@click.confirm`, `click.style`).
4. Binding application contexts with `@with_appcontext`.
5. Exposing a Web UI and REST API.

How to test CLI commands in your terminal:
------------------------------------------
$ python "3. Practice App - Custom CLI Database Seeder and Custom Extension Package.py" seed-users --count 5
$ python "3. Practice App - Custom CLI Database Seeder and Custom Extension Package.py" analytics-report
$ python "3. Practice App - Custom CLI Database Seeder and Custom Extension Package.py" reset-db
"""

import time
import click
from flask import Flask, jsonify, request, render_template_string, current_app
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy unattached globally
db = SQLAlchemy()


# =============================================================================
# 1. Custom Reusable Flask Extension Class
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
# 2. Database Model
# =============================================================================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}


# =============================================================================
# 3. Application Setup & Extension Binding
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
# 4. Custom CLI Commands
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
# 5. Web UI & REST API Routes
# =============================================================================
@app.route('/')
def home():
    users = db.session.execute(db.select(User)).scalars().all()
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Day 13 Custom CLI & Extensions</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 40px; color: #333; }
                .card { max-width: 750px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
                h2 { color: #2c3e50; margin-top: 0; }
                .badge { background: #8e44ad; color: white; padding: 4px 10px; border-radius: 4px; font-size: 0.85em; font-weight: bold; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 10px; border-bottom: 1px solid #e9ecef; text-align: left; }
                th { background: #34495e; color: white; }
                code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; color: #c7254e; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>🛠️ Custom CLI Commands & Extension Demo (Day 13)</h2>
                <p>Custom Extension Active: <span class="badge">RequestAnalyticsExt</span></p>

                <h3>Available Terminal CLI Commands:</h3>
                <ul>
                    <li><code>flask seed-users --count 5</code> -> Seeds sample users</li>
                    <li><code>flask reset-db</code> -> Interactively drops and recreates tables</li>
                    <li><code>flask analytics-report</code> -> Displays CLI request count report</li>
                </ul>

                <h3>Live Users in Database ({{ users|length }}):</h3>
                <table>
                    <thead><tr><th>ID</th><th>Username</th><th>Email</th></tr></thead>
                    <tbody>
                        {% for u in users %}
                        <tr><td>{{ u.id }}</td><td><strong>{{ u.username }}</strong></td><td>{{ u.email }}</td></tr>
                        {% else %}
                        <tr><td colspan="3">No users found. Run <code>flask seed-users</code> in terminal!</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </body>
        </html>
    """, users=users)


@app.route('/api/users')
def api_users():
    users = db.session.execute(db.select(User)).scalars().all()
    return jsonify([u.to_dict() for u in users]), 200


# =============================================================================
# 6. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 13 CLI & Extension Application...")
    print("🌐 Web UI at: http://127.0.0.1:5000/")
    print("📡 Users API at: http://127.0.0.1:5000/api/users")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
