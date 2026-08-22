from capstone.models.user import User, Role
from capstone.extensions import db

try:
    import factory

    class RoleFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Role
            sqlalchemy_session = db.session
            sqlalchemy_session_persistence = "commit"

        name = factory.Sequence(lambda n: f"Role_{n}")
        description = factory.Faker("sentence", nb_words=4)

    class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = User
            sqlalchemy_session = db.session
            sqlalchemy_session_persistence = "commit"

        username = factory.Sequence(lambda n: f"user_{n}")
        email = factory.Sequence(lambda n: f"user_{n}@enterprise-flask.dev")
        is_active = True
        is_admin = False

        @classmethod
        def _create(cls, model_class, *args, **kwargs):
            password = kwargs.pop("password", "SecurePassword123!")
            obj = model_class(*args, **kwargs)
            obj.set_password(password)
            db.session.add(obj)
            db.session.commit()
            return obj

except ImportError:
    # Fallback lightweight generator if factory_boy is not installed
    import itertools
    _user_counter = itertools.count(1)

    class RoleFactory:
        @classmethod
        def create(cls, **kwargs):
            role_name = kwargs.get("name", f"Role_{next(_user_counter)}")
            role = Role(name=role_name, description=kwargs.get("description", "Generated test role"))
            db.session.add(role)
            db.session.commit()
            return role

    class UserFactory:
        @classmethod
        def create(cls, **kwargs):
            n = next(_user_counter)
            user = User(
                username=kwargs.get("username", f"user_{n}"),
                email=kwargs.get("email", f"user_{n}@enterprise-flask.dev"),
                is_active=kwargs.get("is_active", True),
                is_admin=kwargs.get("is_admin", False)
            )
            user.set_password(kwargs.get("password", "SecurePassword123!"))
            db.session.add(user)
            db.session.commit()
            return user
