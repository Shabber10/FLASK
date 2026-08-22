from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_compress import Compress
from flask_marshmallow import Marshmallow
from celery import Celery

# Initialize extensions without app instance (Application Factory Pattern)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cache = Cache()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)
socketio = SocketIO(cors_allowed_origins="*")
cors = CORS()
compress = Compress()
ma = Marshmallow()

celery_app = Celery("capstone_celery")


def init_celery(app, celery):
    """Integrate Celery with Flask application context."""
    celery.conf.update(
        broker_url=app.config.get("CELERY_BROKER_URL"),
        result_backend=app.config.get("CELERY_RESULT_BACKEND"),
        task_ignore_result=False,
        task_track_started=True,
        timezone="UTC",
        task_always_eager=app.config.get("CELERY_TASK_ALWAYS_EAGER", False),
        task_eager_propagates=app.config.get("CELERY_TASK_EAGER_PROPAGATES", False),
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
