import os
from capstone import create_app
from capstone.extensions import socketio

env = os.environ.get("FLASK_ENV", "development")
app = create_app(env)

if __name__ == "__main__":
    # In local development, run with SocketIO server
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, debug=app.config.get("DEBUG", True))
