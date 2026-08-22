from flask import Blueprint, jsonify, current_app
from sqlalchemy import text
from capstone.extensions import db

health_bp = Blueprint("health_v1", __name__)


@health_bp.route("/healthz", methods=["GET"])
def liveness_check():
    """
    Kubernetes Liveness Probe.
    Returns 200 if the web process is running.
    """
    return jsonify({
        "status": "UP",
        "service": "capstone-flask-api",
        "timestamp": current_app.config.get("ENV")
    }), 200


@health_bp.route("/ready", methods=["GET"])
def readiness_check():
    """
    Kubernetes Readiness Probe.
    Verifies connectivity to critical dependencies (PostgreSQL / SQLite Database, Cache).
    Returns 200 OK if healthy, 503 SERVICE UNAVAILABLE if any dependency fails.
    """
    health_status = {
        "status": "UP",
        "database": "UNKNOWN",
        "cache": "UNKNOWN"
    }
    status_code = 200

    # 1. Check Database connection
    try:
        db.session.execute(text("SELECT 1"))
        health_status["database"] = "HEALTHY"
    except Exception as e:
        health_status["database"] = f"UNHEALTHY: {str(e)}"
        health_status["status"] = "DOWN"
        status_code = 503

    # 2. Check Cache
    try:
        from capstone.extensions import cache
        cache.set("_health_check_ping", "pong", timeout=5)
        val = cache.get("_health_check_ping")
        if val == "pong":
            health_status["cache"] = "HEALTHY"
        else:
            health_status["cache"] = "DEGRADED"
    except Exception as e:
        health_status["cache"] = f"UNHEALTHY: {str(e)}"
        health_status["status"] = "DOWN"
        status_code = 503

    return jsonify(health_status), status_code
