"""
Day 29 Practice Application: High-Throughput Ingestion & Batch Engine
======================================================================
This application demonstrates:
1. Building a high-throughput API Ingestion Gateway returning HTTP 202 Accepted.
2. Buffering events in memory / queues to manage backpressure bursts.
3. Spawning a background batch flusher executing bulk SQLAlchemy insertions.
4. Computing real-time time-window analytics aggregations.
5. Interactive Web Dashboard with stress-test payload simulation & throughput monitoring.
"""

import time
import random
import threading
from flask import Flask, jsonify, request, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day29-highthroughput-masterclass-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# In-Memory Queue Buffer for Events
EVENT_BUFFER = []
BUFFER_LOCK = threading.Lock()
TOTAL_INGESTED_COUNT = 0


# ------------------------------------------------------------------------------
# 1. Database Model
# ------------------------------------------------------------------------------
class TelemetryEvent(db.Model):
    __tablename__ = 'telemetry_events'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    latency_ms = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()


# ------------------------------------------------------------------------------
# 2. Background Batch Processing Flusher Thread
# ------------------------------------------------------------------------------
def batch_flush_worker():
    """Background thread that flushes queued events to database in bulk batches of 50."""
    print("[BATCH WORKER] Background flusher thread active...")
    while True:
        time.sleep(1.0) # Flush every 1 second
        batch_to_insert = []
        
        with BUFFER_LOCK:
            if EVENT_BUFFER:
                batch_to_insert = EVENT_BUFFER[:50]
                del EVENT_BUFFER[:50]

        if batch_to_insert:
            start_time = time.time()
            with app.app_context():
                # Perform bulk mapping insertion
                db.session.bulk_insert_mappings(TelemetryEvent, batch_to_insert)
                db.session.commit()
            duration = round((time.time() - start_time) * 1000, 2)
            print(f"[BATCH WORKER] Bulk inserted {len(batch_to_insert)} events in {duration}ms!")

# Start Flusher Thread
flusher_thread = threading.Thread(target=batch_flush_worker, daemon=True)
flusher_thread.start()


# ------------------------------------------------------------------------------
# 3. Interactive Ingestion Dashboard UI
# ------------------------------------------------------------------------------
INGESTION_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 29 High-Throughput Ingestion Masterclass</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; margin: 30px; }
        .card { max-width: 900px; margin: auto; background: #1e293b; padding: 25px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 20px; }
        .stat-card { background: #334155; padding: 15px; border-radius: 6px; text-align: center; }
        .stat-val { font-size: 1.8em; font-weight: bold; color: #38bdf8; font-family: monospace; }
        .btn { background: #3b82f6; color: white; border: none; padding: 10px 18px; border-radius: 4px; cursor: pointer; margin-right: 10px; }
        .btn-success { background: #10b981; }
        .log-box { background: #020617; color: #4ade80; padding: 15px; border-radius: 6px; font-family: monospace; font-size: 0.85em; margin-top: 20px; height: 180px; overflow-y: scroll; }
    </style>
</head>
<body>
    <div class="card">
        <h2>⚡ High-Throughput Event Ingestion Engine (Day 29)</h2>
        <p>Demonstrating Asynchronous Buffer Queueing, HTTP 202 Accepted, and Bulk SQL Batch Inserts.</p>

        <div>
            <button class="btn" onclick="sendSingleEvent()">Ingest Single Event</button>
            <button class="btn btn-success" onclick="simulateBurstTraffic(100)">Simulate Burst Traffic (100 Events)</button>
            <button class="btn" onclick="fetchMetrics()">Refresh Analytics Metrics</button>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div>Queue Buffer Size</div>
                <div id="buffer_count" class="stat-val">0</div>
            </div>
            <div class="stat-card">
                <div>Total Ingested (RPS)</div>
                <div id="total_count" class="stat-val">0</div>
            </div>
            <div class="stat-card">
                <div>DB Total Saved</div>
                <div id="db_count" class="stat-val">0</div>
            </div>
        </div>

        <div id="output" class="log-box">Click a button to ingest events...</div>
    </div>

    <script>
        async function sendSingleEvent() {
            const res = await fetch('/api/v1/telemetry', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({user_id: 101, event_type: 'click', latency_ms: 12.4})
            });
            const data = await res.json();
            document.getElementById('output').innerText = JSON.stringify(data, null, 2);
            fetchMetrics();
        }

        async function simulateBurstTraffic(count) {
            document.getElementById('output').innerText = `Simulating burst stream of ${count} incoming requests...`;
            for (let i = 0; i < count; i++) {
                fetch('/api/v1/telemetry', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({user_id: Math.floor(Math.random()*500)+1, event_type: 'page_view', latency_ms: Math.random()*50})
                });
            }
            setTimeout(fetchMetrics, 500);
        }

        async function fetchMetrics() {
            const res = await fetch('/api/v1/analytics/metrics');
            const data = await res.json();
            document.getElementById('buffer_count').innerText = data.buffer_queue_length;
            document.getElementById('total_count').innerText = data.total_received;
            document.getElementById('db_count').innerText = data.db_records_saved;
        }

        setInterval(fetchMetrics, 1000);
    </script>
</body>
</html>
"""


# ------------------------------------------------------------------------------
# 4. Route Handlers
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template_string(INGESTION_HTML)

# High-Speed Ingestion Endpoint (Returns 202 Accepted Instantly!)
@app.route('/api/v1/telemetry', methods=['POST'])
def ingest_telemetry_event():
    global TOTAL_INGESTED_COUNT
    payload = request.get_json(silent=True) or {}
    
    event_item = {
        "user_id": payload.get('user_id', 1),
        "event_type": payload.get('event_type', 'click'),
        "latency_ms": float(payload.get('latency_ms', 10.0)),
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    with BUFFER_LOCK:
        EVENT_BUFFER.append(event_item)
        TOTAL_INGESTED_COUNT += 1

    # Return 202 Accepted immediately without waiting for DB write!
    return jsonify({
        "status": "Accepted",
        "message": "Event queued in ingestion buffer."
    }), 202

@app.route('/api/v1/analytics/metrics')
def get_analytics_metrics():
    db_count = db.session.query(TelemetryEvent).count()
    return jsonify({
        "status": "Success",
        "buffer_queue_length": len(EVENT_BUFFER),
        "total_received": TOTAL_INGESTED_COUNT,
        "db_records_saved": db_count
    }), 200


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 29 High-Throughput Event Ingestion Engine...")
    print("Ingestion Dashboard UI at http://127.0.0.1:5000/")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
