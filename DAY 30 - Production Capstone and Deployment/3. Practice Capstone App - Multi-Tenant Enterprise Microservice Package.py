"""
===============================================================================
Day 30 Grand Finale Capstone: Enterprise Multi-Tenant Microservice Package
===============================================================================
This Capstone application starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Defining SQLAlchemy ORM Models (`Tenant`, `User`, `AuditLog`).
2. STEP 2: Modular Blueprints (`api_bp`, `health_bp` with Kubernetes `/healthz` & `/readyz` probes).
3. STEP 3: Application Factory (`create_app('production')`) attaching `Flask-Talisman` and correlation middleware (`X-Request-ID`).
4. STEP 4: In-memory database seeding routine (Acme Enterprise & Global Tech Logistics).
5. STEP 5: Interactive Capstone Enterprise Dashboard rendering `templates/index.html`.

How to run this Capstone app:
1. Open your terminal in this directory.
2. Run: python "3. Practice Capstone App - Multi-Tenant Enterprise Microservice Package.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import time
import uuid
import datetime
import logging
import json
from flask import Flask, jsonify, request, g, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

db = SQLAlchemy()


# =============================================================================
# STEP 1: ORM Models (Tenant 1 <---> N User 1 <---> N AuditLog)
# =============================================================================
class Tenant(db.Model):
    """Step 1a: Tenant organization model."""
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    users = db.relationship('User', backref='tenant', lazy=True)


class User(db.Model):
    """Step 1b: User account model linked to Tenant."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(50), default='Member')
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    logs = db.relationship('AuditLog', backref='user', lazy=True)


class AuditLog(db.Model):
    """Step 1c: Audit log record model."""
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


# =============================================================================
# STEP 2: Modular Blueprints & Kubernetes Health Probes
# =============================================================================
api_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')
health_bp = Blueprint('health', __name__)


@health_bp.route('/healthz', methods=['GET'])
def liveness():
    """Step 2a: Kubernetes Liveness Probe."""
    return jsonify({
        "status": "UP",
        "service": "Masterclass-Capstone-API",
        "version": "3.0.0",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }), 200


@health_bp.route('/readyz', methods=['GET'])
def readiness():
    """Step 2b: Kubernetes Readiness Probe checking Database Connectivity."""
    try:
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            "status": "READY",
            "database": "CONNECTED",
            "cache": "ACTIVE"
        }), 200
    except Exception as e:
        return jsonify({"status": "NOT_READY", "error": str(e)}), 503


@api_bp.route('/tenants', methods=['GET'])
def list_tenants():
    """Step 2c: REST API list all tenants."""
    tenants = Tenant.query.all()
    return jsonify({
        "status": "success",
        "tenants": [{"id": t.id, "name": t.name, "users_count": len(t.users)} for t in tenants]
    }), 200


@api_bp.route('/tenants/<int:tenant_id>/users', methods=['GET'])
def list_tenant_users(tenant_id):
    """Step 2d: REST API list users for specific tenant."""
    tenant = Tenant.query.get(tenant_id)
    if not tenant:
        return jsonify({"error": f"Tenant #{tenant_id} not found"}), 404
    return jsonify({
        "status": "success",
        "tenant": tenant.name,
        "users": [{"id": u.id, "username": u.username, "role": u.role} for u in tenant.users]
    }), 200


# =============================================================================
# STEP 3: Application Factory (`create_app`)
# =============================================================================
def create_app(config_mode='production'):
    """Step 3: Application Factory initializing security, middleware, and blueprints."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'day30-capstone-masterclass-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Attach Security Hardening (Flask-Talisman)
    csp = {
        'default-src': "'self'",
        'script-src': ["'self'", "'unsafe-inline'", 'https://cdn.jsdelivr.net'],
        'style-src': ["'self'", "'unsafe-inline'", 'https://fonts.googleapis.com']
    }
    Talisman(app, content_security_policy=csp, force_https=False, frame_options='DENY')

    # Attach Correlation ID Middleware
    @app.before_request
    def before_req():
        g.start_time = time.time()
        g.correlation_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())

    @app.after_request
    def after_req(response):
        if hasattr(g, 'start_time'):
            elapsed_ms = round((time.time() - g.start_time) * 1000, 2)
            response.headers['X-Response-Time-MS'] = f"{elapsed_ms}ms"
        if hasattr(g, 'correlation_id'):
            response.headers['X-Request-ID'] = g.correlation_id
        return response

    # Attach Centralized Error Handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": {"code": 404, "message": "Endpoint or resource not found"}}), 404

    @app.errorhandler(500)
    def server_error(e):
        app.logger.error(f"Internal Error: {str(e)}", exc_info=True)
        return jsonify({"error": {"code": 500, "message": "Internal Server Error"}}), 500

    # Register Blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp)

    # UI Dashboard Route Handler (render_template)
    @app.route('/')
    def dashboard():
        """Step 5: Renders templates/index.html Capstone Dashboard."""
        return render_template('index.html')

    # Step 4: Seed in-memory database
    with app.app_context():
        db.create_all()
        if Tenant.query.count() == 0:
            t1 = Tenant(name="Acme Enterprise Corp")
            t2 = Tenant(name="Global Tech Logistics")
            db.session.add_all([t1, t2])
            db.session.commit()

            u1 = User(username="admin_alice", role="Tenant Admin", tenant_id=t1.id)
            u2 = User(username="dev_bob", role="Developer", tenant_id=t1.id)
            u3 = User(username="ops_charlie", role="DevOps Lead", tenant_id=t2.id)
            db.session.add_all([u1, u2, u3])
            db.session.commit()

    return app


# Create App Instance
app = create_app()

if __name__ == '__main__':
    print("=" * 75)
    print("🎓 FLASK MASTERCLASS GRAND FINALE CAPSTONE")
    print("🚀 Microservice Server Started!")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("🩺 Liveness Probe at: http://127.0.0.1:5000/healthz")
    print("🩺 Readiness Probe at: http://127.0.0.1:5000/readyz")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
