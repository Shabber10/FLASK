import os
from flask import Flask, jsonify
from capstone.config import config_by_name
from capstone.extensions import (
    db, migrate, jwt, cache, limiter, socketio, cors, compress, ma, celery_app, init_celery
)
from capstone.models.user import TokenBlocklist
from capstone.api.v1 import api_v1
from capstone.cli import register_cli_commands
import capstone.sockets.events  # Register WebSocket event listeners


def create_app(config_name: str = None) -> Flask:
    """
    Application Factory for Enterprise Flask Capstone App.
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", os.environ.get("ENV", "development"))

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["default"]))

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    cors.init_app(app)
    compress.init_app(app)
    ma.init_app(app)
    socketio.init_app(app)

    # Initialize Celery
    init_celery(app, celery_app)

    # JWT Token Revocation Check
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "error": "Unauthorized",
            "message": "Token has been revoked. Please log in again."
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "error": "Unauthorized",
            "message": "Token has expired."
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "error": "Unauthorized",
            "message": f"Signature verification failed: {error}"
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "error": "Unauthorized",
            "message": "Request does not contain an access token."
        }), 401

    # Standard JSON Error Handlers
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad Request", "message": str(e)}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not Found", "message": "The requested resource was not found"}), 404

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({"error": "Too Many Requests", "message": f"Rate limit exceeded: {e.description}"}), 429

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500

    # Register Blueprints
    app.register_blueprint(api_v1)

    # Register CLI Commands
    register_cli_commands(app)

    # Root Welcome Endpoint
    @app.route("/", methods=["GET"])
    def index():
        return jsonify({
            "title": "30-Day Enterprise Flask Masterclass - Capstone Service",
            "version": "1.0.0",
            "status": "Operational",
            "api_v1_docs": "/api/v1/health/ready",
            "endpoints": {
                "auth": "/api/v1/auth",
                "users": "/api/v1/users",
                "tasks": "/api/v1/tasks",
                "media": "/api/v1/media",
                "health": "/api/v1/health/healthz",
                "metrics": "/api/v1/metrics"
            }
        }), 200

    return app
