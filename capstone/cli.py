import click
from flask.cli import with_appcontext
from capstone.extensions import db
from capstone.models.user import User, Role, TokenBlocklist
from capstone.services.auth_service import AuthService
from sqlalchemy import select


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Initialize database tables and create standard roles."""
    db.create_all()
    
    # Seed standard roles
    roles = ["Admin", "User", "Manager", "Auditor"]
    for role_name in roles:
        existing = db.session.execute(select(Role).where(Role.name == role_name)).scalar_one_or_none()
        if not existing:
            db.session.add(Role(name=role_name, description=f"Default {role_name} role"))
    db.session.commit()
    click.echo("✓ Database schema initialized with standard roles.")


@click.command("seed-db")
@click.option("--count", default=10, help="Number of dummy users to generate")
@with_appcontext
def seed_db_command(count):
    """Seed the database with test data using Factory Boy."""
    from capstone.factories.user_factory import UserFactory
    
    click.echo(f"Seeding {count} users into database...")
    for _ in range(count):
        UserFactory.create()
    click.echo(f"✓ Successfully seeded {count} users.")


@click.command("create-admin")
@click.option("--username", prompt=True, help="Admin username")
@click.option("--email", prompt=True, help="Admin email address")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Admin password")
@with_appcontext
def create_admin_command(username, email, password):
    """Create a new superadmin user."""
    user, err = AuthService.register_user(
        username=username,
        email=email,
        password=password,
        is_admin=True
    )
    if err:
        click.echo(f"✗ Failed to create admin: {err}")
    else:
        # Assign Admin role
        admin_role = db.session.execute(select(Role).where(Role.name == "Admin")).scalar_one_or_none()
        if admin_role:
            user.roles.append(admin_role)
            db.session.commit()
        click.echo(f"✓ Administrator '{username}' created successfully!")


def register_cli_commands(app):
    """Register custom CLI commands with Flask application."""
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
    app.cli.add_command(create_admin_command)
