import pytest
from capstone import create_app
from capstone.extensions import db as _db, socketio
from capstone.models.user import User, Role
from capstone.services.auth_service import AuthService
from flask_jwt_extended import create_access_token
from sqlalchemy import select


@pytest.fixture(scope="session")
def app():
    """Create test application instance configured for testing."""
    app = create_app("testing")
    return app


@pytest.fixture(scope="function")
def db_session(app):
    """Provide isolated database session for each test function."""
    with app.app_context():
        _db.create_all()
        
        # Initialize default roles safely if not existing
        for role_name, role_desc in [("Admin", "Administrator Role"), ("User", "Standard User Role")]:
            existing = _db.session.execute(select(Role).where(Role.name == role_name)).scalar_one_or_none()
            if not existing:
                _db.session.add(Role(name=role_name, description=role_desc))
        _db.session.commit()

        yield _db.session

        _db.session.rollback()
        _db.drop_all()


@pytest.fixture
def client(app, db_session):
    """Provide Flask test client with database context."""
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


@pytest.fixture
def cli_runner(app):
    """Provide Flask CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def regular_user(db_session):
    """Create and return a standard user."""
    user, _ = AuthService.register_user(
        username="testuser",
        email="testuser@example.com",
        password="TestPassword123!"
    )
    return user


@pytest.fixture
def admin_user(db_session):
    """Create and return an admin user."""
    user, _ = AuthService.register_user(
        username="adminuser",
        email="adminuser@example.com",
        password="AdminPassword123!",
        is_admin=True
    )
    return user


@pytest.fixture
def auth_headers(app, regular_user):
    """Generate JWT authorization headers for a standard user."""
    with app.app_context():
        token = create_access_token(
            identity=str(regular_user.id),
            additional_claims={"is_admin": False, "roles": ["User"]}
        )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(app, admin_user):
    """Generate JWT authorization headers for an admin user."""
    with app.app_context():
        token = create_access_token(
            identity=str(admin_user.id),
            additional_claims={"is_admin": True, "roles": ["Admin"]}
        )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def socket_client(app):
    """Provide SocketIO test client."""
    return socketio.test_client(app)
