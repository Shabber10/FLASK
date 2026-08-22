from flask import Blueprint, Response

metrics_bp = Blueprint("metrics_v1", __name__)

try:
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram
    
    REQUEST_COUNT = Counter(
        "flask_http_requests_total",
        "Total HTTP Requests",
        ["method", "endpoint", "status"]
    )
    REQUEST_LATENCY = Histogram(
        "flask_http_request_duration_seconds",
        "HTTP Request Latency",
        ["endpoint"]
    )
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False


@metrics_bp.route("/metrics", methods=["GET"])
def prometheus_metrics():
    """Expose Prometheus observability metrics."""
    if PROMETHEUS_AVAILABLE:
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    return Response(
        "# Prometheus metrics exporter (prometheus_client not installed in local environment)\nflask_http_requests_total 1\n",
        mimetype="text/plain"
    )
