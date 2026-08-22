from datetime import datetime, timezone
from typing import Optional, Tuple, Dict, Any
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from sqlalchemy import select
from capstone.extensions import db
from capstone.models.user import User, Role, TokenBlocklist
from capstone.models.audit import AuditLog


class AuthService:
    """Service layer handling authentication, token lifecycle, and user management."""

    @staticmethod
    def register_user(username: str, email: str, password: str, is_admin: bool = False) -> Tuple[Optional[User], Optional[str]]:
        """Register a new user account."""
        # Check existing username or email
        existing = db.session.execute(
            select(User).where((User.username == username) | (User.email == email))
        ).scalar_one_or_none()

        if existing:
            if existing.username == username:
                return None, "Username already registered"
            return None, "Email address already registered"

        user = User(
            username=username,
            email=email,
            is_admin=is_admin
        )
        user.set_password(password)

        # Assign default 'User' role if available
        user_role = db.session.execute(select(Role).where(Role.name == "User")).scalar_one_or_none()
        if user_role:
            user.roles.append(user_role)

        db.session.add(user)
        db.session.commit()
        return user, None

    @staticmethod
    def authenticate(username_or_email: str, password: str, ip_address: Optional[str] = None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Authenticate user credentials and return JWT token pair."""
        user = db.session.execute(
            select(User).where(
                (User.username == username_or_email) | (User.email == username_or_email)
            )
        ).scalar_one_or_none()

        if not user or not user.check_password(password):
            return None, "Invalid username or password"

        if not user.is_active:
            return None, "User account is deactivated"

        # Generate JWT tokens with custom claims
        additional_claims = {
            "is_admin": user.is_admin,
            "roles": [r.name for r in user.roles]
        }
        access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)

        # Log audit entry
        audit = AuditLog(
            user_id=user.id,
            action="USER_LOGIN_SUCCESS",
            ip_address=ip_address,
            details={"username": user.username}
        )
        db.session.add(audit)
        db.session.commit()

        return {
            "user": user.to_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token
        }, None

    @staticmethod
    def revoke_token(raw_jwt: dict) -> None:
        """Revoke a JWT token by adding its jti to the blocklist."""
        jti = raw_jwt["jti"]
        token_type = raw_jwt["type"]
        user_id = int(raw_jwt["sub"])
        expires_at = datetime.fromtimestamp(raw_jwt["exp"], tz=timezone.utc)

        blocklist_entry = TokenBlocklist(
            jti=jti,
            token_type=token_type,
            user_id=user_id,
            expires_at=expires_at
        )
        db.session.add(blocklist_entry)
        db.session.commit()
