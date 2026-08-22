from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy import select
from capstone.extensions import db
from capstone.models.task import AsyncTaskRecord


class TaskService:
    """Service managing async task lifecycle and database persistence."""

    @staticmethod
    def create_task_record(task_id: str, name: str, user_id: Optional[int] = None, meta_data: Optional[dict] = None) -> AsyncTaskRecord:
        """Create a new pending async task record in DB."""
        record = AsyncTaskRecord(
            id=task_id,
            name=name,
            status="PENDING",
            user_id=user_id,
            meta_data=meta_data or {}
        )
        db.session.add(record)
        db.session.commit()
        return record

    @staticmethod
    def update_task_status(task_id: str, status: str, result: Optional[str] = None, error: Optional[str] = None) -> Optional[AsyncTaskRecord]:
        """Update the status of an existing async task."""
        record = db.session.execute(
            select(AsyncTaskRecord).where(AsyncTaskRecord.id == task_id)
        ).scalar_one_or_none()

        if record:
            record.status = status
            if result:
                record.result = result
            if error:
                record.error = error
            if status in ("SUCCESS", "FAILURE", "REVOKED"):
                record.completed_at = datetime.now(timezone.utc)
            db.session.commit()
        return record

    @staticmethod
    def get_task(task_id: str) -> Optional[AsyncTaskRecord]:
        """Retrieve task record by task ID."""
        return db.session.execute(
            select(AsyncTaskRecord).where(AsyncTaskRecord.id == task_id)
        ).scalar_one_or_none()
