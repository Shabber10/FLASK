import pytest
from capstone.factories.user_factory import UserFactory, RoleFactory
from capstone.models.user import User


@pytest.mark.unit
def test_user_factory_generation(db_session):
    """Test generating users via Factory Boy."""
    user = UserFactory.create()
    assert user.id is not None
    assert "@enterprise-flask.dev" in user.email
    assert user.check_password("SecurePassword123!")


@pytest.mark.integration
def test_cli_init_db(cli_runner):
    """Test flask init-db CLI command."""
    result = cli_runner.invoke(args=["init-db"])
    assert result.exit_code == 0
    assert "initialized" in result.output


@pytest.mark.integration
def test_cli_seed_db(cli_runner, db_session):
    """Test flask seed-db CLI command."""
    result = cli_runner.invoke(args=["seed-db", "--count", "5"])
    assert result.exit_code == 0
    assert "Successfully seeded 5 users" in result.output
