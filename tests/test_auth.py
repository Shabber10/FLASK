import pytest
from capstone.models.user import User


@pytest.mark.integration
def test_user_registration_success(client):
    """Test standard user registration flow."""
    payload = {
        "username": "newdev",
        "email": "newdev@example.com",
        "password": "StrongPassword999!"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User registered successfully"
    assert data["user"]["username"] == "newdev"
    assert data["user"]["email"] == "newdev@example.com"


@pytest.mark.integration
def test_user_registration_duplicate(client, regular_user):
    """Test duplicate registration rejection."""
    payload = {
        "username": regular_user.username,
        "email": "different@example.com",
        "password": "AnotherPassword123!"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 409
    assert "already registered" in response.get_json()["message"]


@pytest.mark.integration
def test_user_registration_invalid_payload(client):
    """Test validation errors on bad input."""
    response = client.post("/api/v1/auth/register", json={"username": "short"})
    assert response.status_code == 422


@pytest.mark.integration
def test_user_login_success(client, regular_user):
    """Test successful user login and JWT token pair generation."""
    response = client.post("/api/v1/auth/login", json={
        "username": regular_user.username,
        "password": "TestPassword123!"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["username"] == regular_user.username


@pytest.mark.integration
def test_user_login_invalid_password(client, regular_user):
    """Test login failure on incorrect password."""
    response = client.post("/api/v1/auth/login", json={
        "username": regular_user.username,
        "password": "WrongPassword!"
    })
    assert response.status_code == 401
    assert "Invalid username or password" in response.get_json()["message"]


@pytest.mark.integration
def test_get_current_user_profile(client, auth_headers, regular_user):
    """Test authenticated profile endpoint."""
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["user"]["username"] == regular_user.username


@pytest.mark.integration
def test_logout_and_token_revocation(client, regular_user):
    """Test that logging out revokes the access token."""
    # 1. Login to get token
    login_resp = client.post("/api/v1/auth/login", json={
        "username": regular_user.username,
        "password": "TestPassword123!"
    })
    token = login_resp.get_json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Verify token works
    assert client.get("/api/v1/auth/me", headers=headers).status_code == 200

    # 3. Perform logout
    logout_resp = client.post("/api/v1/auth/logout", headers=headers)
    assert logout_resp.status_code == 200

    # 4. Verify token is now rejected as revoked
    me_resp = client.get("/api/v1/auth/me", headers=headers)
    assert me_resp.status_code == 401
    assert "revoked" in me_resp.get_json()["message"].lower()
