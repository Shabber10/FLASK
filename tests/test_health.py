import pytest


@pytest.mark.unit
def test_root_index_endpoint(client):
    """Test root status endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "Operational"
    assert "endpoints" in data


@pytest.mark.unit
def test_liveness_probe(client):
    """Test /api/v1/health/healthz Kubernetes liveness probe."""
    response = client.get("/api/v1/health/healthz")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "UP"
    assert data["service"] == "capstone-flask-api"


@pytest.mark.integration
def test_readiness_probe(client):
    """Test /api/v1/health/ready Kubernetes readiness probe."""
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "UP"
    assert data["database"] == "HEALTHY"
