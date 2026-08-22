import pytest
from capstone.tasks.celery_tasks import send_async_email, cleanup_expired_tokens


@pytest.mark.celery
def test_dispatch_report_task(client, auth_headers):
    """Test dispatching PDF report task."""
    response = client.post(
        "/api/v1/tasks/report",
        json={"title": "Annual Executive Summary"},
        headers=auth_headers
    )
    assert response.status_code == 202
    data = response.get_json()
    assert "task_id" in data
    assert "poll_url" in data


@pytest.mark.celery
def test_dispatch_email_task(client, auth_headers):
    """Test dispatching background email task."""
    response = client.post(
        "/api/v1/tasks/email",
        json={
            "recipient": "customer@enterprise.com",
            "subject": "Invoice Paid",
            "body": "Thank you for your payment."
        },
        headers=auth_headers
    )
    assert response.status_code == 202
    data = response.get_json()
    assert data["status"] == "QUEUED"


@pytest.mark.celery
def test_direct_celery_task_execution():
    """Test direct synchronous/eager execution of Celery worker functions."""
    result = send_async_email("user@domain.com", "Test Subject", "Body content")
    assert result["status"] == "SENT"
    assert result["recipient"] == "user@domain.com"


@pytest.mark.celery
def test_cleanup_expired_tokens_task(db_session):
    """Test token cleanup periodic maintenance task."""
    res = cleanup_expired_tokens()
    assert "deleted_tokens" in res
