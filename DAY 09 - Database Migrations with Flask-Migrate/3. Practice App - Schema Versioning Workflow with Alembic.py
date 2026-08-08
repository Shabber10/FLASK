# Day 09 Practice App: Flask-Migrate Initialization Setup
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///migrations_demo.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

if __name__ == '__main__':
    app.run(debug=True)
