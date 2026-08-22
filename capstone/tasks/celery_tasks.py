import time
from datetime import datetime, timezone
from capstone.extensions import celery_app, db
from capstone.models.task import AsyncTaskRecord
from capstone.models.user import TokenBlocklist
from sqlalchemy import delete


@celery_app.task(bind=True, name="tasks.generate_pdf_report")
def generate_pdf_report(self, user_id: int, report_title: str):
    """
    Simulate generating an extensive PDF analytics report asynchronously.
    Updates DB status and can emit WebSocket events.
    """
    task_id = self.request.id if self.request else "local-eager-id"
    
    # Update DB task state to IN_PROGRESS
    record = db.session.get(AsyncTaskRecord, task_id)
    if record:
        record.status = "PROCESSING"
        db.session.commit()

    # Emulate work steps
    for step in range(1, 3):
        try:
            self.update_state(state="PROGRESS", meta={"step": step, "total": 2})
        except Exception:
            pass  # In memory/eager testing backend without live Redis

    result_payload = f"Report '{report_title}' generated successfully for user_id={user_id}. File size: 2.4MB."
    
    if record:
        record.status = "SUCCESS"
        record.result = result_payload
        record.completed_at = datetime.now(timezone.utc)
        db.session.commit()

    return {"status": "SUCCESS", "message": result_payload}


@celery_app.task(bind=True, name="tasks.send_async_email")
def send_async_email(self, recipient: str, subject: str, body: str):
    """
    Simulate sending transactional email asynchronously.
    """
    return {
        "status": "SENT",
        "recipient": recipient,
        "subject": subject,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@celery_app.task(name="tasks.cleanup_expired_tokens")
def cleanup_expired_tokens():
    """
    Periodic maintenance task to delete expired JWT tokens from blocklist.
    """
    now = datetime.now(timezone.utc)
    stmt = delete(TokenBlocklist).where(TokenBlocklist.expires_at < now)
    result = db.session.execute(stmt)
    db.session.commit()
    return {"deleted_tokens": result.rowcount}
