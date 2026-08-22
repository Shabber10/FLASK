from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, JSON
from capstone.extensions import db

if TYPE_CHECKING:
    from capstone.models.user import User


class AsyncTaskRecord(db.Model):
    """Tracks Celery background asynchronous task execution in DB."""
    __tablename__ = "async_tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)  # Celery Task UUID
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="PENDING", nullable=False, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    meta_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationship
    user: Mapped[Optional[User]] = relationship("User", back_populates="tasks")

    def to_dict(self) -> dict:
        return {
            "task_id": self.id,
            "name": self.name,
            "status": self.status,
            "user_id": self.user_id,
            "meta_data": self.meta_data,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
