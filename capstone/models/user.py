from __future__ import annotations
from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Table, Column
from werkzeug.security import generate_password_hash, check_password_hash
from capstone.extensions import db

if TYPE_CHECKING:
    from capstone.models.task import AsyncTaskRecord


# Association Table for User-Role Many-to-Many Relationship
user_roles = Table(
    "user_roles",
    db.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)


class Role(db.Model):
    """Role model for Role-Based Access Control (RBAC)."""
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    users: Mapped[List[User]] = relationship(
        secondary=user_roles,
        back_populates="roles",
        lazy="selectin"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class User(db.Model):
    """
    Modern SQLAlchemy 2.0 User model with Mapped type annotations.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    roles: Mapped[List[Role]] = relationship(
        secondary=user_roles,
        back_populates="users",
        lazy="selectin"
    )
    tasks: Mapped[List["AsyncTaskRecord"]] = relationship(
        "AsyncTaskRecord",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def set_password(self, password: str) -> None:
        """Hash and set the user password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify the password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name: str) -> bool:
        """Check if user has a specific role."""
        if self.is_admin:
            return True
        return any(role.name == role_name for role in self.roles)

    def to_dict(self) -> dict:
        """Serialize user object to dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "roles": [r.name for r in self.roles],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class TokenBlocklist(db.Model):
    """Token blocklist model for JWT revocation on logout."""
    __tablename__ = "token_blocklist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    jti: Mapped[str] = mapped_column(String(36), nullable=False, unique=True, index=True)
    token_type: Mapped[str] = mapped_column(String(10), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
