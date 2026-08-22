from flask import Blueprint
from capstone.api.v1.auth import auth_bp
from capstone.api.v1.users import users_bp
from capstone.api.v1.tasks import tasks_bp
from capstone.api.v1.media import media_bp
from capstone.api.v1.health import health_bp
from capstone.api.v1.metrics import metrics_bp

# Master API v1 Blueprint
api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

# Register sub-blueprints
api_v1.register_blueprint(auth_bp, url_prefix="/auth")
api_v1.register_blueprint(users_bp, url_prefix="/users")
api_v1.register_blueprint(tasks_bp, url_prefix="/tasks")
api_v1.register_blueprint(media_bp, url_prefix="/media")
api_v1.register_blueprint(health_bp, url_prefix="/health")
api_v1.register_blueprint(metrics_bp)

__all__ = ["api_v1"]
