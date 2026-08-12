"""
===============================================================================
Day 29 Practice Script: Production Pytest Automation Suite with Fixtures
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Defining ORM Models (`User` and `Task`).
2. STEP 2: Building an Application Factory (`create_app('testing')`) with REST API endpoints.
3. STEP 3: Defining Pytest fixtures (`app_instance`, `client`, `user_headers`) with setup & teardown.
4. STEP 4: Authoring 6 Pytest automated assertion test cases.
5. STEP 5: Interactive Web UI Pytest Runner Dashboard rendering `templates/index.html`.

How to run Pytest on this script:
1. Open your terminal in this directory.
2. Run: python -m pytest "3. Practice Test Suite - Production Pytest Test Suite with Fixtures.py" -v
"""

import pytest
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# =============================================================================
# STEP 1: ORM Models (User 1 <---> N Task)
# =============================================================================
class User(db.Model):
    """Step 1a: User entity model."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


class Task(db.Model):
    """Step 1b: Task entity model."""
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


# =============================================================================
# STEP 2: Application Factory & REST API Routes
# =============================================================================
def create_app(config_type='testing'):
    """Step 2: Application Factory setting up in-memory DB and routes."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'day29-pytest-masterclass-secret'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route('/')
    def home():
        """Renders templates/index.html test runner dashboard."""
        return render_template('index.html')

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

    @app.route('/api/v1/run-tests', methods=['POST'])
    def run_tests_endpoint():
        """API endpoint executing test assertions programmatically for UI dashboard."""
        test_client = app.test_client()
        results = []

        # Run Test 1
        r1 = test_client.get('/api/v1/ping')
        results.append({"test": "test_ping_endpoint", "status": "PASSED" if r1.status_code == 200 else "FAILED"})

        # Run Test 2
        r2 = test_client.post('/api/v1/users', json={"username": "bob", "email": "bob@example.com"})
        results.append({"test": "test_user_registration_success", "status": "PASSED" if r2.status_code == 201 else "FAILED"})

        # Run Test 3
        r3 = test_client.post('/api/v1/users', json={"username": "bob", "email": "bob@example.com"})
        results.append({"test": "test_user_registration_duplicate_fails", "status": "PASSED" if r3.status_code == 409 else "FAILED"})

        passed_count = sum(1 for r in results if r["status"] == "PASSED")
        return jsonify({
            "status": "success",
            "total_tests": len(results),
            "passed": passed_count,
            "failed": len(results) - passed_count,
            "results": results
        }), 200

    return app


# =============================================================================
# STEP 3: Pytest Fixtures (Setup & Teardown)
# =============================================================================
@pytest.fixture(scope='function')
def app_instance():
    """Step 3a: Fixture initializing Flask app and SQLite in-memory database."""
    flask_app = create_app('testing')
    with flask_app.app_context():
        db.create_all()     # Setup fresh DB schema before test
        yield flask_app     # Yield app instance to test function
        db.session.remove()
        db.drop_all()       # Teardown DB schema after test finishes


@pytest.fixture(scope='function')
def client(app_instance):
    """Step 3b: Fixture providing Flask test_client instance."""
    return app_instance.test_client()


@pytest.fixture(scope='function')
def user_headers(client):
    """Step 3c: Fixture creating a test user in DB and returning authorization headers."""
    res = client.post('/api/v1/users', json={"username": "alice", "email": "alice@example.com"})
    assert res.status_code == 201
    user_id = res.get_json()['user']['id']
    return {"X-User-ID": str(user_id), "Content-Type": "application/json"}


# =============================================================================
# STEP 4: Pytest Automated Test Cases
# =============================================================================
def test_ping_endpoint(client):
    """Step 4a: Test 1 - Verify healthcheck endpoint returns HTTP 200 and pong JSON."""
    response = client.get('/api/v1/ping')
    assert response.status_code == 200
    assert response.get_json() == {"status": "success", "ping": "pong"}


def test_user_registration_success(client):
    """Step 4b: Test 2 - Verify valid user registration succeeds with HTTP 201."""
    payload = {"username": "bob", "email": "bob@example.com"}
    response = client.post('/api/v1/users', json=payload)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['status'] == 'success'
    assert json_data['user']['username'] == 'bob'


def test_user_registration_duplicate_fails(client):
    """Step 4c: Test 3 - Verify duplicate username registration fails with HTTP 409 Conflict."""
    payload = {"username": "charlie", "email": "charlie@example.com"}
    res1 = client.post('/api/v1/users', json=payload)
    assert res1.status_code == 201

    res2 = client.post('/api/v1/users', json=payload)
    assert res2.status_code == 409
    assert "already taken" in res2.get_json()['error']


def test_create_task_authenticated(client, user_headers):
    """Step 4d: Test 4 - Verify task creation succeeds when authenticated with headers."""
    payload = {"title": "Write Pytest Test Suite"}
    response = client.post('/api/v1/tasks', json=payload, headers=user_headers)
    assert response.status_code == 201
    assert response.get_json()['task']['title'] == "Write Pytest Test Suite"


def test_create_task_unauthenticated_fails(client):
    """Step 4e: Test 5 - Verify task creation fails with HTTP 401 when X-User-ID header is missing."""
    payload = {"title": "Unauthorized Task"}
    response = client.post('/api/v1/tasks', json=payload)
    assert response.status_code == 401
    assert "Unauthorized" in response.get_json()['error']


def test_get_tasks_list(client, user_headers):
    """Step 4f: Test 6 - Verify fetching user task list returns created tasks."""
    client.post('/api/v1/tasks', json={"title": "Task 1"}, headers=user_headers)
    client.post('/api/v1/tasks', json={"title": "Task 2"}, headers=user_headers)

    response = client.get('/api/v1/tasks', headers=user_headers)
    assert response.status_code == 200
    tasks = response.get_json()['tasks']
    assert len(tasks) == 2
    assert tasks[0]['title'] == "Task 1"
    assert tasks[1]['title'] == "Task 2"


# =============================================================================
# STEP 5: Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    app = create_app('development')
    print("=" * 75)
    print("🚀 Starting Day 29 Pytest Masterclass Dashboard...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("🧪 Run Pytest from terminal: python -m pytest \"3. Practice Test Suite...py\" -v")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
