"""
===============================================================================
Day 25 Practice Script: High Concurrency Asynchronous Microservice Aggregator
===============================================================================
This script demonstrates:
1. Writing asynchronous coroutine functions using `async def` and `await`.
2. Executing concurrent I/O requests in parallel using `asyncio.gather()`.
3. Comparing Sequential I/O (~5.0s) vs Concurrent Asynchronous I/O (~1.0s).
4. Measuring performance latency headers (`X-Response-Time-MS`).
5. Interactive Web UI Concurrency Benchmark Dashboard.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - High Concurrency Async External API Fetcher.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import time
import asyncio
from flask import Flask, jsonify, g, render_template_string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day25-async-masterclass-secret'

# Simulated External Microservice Endpoints
MICROSERVICES = [
    {"id": 1, "name": "Payment Gateway API", "delay": 1.0},
    {"id": 2, "name": "User Profile Service", "delay": 1.0},
    {"id": 3, "name": "Inventory Stock Service", "delay": 1.0},
    {"id": 4, "name": "Shipping & Logistics API", "delay": 1.0},
    {"id": 5, "name": "Fraud Detection Service", "delay": 1.0}
]


# =============================================================================
# 1. Performance Measurement Middleware
# =============================================================================
@app.before_request
def start_timer():
    g.start_time = time.time()


@app.after_request
def inject_latency_headers(response):
    if hasattr(g, 'start_time'):
        elapsed_ms = round((time.time() - g.start_time) * 1000, 2)
        response.headers['X-Response-Time-MS'] = f"{elapsed_ms}ms"
    return response


# =============================================================================
# 2. Async Coroutine Helpers & Sync Simulators
# =============================================================================
async def fetch_microservice_async(service):
    """Asynchronous non-blocking coroutine simulating external API fetch."""
    await asyncio.sleep(service['delay'])  # Non-blocking async sleep!
    return {
        "service_id": service['id'],
        "name": service['name'],
        "status": "HEALTHY",
        "response_time_sec": service['delay']
    }


def fetch_microservice_sync(service):
    """Synchronous blocking function simulating traditional API fetch."""
    time.sleep(service['delay'])  # Blocking thread sleep!
    return {
        "service_id": service['id'],
        "name": service['name'],
        "status": "HEALTHY",
        "response_time_sec": service['delay']
    }


async def aggregate_all_microservices_async():
    """Concurrently fetches all 5 microservices in parallel using asyncio.gather()."""
    tasks = [fetch_microservice_async(svc) for svc in MICROSERVICES]
    # Runs all 5 tasks concurrently on the event loop!
    results = await asyncio.gather(*tasks)
    return results


# =============================================================================
# 3. REST API Endpoints
# =============================================================================

# GET /api/v1/sync-fetch -> Sequential Execution (5 x 1.0s = ~5.0 seconds!)
@app.route('/api/v1/sync-fetch', methods=['GET'])
def get_sync_fetch():
    results = []
    for svc in MICROSERVICES:
        results.append(fetch_microservice_sync(svc))

    return jsonify({
        "status": "success",
        "execution_mode": "Synchronous Sequential (Blocking)",
        "microservices_count": len(results),
        "data": results
    }), 200


# GET /api/v1/async-fetch -> Concurrent Async Execution (5 x 1.0s = ~1.0 second!)
@app.route('/api/v1/async-fetch', methods=['GET'])
def get_async_fetch():
    # Execute async event loop gather
    results = asyncio.run(aggregate_all_microservices_async())

    return jsonify({
        "status": "success",
        "execution_mode": "Asynchronous Concurrent (asyncio.gather)",
        "microservices_count": len(results),
        "data": results
    }), 200


# =============================================================================
# 4. Interactive Web UI Concurrency Benchmark Dashboard
# =============================================================================
@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Day 25 Async Concurrency Masterclass</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 40px; color: #333; }
                .card { max-width: 850px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
                h2 { color: #2c3e50; margin-top: 0; }
                .badge { background: #8e44ad; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; }
                .btn { display: inline-block; background: #27ae60; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-right: 10px; border: none; cursor: pointer; }
                .btn-danger { background: #c0392b; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 10px; border-bottom: 1px solid #e9ecef; text-align: left; }
                th { background: #34495e; color: white; }
                code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; color: #c7254e; font-weight: bold; }
                .metric { font-size: 26px; font-weight: bold; color: #e74c3c; margin-top: 10px; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>⚡ Async Flask & Concurrency Aggregator (Day 25)</h2>
                <p>Execution Engine: <span class="badge">Python asyncio.gather()</span></p>

                <p>This demo fetches data from 5 external microservices (each having 1.0s latency):</p>

                <p>
                    <button class="btn btn-danger" onclick="testBenchmark('/api/v1/sync-fetch')">🔴 Run Synchronous Sequential (~5.0s)</button>
                    <button class="btn" onclick="testBenchmark('/api/v1/async-fetch')">🟢 Run Asynchronous Parallel (~1.0s)</button>
                </p>

                <h3>Live Latency Benchmark Console:</h3>
                <div id="output" style="background: #1e1e1e; color: #00ff00; padding: 15px; border-radius: 5px; font-family: monospace; min-height: 120px;">
                    Click a benchmark button above to test concurrency execution...
                </div>

                <script>
                    function testBenchmark(url) {
                        const out = document.getElementById('output');
                        out.innerHTML = "Executing request to '" + url + "'... Please wait...";
                        const startTime = performance.now();

                        fetch(url)
                        .then(res => {
                            const latencyHeader = res.headers.get('X-Response-Time-MS');
                            return res.json().then(data => ({ data, latencyHeader }));
                        })
                        .then(item => {
                            const clientMs = Math.round(performance.now() - startTime);
                            out.innerHTML = "STATUS 200 OK!<br>" +
                                "Execution Mode: <strong>" + item.data.execution_mode + "</strong><br>" +
                                "Server Latency Header: <span class='metric'>" + item.latencyHeader + "</span><br>" +
                                "Client Roundtrip Time: " + clientMs + "ms<br><br>" +
                                "Aggregated Data: " + JSON.stringify(item.data.data, null, 2);
                        });
                    }
                </script>
            </div>
        </body>
        </html>
    """)


# =============================================================================
# 5. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 25 Async Concurrency Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("🔴 Sync Fetch at: http://127.0.0.1:5000/api/v1/sync-fetch")
    print("🟢 Async Fetch at: http://127.0.0.1:5000/api/v1/async-fetch")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
