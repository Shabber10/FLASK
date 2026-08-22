import io
import pytest


@pytest.mark.integration
def test_list_users_paginated(client, auth_headers, regular_user, admin_user):
    """Test user listing with pagination."""
    response = client.get("/api/v1/users?page=1&per_page=10", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert "users" in data
    assert len(data["users"]) >= 2


@pytest.mark.integration
def test_get_user_by_id(client, auth_headers, regular_user):
    """Test get user details by id."""
    response = client.get(f"/api/v1/users/{regular_user.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["user"]["id"] == regular_user.id


@pytest.mark.integration
def test_update_user_profile(client, auth_headers, regular_user):
    """Test updating user profile email."""
    response = client.put(
        f"/api/v1/users/{regular_user.id}",
        json={"email": "updated_email@example.com"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.get_json()["user"]["email"] == "updated_email@example.com"


@pytest.mark.integration
def test_admin_delete_user(client, admin_headers, regular_user):
    """Test admin deleting a user account."""
    response = client.delete(f"/api/v1/users/{regular_user.id}", headers=admin_headers)
    assert response.status_code == 200
    assert "deleted successfully" in response.get_json()["message"]


@pytest.mark.integration
def test_regular_user_cannot_delete(client, auth_headers, regular_user):
    """Test non-admin cannot delete user."""
    response = client.delete(f"/api/v1/users/{regular_user.id}", headers=auth_headers)
    assert response.status_code == 403


@pytest.mark.integration
def test_media_upload_valid_file(client, auth_headers):
    """Test uploading a valid text/csv file."""
    data = {
        "file": (io.BytesIO(b"id,name\n1,Alice\n2,Bob"), "test_data.csv")
    }
    response = client.post(
        "/api/v1/media/upload",
        data=data,
        content_type="multipart/form-data",
        headers=auth_headers
    )
    assert response.status_code == 201
    result = response.get_json()
    assert "file" in result
    assert result["file"]["extension"] == "csv"


@pytest.mark.integration
def test_media_upload_invalid_extension(client, auth_headers):
    """Test uploading an executable/forbidden file."""
    data = {
        "file": (io.BytesIO(b"binary payload"), "malicious.exe")
    }
    response = client.post(
        "/api/v1/media/upload",
        data=data,
        content_type="multipart/form-data",
        headers=auth_headers
    )
    assert response.status_code == 422
