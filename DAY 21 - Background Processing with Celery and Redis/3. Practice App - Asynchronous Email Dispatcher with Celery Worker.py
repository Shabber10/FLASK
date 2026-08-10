"""
===============================================================================
Day 21 Practice Script: Asynchronous Background Processing Engine
===============================================================================
This script demonstrates:
1. Configuring Celery with Flask (`celery_init_app()`).
2. Defining background tasks (`@celery_app.task`).
3. Triggering background tasks (`.delay()` and `.apply_async()`).
4. Returning HTTP 202 Accepted status responses.
5. Polling task execution states (`AsyncResult`) from Redis / Fallback Store.
6. Interactive Web UI background job management dashboard.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Asynchronous Email Dispatcher with Celery Worker.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import time
import uuid
from threading import Thread
from flask import Flask, jsonify, request, render_template_string
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
# 1. Official Flask-Celery Application Factory Helper
# =============================================================================
def celery_init_app(app: Flask) -> Celery:
    """Official Flask 2.3+ Celery Integration Factory."""
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
# 2. Fallback In-Memory Task Simulator (Ensures Script Runs Without Redis)
# =============================================================================
class InMemoryTaskStore:
    """Fallback simulator tracking task states if Redis server is offline."""
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
    """Thread simulator executing background work if Redis worker is not running."""
    time.sleep(1)
    task_store.update_task(task_id, "STARTED")
    time.sleep(seconds_delay)
    task_store.update_task(task_id, "SUCCESS", result=return_value)


# =============================================================================
# 3. Background Tasks
# =============================================================================
@celery_app.task(bind=True)
def send_email_task(self, recipient_email, subject_text):
    """Celery background task simulating email dispatch."""
    time.sleep(4)  # Simulate 4-second SMTP network delay
    return f"Email with subject '{subject_text}' successfully delivered to {recipient_email}."


@celery_app.task(bind=True)
def generate_pdf_report_task(self, report_id):
    """Celery background task simulating PDF generation."""
    time.sleep(6)  # Simulate heavy PDF computation
    return f"PDF Report #{report_id} generated and saved to S3 storage."


# =============================================================================
# 4. REST API Endpoints
# =============================================================================

# POST /api/v1/jobs/send-email -> Queue Email Task
@app.route('/api/v1/jobs/send-email', methods=['POST'])
def trigger_email_job():
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
    # Try querying Celery AsyncResult first
    try:
        async_res = celery_app.AsyncResult(task_id)
        state = async_res.state
        result = async_res.result if state == 'SUCCESS' else None
    except Exception:
        # Fallback to local simulator store
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
# 5. Interactive Web UI Job Dashboard
# =============================================================================
@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Day 21 Background Processing</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 40px; color: #333; }
                .card { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
                h2 { color: #2c3e50; margin-top: 0; }
                .badge { background: #d35400; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; }
                .btn { display: inline-block; background: #2980b9; color: white; padding: 10px 18px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-right: 10px; }
                .btn-success { background: #27ae60; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 10px; border-bottom: 1px solid #e9ecef; text-align: left; }
                th { background: #34495e; color: white; }
                code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; color: #c7254e; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>⚙️ Background Task Queue & Celery Engine (Day 21)</h2>
                <p>Task Engine Status: <span class="badge">Celery + Redis / Simulator Ready</span></p>

                <h3>Trigger Background Jobs:</h3>
                <p>
                    <button class="btn" onclick="triggerJob('/api/v1/jobs/send-email')">📧 Queue Asynchronous Email (4s)</button>
                    <button class="btn btn-success" onclick="triggerJob('/api/v1/jobs/generate-report')">📄 Queue PDF Report (6s)</button>
                </p>

                <h3>Live Job Monitoring Console:</h3>
                <div id="output" style="background: #1e1e1e; color: #00ff00; padding: 15px; border-radius: 5px; font-family: monospace; min-height: 120px; overflow-y: auto;">
                    Click a button above to queue a background task...
                </div>

                <script>
                    function triggerJob(url) {
                        const consoleDiv = document.getElementById('output');
                        consoleDiv.innerHTML = "Submitting job request to server...";
                        
                        fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' } })
                        .then(r => r.json())
                        .then(data => {
                            consoleDiv.innerHTML = "HTTP 202 ACCEPTED!<br>Task ID: " + data.task_id + "<br>Engine: " + data.engine + "<br>Polling status...";
                            pollStatus(data.task_id);
                        });
                    }

                    function pollStatus(taskId) {
                        const consoleDiv = document.getElementById('output');
                        const interval = setInterval(() => {
                            fetch('/api/v1/jobs/' + taskId)
                            .then(r => r.json())
                            .then(data => {
                                consoleDiv.innerHTML = "Polling Task ID: " + data.task_id + "<br>State: <strong>" + data.state + "</strong>";
                                if (data.state === 'SUCCESS') {
                                    clearInterval(interval);
                                    consoleDiv.innerHTML += "<br>🎉 Result: " + JSON.stringify(data.result);
                                }
                            });
                        }, 1000);
                    }
                </script>
            </div>
        </body>
        </html>
    """)


# =============================================================================
# 6. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 21 Background Processing Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("⚙️ Celery Task Dispatcher Active")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
