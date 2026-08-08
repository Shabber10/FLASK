# Day 21 Practice App: Celery Task Integration Setup
from flask import Flask, jsonify, request
from celery import Celery
import time

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task(bind=True)
def long_task(self):
    time.sleep(5)
    return {"status": "Task Complete", "result": 42}

@app.route('/trigger-task', methods=['POST'])
def trigger():
    task = long_task.apply_async()
    return jsonify({"task_id": task.id, "status": "Task Queued"}), 202

if __name__ == '__main__':
    app.run(debug=True)
