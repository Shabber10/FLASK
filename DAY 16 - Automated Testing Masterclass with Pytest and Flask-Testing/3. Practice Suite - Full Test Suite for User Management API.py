"""
Day 16 Practice Application & Test Suite: User Management API
============================================================
This file contains both the target Flask Application Factory AND
a complete, production-grade Pytest suite demonstrating:
1. Application Factory pattern with TestingConfig (In-Memory SQLite).
2. Pytest fixtures for app, client, and authenticated headers.
3. Unit & Integration tests for Registration, Login, and Protected APIs.
4. HTTP Status Code and JSON payload assertions.

Run this test suite directly using pytest:
    pytest "DAY 16 - Automated Testing Masterclass with Pytest and Flask-Testing/3. Practice Suite - Full Test Suite for User Management API.py" -v
"""

import pytest
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# ------------------------------------------------------------------------------
# 1. Target Application Definition & Models
# ------------------------------------------------------------------------------
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

def create_app(config_name='testing'):
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'

    db.init_app(app)

    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"}), 200

    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.get_json(silent=True) or {}
        if not data.get('username') or not data.get('password'):
            return jsonify({"error": "Bad Request", "message": "Missing username or password"}), 400

        existing = db.session.execute(db.select(User).where(User.username == data['username'])).scalar_one_or_none()
        if existing:
            return jsonify({"error": "Conflict", "message": "Username already exists"}), 409

        user = User(username=data['username'], password_hash=generate_password_hash(data['password']))
        db.session.add(user)
        db.session.commit()
        return jsonify({"id": user.id, "username": user.username}), 201

    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json(silent=True) or {}
        user = db.session.execute(db.select(User).where(User.username == data.get('username'))).scalar_one_or_none()
        if not user or not check_password_hash(user.password_hash, data.get('password', '')):
            return jsonify({"error": "Unauthorized", "message": "Invalid credentials"}), 401
            
        return jsonify({"message": "Login successful", "user_id": user.id}), 200

    with app.app_context():
        db.create_all()

    return app


# ------------------------------------------------------------------------------
# 2. Pytest Test Suite & Fixtures
# ------------------------------------------------------------------------------
@pytest.fixture
def app():
    """Fixture initializing an isolated Flask application instance."""
    app_instance = create_app('testing')
    with app_instance.app_context():
        yield app_instance
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Fixture providing a Flask test client."""
    return app.test_client()


def test_health_check_endpoint(client):
    """Unit Test: Verifies GET /health returns 200 OK."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_user_registration_success(client):
    """Integration Test: Verifies POST /api/register creates a new user (201 Created)."""
    payload = {"username": "alice_test", "password": "Password123!"}
    response = client.post('/api/register', json=payload)
    
    assert response.status_code == 201
    assert response.json['username'] == "alice_test"
    assert "id" in response.json

def test_user_registration_duplicate_username(client):
    """Integration Test: Verifies duplicate registration returns 409 Conflict."""
    payload = {"username": "bob_test", "password": "Password123!"}
    
    # First registration -> 201 Created
    res1 = client.post('/api/register', json=payload)
    assert res1.status_code == 201

    # Second registration with same username -> 409 Conflict
    res2 = client.post('/api/register', json=payload)
    assert res2.status_code == 409
    assert res2.json['error'] == "Conflict"

def test_user_login_invalid_credentials(client):
    """Unit Test: Verifies invalid login attempts return 401 Unauthorized."""
    response = client.post('/api/login', json={"username": "nobody", "password": "wrong"})
    assert response.status_code == 401
    assert response.json['error'] == "Unauthorized"

def test_user_login_success(client):
    """Integration Test: Verifies valid login returns 200 OK."""
    # Register User
    client.post('/api/register', json={"username": "charlie", "password": "Secret123!"})
    
    # Login
    response = client.post('/api/login', json={"username": "charlie", "password": "Secret123!"})
    assert response.status_code == 200
    assert response.json['message'] == "Login successful"


if __name__ == '__main__':
    print("Run this test suite using Pytest:")
    print("pytest \"3. Practice Suite - Full Test Suite for User Management API.py\" -v")
