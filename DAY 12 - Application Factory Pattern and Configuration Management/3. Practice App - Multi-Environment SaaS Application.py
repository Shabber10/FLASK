"""
Day 12 Practice Application: Multi-Environment Application Factory
================================================--------------------
This application demonstrates:
1. Writing a production-grade Application Factory function (create_app).
2. Implementing class-based configuration inheritance (Dev, Testing, Prod).
3. Using the deferred extension initialization pattern (init_app).
4. Registering Blueprints dynamically inside the factory.
5. Providing an interactive Web UI displaying active configuration settings.
"""

import os
from flask import Flask, Blueprint, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# ------------------------------------------------------------------------------
# 1. Unbound Extension Instances (extensions.py)
# ------------------------------------------------------------------------------
db = SQLAlchemy()
csrf = CSRFProtect()


# ------------------------------------------------------------------------------
# 2. Configuration Classes (config.py)
# ------------------------------------------------------------------------------
class BaseConfig:
    """Base Configuration holding common settings."""
    APP_NAME = "Enterprise SaaS Platform"
    SECRET_KEY = os.environ.get('SECRET_KEY', 'day12-factory-secret-key-30-days')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB Limit


class DevelopmentConfig(BaseConfig):
    """Development Environment Configuration."""
    ENV_NAME = "Development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_saas.db'
    SQLALCHEMY_ECHO = True


class TestingConfig(BaseConfig):
    """Testing Environment Configuration."""
    ENV_NAME = "Testing"
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(BaseConfig):
    """Production Environment Configuration."""
    ENV_NAME = "Production"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///prod_saas.db')
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 20, 'pool_pre_ping': True}


config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


# ------------------------------------------------------------------------------
# 3. Sample Model & Blueprint
# ------------------------------------------------------------------------------
class Tenant(db.Model):
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subdomain = db.Column(db.String(50), unique=True, nullable=False)

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    config_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Day 12 Application Factory Masterclass</title>
        <style>
            body { font-family: Arial, sans-serif; background: #eef2f5; margin: 30px; }
            .card { max-width: 850px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            .badge { padding: 5px 10px; border-radius: 4px; color: white; font-weight: bold; }
            .badge-dev { background: #e67e22; }
            .badge-prod { background: #27ae60; }
            .badge-test { background: #2980b9; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 10px; border-bottom: 1px solid #ddd; text-align: left; }
            th { background: #2c3e50; color: white; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🏭 Application Factory & Config Management (Day 12)</h2>
            <p>Active Environment: 
                <span class="badge {% if config.ENV_NAME == 'Development' %}badge-dev{% elif config.ENV_NAME == 'Production' %}badge-prod{% else %}badge-test{% endif %}">
                    {{ config.ENV_NAME }}
                </span>
            </p>

            <h3>Active Application Settings</h3>
            <table>
                <thead>
                    <tr>
                        <th>Configuration Key</th>
                        <th>Resolved Setting Value</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><code>APP_NAME</code></td><td>{{ config.APP_NAME }}</td></tr>
                    <tr><td><code>DEBUG</code></td><td><code>{{ config.DEBUG }}</code></td></tr>
                    <tr><td><code>TESTING</code></td><td><code>{{ config.TESTING }}</code></td></tr>
                    <tr><td><code>SQLALCHEMY_DATABASE_URI</code></td><td><code>{{ config.SQLALCHEMY_DATABASE_URI }}</code></td></tr>
                    <tr><td><code>SECRET_KEY</code></td><td><code>{{ config.SECRET_KEY[:10] }}... (Masked)</code></td></tr>
                    <tr><td><code>MAX_CONTENT_LENGTH</code></td><td>{{ config.MAX_CONTENT_LENGTH }} bytes</td></tr>
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return render_template_string(config_html)

@main_bp.route('/api/config')
def config_api():
    return jsonify({
        "environment": app.config['ENV_NAME'],
        "debug": app.config['DEBUG'],
        "testing": app.config['TESTING'],
        "database": app.config['SQLALCHEMY_DATABASE_URI']
    })


# ------------------------------------------------------------------------------
# 4. Application Factory Function
# ------------------------------------------------------------------------------
def create_app(config_name='development'):
    """Application Factory: Produces isolated, fully configured Flask instances."""
    app = Flask(__name__)
    
    # 1. Load Configuration Object
    selected_config = config_map.get(config_name, DevelopmentConfig)
    app.config.from_object(selected_config)
    
    # 2. Deferred Extension Initialization
    db.init_app(app)
    csrf.init_app(app)
    
    # 3. Register Blueprints
    app.register_blueprint(main_bp)
    
    # 4. Create Tables inside App Context
    with app.app_context():
        db.create_all()
        
    return app


# Create default development app instance for CLI / WSGI servers
app = create_app(os.environ.get('FLASK_ENV', 'development'))


if __name__ == '__main__':
    print("=" * 70)
    print(f"Starting Day 12 Factory Application in [{app.config['ENV_NAME']}] Mode...")
    print("Dashboard UI at http://127.0.0.1:5000/")
    print("Config API at http://127.0.0.1:5000/api/config")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000)
