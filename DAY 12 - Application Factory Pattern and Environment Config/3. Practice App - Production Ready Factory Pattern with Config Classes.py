"""
===============================================================================
Day 12 Practice Script: Enterprise Application Factory & Config Switching
===============================================================================
This script demonstrates:
1. Class-based configuration inheritance (`BaseConfig` -> `DevConfig`, `TestConfig`, `ProdConfig`).
2. The Application Factory Pattern (`create_app()`).
3. Deferred extension binding using `db.init_app(app)`.
4. Dynamic environment switching via arguments or environment variables.
5. Exposing a Configuration Status UI and REST API.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Production Ready Factory Pattern with Config Classes.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import os
from flask import Flask, jsonify, render_template_string, request
from flask_sqlalchemy import SQLAlchemy

# Instantiate unattached extension instance globally
db = SQLAlchemy()


# =============================================================================
# 1. Class-Based Configurations Hierarchy
# =============================================================================
class BaseConfig:
    """Shared Baseline Configuration Settings."""
    ENV_NAME = "base"
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-factory-secret-key-12345')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size


class DevConfig(BaseConfig):
    """Development Environment Settings."""
    ENV_NAME = "development"
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL', 'sqlite:///factory_dev.db')


class TestConfig(BaseConfig):
    """Automated Testing Environment Settings."""
    ENV_NAME = "testing"
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Isolated in-memory DB!
    WTF_CSRF_ENABLED = False


class ProdConfig(BaseConfig):
    """Live Production Environment Settings."""
    ENV_NAME = "production"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///factory_prod.db')
    SESSION_COOKIE_SECURE = True


# Map configuration keys to Config Classes
CONFIG_MAP = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig
}


# =============================================================================
# 2. User ORM Model Definition
# =============================================================================
class User(db.Model):
    """ORM Model representing Users."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}


# =============================================================================
# 3. Application Factory Function
# =============================================================================
def create_app(config_object=DevConfig):
    """
    Application Factory Pattern creating and returning a configured Flask app instance.
    
    :param config_object: Config class instance or dictionary mapping key string.
    """
    app = Flask(__name__)

    # 1. Load Configuration
    if isinstance(config_object, str):
        config_object = CONFIG_MAP.get(config_object.lower(), DevConfig)
        
    app.config.from_object(config_object)

    # 2. Initialize Extensions (Deferred Binding Pattern)
    db.init_app(app)

    # 3. Create Tables inside Active Database Context
    with app.app_context():
        db.create_all()

    # 4. Register Routes and Endpoints
    @app.route('/')
    def index():
        return render_template_string("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Day 12 Application Factory</title>
                <style>
                    body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 40px; color: #333; }
                    .card { max-width: 700px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
                    h2 { color: #2c3e50; margin-top: 0; }
                    .badge { background: #27ae60; color: white; padding: 4px 10px; border-radius: 4px; font-size: 0.85em; font-weight: bold; }
                    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                    th, td { padding: 10px; border-bottom: 1px solid #e9ecef; text-align: left; }
                    th { background: #34495e; color: white; }
                    code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; color: #c7254e; }
                </style>
            </head>
            <body>
                <div class="card">
                    <h2>🏭 Application Factory & Config Status (Day 12)</h2>
                    <p>Active Environment: <span class="badge">{{ config.ENV_NAME|upper }}</span></p>

                    <table>
                        <thead>
                            <tr><th>Setting Key</th><th>Value</th></tr>
                        </thead>
                        <tbody>
                            <tr><td><code>DEBUG</code></td><td>{{ config.DEBUG }}</td></tr>
                            <tr><td><code>TESTING</code></td><td>{{ config.TESTING }}</td></tr>
                            <tr><td><code>SQLALCHEMY_DATABASE_URI</code></td><td>{{ config.SQLALCHEMY_DATABASE_URI }}</td></tr>
                            <tr><td><code>SECRET_KEY</code></td><td>{{ config.SECRET_KEY[:8] }}... (Truncated for Security)</td></tr>
                            <tr><td><code>MAX_CONTENT_LENGTH</code></td><td>{{ config.MAX_CONTENT_LENGTH // (1024*1024) }} MB</td></tr>
                        </tbody>
                    </table>

                    <p style="margin-top: 20px;">
                        <a href="/api/config-status">View JSON Config API</a> | 
                        <a href="/api/users">View Users API</a>
                    </p>
                </div>
            </body>
            </html>
        """)

    @app.route('/api/config-status')
    def config_status():
        """Returns JSON representation of active configuration settings."""
        return jsonify({
            "environment": app.config.get('ENV_NAME'),
            "debug": app.config.get('DEBUG'),
            "testing": app.config.get('TESTING'),
            "database_uri": app.config.get('SQLALCHEMY_DATABASE_URI'),
            "max_upload_bytes": app.config.get('MAX_CONTENT_LENGTH')
        }), 200

    @app.route('/api/users')
    def list_users():
        """Returns list of users from active database."""
        users = db.session.execute(db.select(User)).scalars().all()
        return jsonify([u.to_dict() for u in users]), 200

    return app


# =============================================================================
# 5. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    # Determine configuration mode from environment variable or default to DevConfig
    env_choice = os.environ.get('FLASK_CONFIG', 'development')
    app = create_app(env_choice)

    print("=" * 75)
    print(f"🚀 Starting Day 12 Factory Application in [{env_choice.upper()}] mode...")
    print("🌐 Status UI at: http://127.0.0.1:5000/")
    print("📡 Config API at: http://127.0.0.1:5000/api/config-status")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=app.config['DEBUG'])
