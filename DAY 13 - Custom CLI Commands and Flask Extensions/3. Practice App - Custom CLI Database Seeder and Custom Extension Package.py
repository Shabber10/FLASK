# Day 13 Practice App: Custom CLI & Extension Initialization
import click
from flask import Flask, jsonify

class SimpleLoggerExt:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('LOGGER_PREFIX', '[APP_LOG]')
        app.extensions['simple_logger'] = self

    def log(self, message):
        print(f"LOGGER: {message}")

app = Flask(__name__)
logger = SimpleLoggerExt(app)

@app.cli.command("seed")
@click.argument("name")
def seed_command(name):
    logger.log(f"Seeding database for user: {name}")
    click.echo(f"User {name} seeded!")

@app.route('/')
def home():
    logger.log("Home route accessed.")
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
