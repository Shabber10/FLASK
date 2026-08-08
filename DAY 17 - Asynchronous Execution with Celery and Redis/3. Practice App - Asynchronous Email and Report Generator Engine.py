"""
Day 17 Practice Application: Asynchronous Job Processing Engine
================================================================
This application demonstrates:
1. Configuring Celery with Flask 3.x using the official application context wrapper.
2. Offloading simulated heavy tasks (PDF Report Generation & Email Sending).
3. Dispatching tasks asynchronously with .delay() and returning UUID task IDs.
4. Polling task status (PENDING, SUCCESS, FAILURE) via AsyncResult.
5. Providing an interactive Web UI with real-time AJAX progress tracking.
"""

import time
import random
from flask import Flask, jsonify, request, render_template_string
from celery import Celery, Task, shared_task
from celery.result import AsyncResult

# ------------------------------------------------------------------------------
# 1. Flask & Celery Factory Setup
# ------------------------------------------------------------------------------
def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


app = Flask(__name__)
app.config['SECRET_KEY'] = 'day17-celery-redis-masterclass-secret'
app.config["CELERY"] = {
    "broker_url": "redis://localhost:6379/0",
    "result_backend": "redis://localhost:6379/0",
    "task_serializer": "json",
    "result_serializer": "json",
    "accept_content": ["json"],
    "result_expires": 3600
}

celery_app = celery_init_app(app)


# ------------------------------------------------------------------------------
# 2. Celery Background Tasks
# ------------------------------------------------------------------------------
@celery_app.task(bind=True)
def generate_monthly_report_task(self, report_name):
    """Simulates a heavy 5-second PDF report compilation task."""
    print(f"[CELERY WORKER] Starting PDF generation for '{report_name}'...")
    
    for i in range(1, 6):
        time.sleep(1) # Simulate heavy computation
        # Update custom task state progress
        self.update_state(state='PROGRESS', meta={'current': i * 20, 'total': 100, 'status': f'Processing step {i}/5'})

    print(f"[CELERY WORKER] PDF '{report_name}' generated successfully!")
    return {
        "status": "COMPLETED",
        "report_name": report_name,
        "download_url": f"/downloads/{report_name.lower().replace(' ', '_')}.pdf",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }


# ------------------------------------------------------------------------------
# 3. HTML Web UI Dashboard
# ------------------------------------------------------------------------------
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 17 Celery & Redis Task Engine</title>
    <style>
        body { font-family: Arial, sans-serif; background: #eef2f5; margin: 30px; }
        .card { max-width: 850px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .btn { background: #27ae60; color: white; border: none; padding: 10px 18px; border-radius: 4px; font-size: 1em; cursor: pointer; }
        .progress-bar { width: 100%; background: #e2e8f0; height: 25px; border-radius: 12px; overflow: hidden; margin-top: 15px; }
        .progress-fill { width: 0%; background: #3182ce; height: 100%; text-align: center; color: white; line-height: 25px; font-size: 0.85em; transition: width 0.3s; }
        .status-box { background: #1a202c; color: #63b3ed; padding: 15px; border-radius: 6px; font-family: monospace; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>⚡ Asynchronous Task Processing Engine (Day 17)</h2>
        <p>Offload heavy tasks to Celery background workers & Redis message brokers without blocking Flask requests.</p>

        <button class="btn" onclick="startReportTask()">Generate Heavy PDF Report (Async Task)</button>

        <div class="progress-bar">
            <div id="progress" class="progress-fill">0%</div>
        </div>

        <div id="status_output" class="status-box">Ready to dispatch tasks. Click button above.</div>
    </div>

    <script>
        let pollTimer = null;

        async function startReportTask() {
            document.getElementById('status_output').innerText = "Dispatching Celery Task...";
            const res = await fetch('/api/reports/generate', { method: 'POST' });
            const data = await res.json();
            
            if (res.ok) {
                document.getElementById('status_output').innerText = "Task Dispatched! Task ID: " + data.task_id;
                pollTaskStatus(data.task_id);
            }
        }

        function pollTaskStatus(taskId) {
            pollTimer = setInterval(async () => {
                const res = await fetch('/api/tasks/' + taskId);
                const data = await res.json();
                
                if (data.state === 'PROGRESS') {
                    const percent = data.meta.current;
                    document.getElementById('progress').style.width = percent + '%';
                    document.getElementById('progress').innerText = percent + '%';
                    document.getElementById('status_output').innerText = "Task Progress: " + data.meta.status;
                } else if (data.state === 'SUCCESS') {
                    clearInterval(pollTimer);
                    document.getElementById('progress').style.width = '100%';
                    document.getElementById('progress').innerText = '100%';
                    document.getElementById('status_output').innerText = "Task Completed! Result:\n" + JSON.stringify(data.result, null, 2);
                } else if (data.state === 'FAILURE') {
                    clearInterval(pollTimer);
                    document.getElementById('status_output').innerText = "Task Failed! Error: " + data.error;
                }
            }, 1000);
        }
    </script>
</body>
</html>
"""


# ------------------------------------------------------------------------------
# 4. Route Handlers
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/reports/generate', methods=['POST'])
def generate_report():
    report_name = f"Financial_Report_Q{random.randint(1, 4)}_{int(time.time())}"
    # Dispatch task asynchronously to Redis/Celery queue
    task = generate_monthly_report_task.delay(report_name)
    return jsonify({
        "status": "Task Queued Successfully",
        "task_id": task.id,
        "report_name": report_name
    }), 202

@app.route('/api/tasks/<task_id>')
def task_status(task_id):
    res = AsyncResult(task_id, app=celery_app)
    
    response_data = {
        "task_id": task_id,
        "state": res.state
    }

    if res.state == 'PROGRESS':
        response_data["meta"] = res.info
    elif res.state == 'SUCCESS':
        response_data["result"] = res.result
    elif res.state == 'FAILURE':
        response_data["error"] = str(res.result)

    return jsonify(response_data)


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 17 Celery Application...")
    print("Dashboard UI at http://127.0.0.1:5000/")
    print("Note: Ensure Redis is running (redis://localhost:6379/0)")
    print("And start Celery Worker: celery -A app.celery_app worker --loglevel=info")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
