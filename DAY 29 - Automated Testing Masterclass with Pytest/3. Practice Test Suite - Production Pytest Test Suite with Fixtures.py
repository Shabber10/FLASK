"""
===============================================================================
Day 29 Practice Script: Production Pytest Automation Suite with Fixtures
===============================================================================
This script contains BOTH a Flask REST API application AND a complete Pytest
automated test suite in a single self-contained file!

This script demonstrates:
1. Building an Application Factory (`create_app('testing')`).
2. Configuring in-memory SQLite databases for isolated test execution.
3. Defining Pytest fixtures (`app`, `client`, `user_headers`) with setup & teardown.
4. Testing HTTP status codes, JSON responses, and database state changes.
5. Testing authenticated vs unauthenticated access control.

How to run Pytest on this script:
1. Open your terminal in this directory.
2. Run: python -m pytest "3. Practice Test Suite - Production Pytest Test Suite with Fixtures.py" -v
"""

import pytest
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# =============================================================================
# 1. ORM Models (User 1 <---> N Task)
# =============================================================================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


# =============================================================================
# 2. Application Factory & REST API Routes
# =============================================================================
def create_app(config_type='testing'):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'day29-pytest-masterclass-secret'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route('/api/v1/ping', methods=['GET'])
    def ping():
        return jsonify({"status": "success", "ping": "pong"}), 200

    @app.route('/api/v1/users', methods=['POST'])
    def register_user():
        data = request.get_json() or {}
        username = data.get('username')
        email = data.get('email')

        if not username or not email:
            return jsonify({"error": "Fields 'username' and 'email' are required"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": f"Username '{username}' is already taken"}), 409

        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify({"status": "success", "user": {"id": user.id, "username": user.username}}), 201

    @app.route('/api/v1/tasks', methods=['POST'])
    def create_task():
        user_id = request.headers.get('X-User-ID', type=int)
        if not user_id or not User.query.get(user_id):
            return jsonify({"error": "Unauthorized: Valid X-User-ID header required"}), 401

        data = request.get_json() or {}
        title = data.get('title')
        if not title:
            return jsonify({"error": "Field 'title' is required"}), 400

        task = Task(title=title, user_id=user_id)
        db.session.add(task)
        db.session.commit()
        return jsonify({"status": "success", "task": {"id": task.id, "title": task.title}}), 201

    @app.route('/api/v1/tasks', methods=['GET'])
    def list_tasks():
        user_id = request.headers.get('X-User-ID', type=int)
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        tasks = Task.query.filter_by(user_id=user_id).all()
        return jsonify({
            "status": "success",
            "tasks": [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]
        }), 200

    return app


# =============================================================================
# 3. Pytest Fixtures (Setup & Teardown)
# =============================================================================

@pytest.fixture(scope='function')
def app_instance():
    """Fixture initializing Flask app and SQLite in-memory database."""
    flask_app = create_app('testing')
    with flask_app.app_context():
        db.create_all()     # Setup fresh DB schema before test
        yield flask_app     # Yield app instance to test function
        db.session.remove()
        db.drop_all()       # Teardown DB schema after test finishes


@pytest.fixture(scope='function')
def client(app_instance):
    """Fixture providing Flask test_client instance."""
    return app_instance.test_client()


@pytest.fixture(scope='function')
def user_headers(client):
    """Fixture creating a test user in DB and returning authorization headers."""
    res = client.post('/api/v1/users', json={"username": "alice", "email": "alice@example.com"})
    assert res.status_code == 201
    user_id = res.get_json()['user']['id']
    return {"X-User-ID": str(user_id), "Content-Type": "application/json"}


# =============================================================================
# 4. Pytest Automated Test Cases
# =============================================================================

def test_ping_endpoint(client):
    """Test 1: Verify healthcheck endpoint returns HTTP 200 and pong JSON."""
    response = client.get('/api/v1/ping')
    assert response.status_code == 200
    assert response.get_json() == {"status": "success", "ping": "pong"}


def test_user_registration_success(client):
    """Test 2: Verify valid user registration succeeds with HTTP 201."""
    payload = {"username": "bob", "email": "bob@example.com"}
    response = client.post('/api/v1/users', json=payload)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['status'] == 'success'
    assert json_data['user']['username'] == 'bob'


def test_user_registration_duplicate_fails(client):
    """Test 3: Verify duplicate username registration fails with HTTP 409 Conflict."""
    payload = {"username": "charlie", "email": "charlie@example.com"}
    res1 = client.post('/api/v1/users', json=payload)
    assert res1.status_code == 201

    res2 = client.post('/api/v1/users', json=payload)
    assert res2.status_code == 409
    assert "already taken" in res2.get_json()['error']


def test_create_task_authenticated(client, user_headers):
    """Test 4: Verify task creation succeeds when authenticated with headers."""
    payload = {"title": "Write Pytest Test Suite"}
    response = client.post('/api/v1/tasks', json=payload, headers=user_headers)
    assert response.status_code == 201
    assert response.get_json()['task']['title'] == "Write Pytest Test Suite"


def test_create_task_unauthenticated_fails(client):
    """Test 5: Verify task creation fails with HTTP 401 when X-User-ID header is missing."""
    payload = {"title": "Unauthorized Task"}
    response = client.post('/api/v1/tasks', json=payload)
    assert response.status_code == 401
    assert "Unauthorized" in response.get_json()['error']


def test_get_tasks_list(client, user_headers):
    """Test 6: Verify fetching user task list returns created tasks."""
    client.post('/api/v1/tasks', json={"title": "Task 1"}, headers=user_headers)
    client.post('/api/v1/tasks', json={"title": "Task 2"}, headers=user_headers)

    response = client.get('/api/v1/tasks', headers=user_headers)
    assert response.status_code == 200
    tasks = response.get_json()['tasks']
    assert len(tasks) == 2
    assert tasks[0]['title'] == "Task 1"
    assert tasks[1]['title'] == "Task 2"
