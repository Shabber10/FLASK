"""
===============================================================================
Day 22 Practice Script: Automated Periodic Task Scheduler & Celery Beat
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Defining background maintenance tasks (session cleanup, analytics, backups).
2. STEP 2: Configuring Celery Beat Periodic Task Schedules (`celery_app.conf.beat_schedule`).
3. STEP 3: Embedded Live Scheduler Thread Simulator executing periodic jobs for interactive testing.
4. STEP 4: REST API endpoints inspecting active schedules, logs, and manual triggers.
5. STEP 5: Interactive Web UI Live Scheduler Monitoring Dashboard rendering `templates/index.html`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Automated Periodic Database Cleanup Scheduler.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import time
import datetime
from threading import Thread
from flask import Flask, jsonify, render_template
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
# STEP 1: Periodic Tasks Definitions
# =============================================================================
@celery_app.task
def purge_expired_sessions_task():
    """Step 1a: Periodic Job 1 - Purges stale session records from DB."""
    add_execution_log("PURGE_SESSIONS", "Purged 14 expired user session tokens from database.")
    return "Purged expired sessions."


@celery_app.task
def aggregate_traffic_analytics_task():
    """Step 1b: Periodic Job 2 - Aggregates website traffic analytics."""
    add_execution_log("ANALYTICS_SYNC", "Aggregated 1,250 page views into analytics summary.")
    return "Analytics aggregated."


@celery_app.task
def nightly_database_backup_task():
    """Step 1c: Periodic Job 3 - Generates database backup archive."""
    add_execution_log("NIGHTLY_BACKUP", "Created PostgreSQL dump archive 'db_backup_20260810.sql.gz'.")
    return "Database backup complete."


# =============================================================================
# STEP 2: Celery Beat Schedule Configuration (`beat_schedule`)
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
# STEP 3: Embedded Live Scheduler Simulator Loop
# =============================================================================
def start_embedded_scheduler():
    """Step 3: Background thread simulating Beat periodic execution for interactive testing."""
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
# STEP 4: REST API Endpoints (Schedules, Logs, Manual Triggers)
# =============================================================================

# GET /api/v1/schedules -> Inspect active Celery Beat schedules
@app.route('/api/v1/schedules', methods=['GET'])
def get_schedules():
    """Step 4a: Inspects active Celery Beat schedule dictionary."""
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
    """Step 4b: Returns live execution logs for UI console monitoring."""
    return jsonify({
        "status": "success",
        "logs": execution_logs
    }), 200


# POST /api/v1/trigger/<job_name> -> Manually trigger a periodic job
@app.route('/api/v1/trigger/<job_name>', methods=['POST'])
def trigger_manual_job(job_name):
    """Step 4c: Manually executes periodic tasks out of schedule."""
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
# STEP 5: Interactive Web UI Dashboard Route Handler (render_template)
# =============================================================================
@app.route('/')
def home():
    """Step 5: Renders templates/index.html dashboard."""
    return render_template('index.html')


# =============================================================================
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 22 Periodic Task Scheduler Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("⏰ Celery Beat Config & Embedded Periodic Engine Active")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
