"""
===============================================================================
Day 22 Practice Script: Automated Periodic Task Scheduler & Celery Beat
===============================================================================
This script demonstrates:
1. Configuring Celery Beat Periodic Task Schedules (`celery_app.conf.beat_schedule`).
2. Interval schedules (`schedule=10.0`) and Crontab schedules (`crontab(hour=0, minute=0)`).
3. Defining background maintenance tasks (session cleanup, analytics, backups).
4. Live embedded scheduler thread simulator displaying real-time execution logs.
5. Interactive Web UI Live Scheduler Monitoring Dashboard.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Automated Periodic Database Cleanup Scheduler.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import time
import datetime
from threading import Thread
from flask import Flask, jsonify, render_template_string
from celery import Celery
from celery.schedules import crontab

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day22-scheduler-masterclass-secret'

# Configure Celery Broker and Result Backend
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery_app = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery_app.conf.update(app.config)

# Global execution logs list for dashboard UI monitoring
execution_logs = []


def add_execution_log(job_name, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{job_name}] {message}"
    execution_logs.append(log_entry)
    if len(execution_logs) > 30:
        execution_logs.pop(0)
    print(f"⏰ {log_entry}")


# =============================================================================
# 1. Periodic Tasks Definitions
# =============================================================================
@celery_app.task
def purge_expired_sessions_task():
    """Periodic Job 1: Purges stale session records from DB."""
    add_execution_log("PURGE_SESSIONS", "Purged 14 expired user session tokens from database.")
    return "Purged expired sessions."


@celery_app.task
def aggregate_traffic_analytics_task():
    """Periodic Job 2: Aggregates website traffic analytics."""
    add_execution_log("ANALYTICS_SYNC", "Aggregated 1,250 page views into analytics summary.")
    return "Analytics aggregated."


@celery_app.task
def nightly_database_backup_task():
    """Periodic Job 3: Generates database backup archive."""
    add_execution_log("NIGHTLY_BACKUP", "Created PostgreSQL dump archive 'db_backup_20260810.sql.gz'.")
    return "Database backup complete."


# =============================================================================
# 2. Celery Beat Schedule Configuration (`beat_schedule`)
# =============================================================================
celery_app.conf.beat_schedule = {
    # Schedule 1: Run session cleanup every 10 seconds
    'session-cleanup-10s': {
        'task': f'{__name__}.purge_expired_sessions_task',
        'schedule': 10.0,
    },
    # Schedule 2: Run analytics aggregation every 30 seconds
    'analytics-aggregation-30s': {
        'task': f'{__name__}.aggregate_traffic_analytics_task',
        'schedule': 30.0,
    },
    # Schedule 3: Run database backup every night at Midnight (00:00)
    'nightly-database-backup-midnight': {
        'task': f'{__name__}.nightly_database_backup_task',
        'schedule': crontab(hour=0, minute=0),
    },
}


# =============================================================================
# 3. Embedded Live Scheduler Simulator Loop (Runs without needing Celery Beat daemon)
# =============================================================================
def start_embedded_scheduler():
    """Background thread simulating Beat periodic execution for interactive testing."""
    time.sleep(2)
    add_execution_log("SYSTEM", "Embedded Periodic Scheduler Engine initialized!")
    step = 0
    while True:
        time.sleep(5)
        step += 5
        if step % 10 == 0:
            purge_expired_sessions_task()
        if step % 30 == 0:
            aggregate_traffic_analytics_task()


Thread(target=start_embedded_scheduler, daemon=True).start()


# =============================================================================
# 4. REST API Endpoints
# =============================================================================

# GET /api/v1/schedules -> Inspect active Celery Beat schedules
@app.route('/api/v1/schedules', methods=['GET'])
def get_schedules():
    schedules_info = []
    for name, config in celery_app.conf.beat_schedule.items():
        schedules_info.append({
            "schedule_name": name,
            "task": config['task'],
            "schedule_rule": str(config['schedule'])
        })
    return jsonify({
        "status": "success",
        "beat_schedules": schedules_info
    }), 200


# GET /api/v1/logs -> Live execution logs
@app.route('/api/v1/logs', methods=['GET'])
def get_logs():
    return jsonify({
        "status": "success",
        "logs": execution_logs
    }), 200


# POST /api/v1/trigger/<job_name> -> Manually trigger a periodic job
@app.route('/api/v1/trigger/<job_name>', methods=['POST'])
def trigger_manual_job(job_name):
    if job_name == 'purge-sessions':
        purge_expired_sessions_task()
    elif job_name == 'analytics':
        aggregate_traffic_analytics_task()
    elif job_name == 'backup':
        nightly_database_backup_task()
    else:
        return jsonify({"error": f"Unknown job name '{job_name}'"}), 404

    return jsonify({"status": "success", "message": f"Job '{job_name}' executed manually."}), 200


# =============================================================================
# 5. Interactive Web UI Live Scheduler Dashboard
# =============================================================================
@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Day 22 Periodic Task Scheduler</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 40px; color: #333; }
                .card { max-width: 850px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
                h2 { color: #2c3e50; margin-top: 0; }
                .badge { background: #8e44ad; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; }
                .btn { display: inline-block; background: #2980b9; color: white; padding: 8px 14px; text-decoration: none; border-radius: 4px; font-weight: bold; margin-right: 8px; border: none; cursor: pointer; }
                table { width: 100%; border-collapse: collapse; margin-top: 15px; }
                th, td { padding: 10px; border-bottom: 1px solid #e9ecef; text-align: left; }
                th { background: #34495e; color: white; }
                code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; color: #c7254e; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>⏰ Automated Periodic Task Scheduler & Celery Beat (Day 22)</h2>
                <p>Scheduler Status: <span class="badge">Celery Beat Configured + Live Thread Engine Active</span></p>

                <h3>Configured Celery Beat Schedules:</h3>
                <table>
                    <thead><tr><th>Schedule Name</th><th>Task Function</th><th>Interval / Cron Rule</th><th>Action</th></tr></thead>
                    <tbody>
                        <tr><td><code>session-cleanup-10s</code></td><td><code>purge_expired_sessions_task</code></td><td>Every 10 seconds</td><td><button class="btn" onclick="triggerJob('purge-sessions')">Run Now</button></td></tr>
                        <tr><td><code>analytics-aggregation-30s</code></td><td><code>aggregate_traffic_analytics_task</code></td><td>Every 30 seconds</td><td><button class="btn" onclick="triggerJob('analytics')">Run Now</button></td></tr>
                        <tr><td><code>nightly-backup-midnight</code></td><td><code>nightly_database_backup_task</code></td><td><code>crontab(0, 0)</code> (Midnight)</td><td><button class="btn" onclick="triggerJob('backup')">Run Now</button></td></tr>
                    </tbody>
                </table>

                <h3 style="margin-top: 25px;">Live Execution Logs (Auto-Refreshing):</h3>
                <div id="logs" style="background: #1e1e1e; color: #00ff00; padding: 15px; border-radius: 5px; font-family: monospace; height: 180px; overflow-y: auto;">
                    Loading live execution logs...
                </div>

                <script>
                    function triggerJob(jobName) {
                        fetch('/api/v1/trigger/' + jobName, { method: 'POST' })
                        .then(r => r.json())
                        .then(d => refreshLogs());
                    }

                    function refreshLogs() {
                        fetch('/api/v1/logs')
                        .then(r => r.json())
                        .then(data => {
                            const logsDiv = document.getElementById('logs');
                            logsDiv.innerHTML = data.logs.join('<br>') || 'Waiting for scheduled executions...';
                            logsDiv.scrollTop = logsDiv.scrollHeight;
                        });
                    }

                    setInterval(refreshLogs, 2000);
                    refreshLogs();
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
    print("🚀 Starting Day 22 Periodic Task Scheduler Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("⏰ Celery Beat Config & Embedded Periodic Engine Active")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
