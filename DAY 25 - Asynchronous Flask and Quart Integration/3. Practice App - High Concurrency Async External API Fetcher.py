"""
===============================================================================
Day 25 Practice Script: High Concurrency Asynchronous Microservice Aggregator
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Authoring performance measurement middleware (`X-Response-Time-MS`).
2. STEP 2: Writing asynchronous coroutine functions using `async def` and `await`.
3. STEP 3: Executing concurrent I/O requests in parallel using `asyncio.gather()`.
4. STEP 4: REST API Endpoints comparing Sequential I/O (~5.0s) vs Concurrent Asynchronous I/O (~1.0s).
5. STEP 5: Interactive Web UI Concurrency Benchmark Dashboard rendering `templates/index.html`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - High Concurrency Async External API Fetcher.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import time
import asyncio
from flask import Flask, jsonify, g, render_template

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
# STEP 1: Performance Measurement Middleware
# =============================================================================
@app.before_request
def start_timer():
    """Step 1a: Captures request start time."""
    g.start_time = time.time()


@app.after_request
def inject_latency_headers(response):
    """Step 1b: Calculates request execution latency in milliseconds."""
    if hasattr(g, 'start_time'):
        elapsed_ms = round((time.time() - g.start_time) * 1000, 2)
        response.headers['X-Response-Time-MS'] = f"{elapsed_ms}ms"
    return response


# =============================================================================
# STEP 2: Async Coroutine Helpers & Sync Simulators
# =============================================================================
async def fetch_microservice_async(service):
    """Step 2a: Asynchronous non-blocking coroutine simulating external API fetch."""
    await asyncio.sleep(service['delay'])  # Non-blocking async sleep!
    return {
        "service_id": service['id'],
        "name": service['name'],
        "status": "HEALTHY",
        "response_time_sec": service['delay']
    }


def fetch_microservice_sync(service):
    """Step 2b: Synchronous blocking function simulating traditional API fetch."""
    time.sleep(service['delay'])  # Blocking thread sleep!
    return {
        "service_id": service['id'],
        "name": service['name'],
        "status": "HEALTHY",
        "response_time_sec": service['delay']
    }


# =============================================================================
# STEP 3: High-Concurrency Parallel Aggregation (asyncio.gather)
# =============================================================================
async def aggregate_all_microservices_async():
    """Step 3: Concurrently fetches all 5 microservices in parallel using asyncio.gather()."""
    tasks = [fetch_microservice_async(svc) for svc in MICROSERVICES]
    # Runs all 5 tasks concurrently on the event loop!
    results = await asyncio.gather(*tasks)
    return results


# =============================================================================
# STEP 4: REST API Endpoints (Sync vs Async Benchmarks)
# =============================================================================

# GET /api/v1/sync-fetch -> Sequential Execution (5 x 1.0s = ~5.0 seconds!)
@app.route('/api/v1/sync-fetch', methods=['GET'])
def get_sync_fetch():
    """Step 4a: Sequential blocking execution taking ~5.0 seconds total."""
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
    """Step 4b: Concurrent parallel execution taking ~1.0 second total."""
    results = asyncio.run(aggregate_all_microservices_async())

    return jsonify({
        "status": "success",
        "execution_mode": "Asynchronous Concurrent (asyncio.gather)",
        "microservices_count": len(results),
        "data": results
    }), 200


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
    print("🚀 Starting Day 25 Async Concurrency Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("🔴 Sync Fetch at: http://127.0.0.1:5000/api/v1/sync-fetch")
    print("🟢 Async Fetch at: http://127.0.0.1:5000/api/v1/async-fetch")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
