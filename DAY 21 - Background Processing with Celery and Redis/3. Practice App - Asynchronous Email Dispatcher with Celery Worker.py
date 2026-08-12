"""
===============================================================================
Day 21 Practice Script: Asynchronous Background Processing Engine
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Configuring Celery with Flask (`celery_init_app()`).
2. STEP 2: Fallback In-Memory Task Simulator (`InMemoryTaskStore`) ensuring script runs without Redis.
3. STEP 3: Defining background tasks (`@celery_app.task`).
4. STEP 4: Triggering background tasks (`.delay()` and `.apply_async()`) returning HTTP 202 Accepted.
5. STEP 5: Polling task execution states (`AsyncResult`) from Redis / Fallback Store.
6. STEP 6: Interactive Web UI background job management dashboard rendering `templates/index.html`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Asynchronous Email Dispatcher with Celery Worker.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import time
import uuid
from threading import Thread
from flask import Flask, jsonify, request, render_template
from celery import Celery, Task

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day21-celery-masterclass-secret'

# Configure Redis Broker and Result Backend
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/0",
        task_ignore_result=False,
    ),
)


# =============================================================================
# STEP 1: Official Flask-Celery Application Factory Helper
# =============================================================================
def celery_init_app(app: Flask) -> Celery:
    """Step 1: Official Flask 2.3+ Celery Integration Factory."""
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config.get("CELERY", {}))
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


celery_app = celery_init_app(app)


# =============================================================================
# STEP 2: Fallback In-Memory Task Simulator (Ensures Script Runs Without Redis)
# =============================================================================
class InMemoryTaskStore:
    """Step 2a: Fallback simulator tracking task states if Redis server is offline."""
    def __init__(self):
        self.tasks = {}

    def create_task(self, task_name, payload):
        task_id = str(uuid.uuid4())
        self.tasks[task_id] = {"state": "PENDING", "name": task_name, "payload": payload, "result": None}
        return task_id

    def update_task(self, task_id, state, result=None):
        if task_id in self.tasks:
            self.tasks[task_id]["state"] = state
            self.tasks[task_id]["result"] = result

    def get_task(self, task_id):
        return self.tasks.get(task_id)


task_store = InMemoryTaskStore()


def simulate_background_execution(task_id, seconds_delay, return_value):
    """Step 2b: Thread simulator executing background work if Redis worker is not running."""
    time.sleep(1)
    task_store.update_task(task_id, "STARTED")
    time.sleep(seconds_delay)
    task_store.update_task(task_id, "SUCCESS", result=return_value)


# =============================================================================
# STEP 3: Background Tasks
# =============================================================================
@celery_app.task(bind=True)
def send_email_task(self, recipient_email, subject_text):
    """Step 3a: Celery background task simulating email dispatch."""
    time.sleep(4)  # Simulate 4-second SMTP network delay
    return f"Email with subject '{subject_text}' successfully delivered to {recipient_email}."


@celery_app.task(bind=True)
def generate_pdf_report_task(self, report_id):
    """Step 3b: Celery background task simulating PDF generation."""
    time.sleep(6)  # Simulate heavy PDF computation
    return f"PDF Report #{report_id} generated and saved to S3 storage."


# =============================================================================
# STEP 4 & 5: REST API Endpoints (Queue Jobs & Poll Status)
# =============================================================================

# POST /api/v1/jobs/send-email -> Queue Email Task
@app.route('/api/v1/jobs/send-email', methods=['POST'])
def trigger_email_job():
    """Step 4a: Queues Email task asynchronously and returns HTTP 202 Accepted."""
    data = request.get_json() or {}
    email = data.get('email', 'user@example.com')
    subject = data.get('subject', 'Welcome to Flask Masterclass!')

    # Try Celery delay queue first; fallback to simulator if Redis offline
    try:
        celery_job = send_email_task.delay(email, subject)
        task_id = celery_job.id
        engine = "Celery + Redis Broker"
    except Exception:
        # Fallback simulator execution
        task_id = task_store.create_task("send_email_task", {"email": email, "subject": subject})
        res_text = f"Email with subject '{subject}' successfully delivered to {email}."
        Thread(target=simulate_background_execution, args=(task_id, 4, res_text)).start()
        engine = "In-Memory Thread Simulator (Redis Offline)"

    return jsonify({
        "status": "accepted",
        "message": "Email job accepted for background processing.",
        "task_id": task_id,
        "engine": engine,
        "status_url": f"/api/v1/jobs/{task_id}"
    }), 202


# POST /api/v1/jobs/generate-report -> Queue Heavy PDF Task
@app.route('/api/v1/jobs/generate-report', methods=['POST'])
def trigger_report_job():
    """Step 4b: Queues heavy PDF Report task asynchronously."""
    report_id = str(uuid.uuid4())[:8]

    try:
        celery_job = generate_pdf_report_task.delay(report_id)
        task_id = celery_job.id
        engine = "Celery + Redis Broker"
    except Exception:
        task_id = task_store.create_task("generate_pdf_report_task", {"report_id": report_id})
        res_text = f"PDF Report #{report_id} generated and saved to S3 storage."
        Thread(target=simulate_background_execution, args=(task_id, 6, res_text)).start()
        engine = "In-Memory Thread Simulator (Redis Offline)"

    return jsonify({
        "status": "accepted",
        "message": "PDF Report generation queued.",
        "task_id": task_id,
        "engine": engine,
        "status_url": f"/api/v1/jobs/{task_id}"
    }), 202


# GET /api/v1/jobs/<task_id> -> Poll Task Status
@app.route('/api/v1/jobs/<task_id>', methods=['GET'])
def get_job_status(task_id):
    """Step 5: Queries task state (PENDING, STARTED, SUCCESS) from Redis / Simulator."""
    try:
        async_res = celery_app.AsyncResult(task_id)
        state = async_res.state
        result = async_res.result if state == 'SUCCESS' else None
    except Exception:
        sim_task = task_store.get_task(task_id)
        if sim_task:
            state = sim_task["state"]
            result = sim_task["result"]
        else:
            state = "NOT_FOUND"
            result = None

    return jsonify({
        "task_id": task_id,
        "state": state,
        "result": result
    }), 200


# =============================================================================
# STEP 6: Interactive Web UI Dashboard Route Handler (render_template)
# =============================================================================
@app.route('/')
def home():
    """Step 6: Renders templates/index.html dashboard."""
    return render_template('index.html')


# =============================================================================
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 21 Background Processing Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("⚙️ Celery Task Dispatcher Active")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
