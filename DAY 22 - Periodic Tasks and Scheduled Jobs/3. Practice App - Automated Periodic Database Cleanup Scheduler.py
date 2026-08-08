# Day 22 Practice App: Periodic Task Schedule Configuration
from flask import Flask
from celery import Celery
from celery.schedules import crontab

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

@celery.task
def scheduled_report():
    print("[CELERY BEAT] Generating hourly analytics report...")

celery.conf.beat_schedule = {
    'hourly-analytics': {
        'task': f'{__name__}.scheduled_report',
        'schedule': 3600.0, # Every hour
    }
}

if __name__ == '__main__':
    app.run(debug=True)
