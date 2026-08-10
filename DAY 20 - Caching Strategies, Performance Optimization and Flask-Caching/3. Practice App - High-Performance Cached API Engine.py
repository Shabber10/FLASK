"""
Day 20 Practice Application: High-Performance Caching & Analytics Engine
========================================================================
This application demonstrates:
1. Initializing Flask-Caching extension (SimpleCache / RedisCache).
2. Caching HTTP view responses with @cache.cached(timeout=60, query_string=True).
3. Memoizing expensive functions with @cache.memoize(timeout=300).
4. Explicit cache invalidation using cache.delete_memoized().
5. Interactive Web Dashboard benchmarking Cache Hits vs Cache Misses and timing.
"""

import time
from flask import Flask, jsonify, request, render_template_string
from flask_caching import Cache

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day20-caching-masterclass-secret'
app.config['CACHE_TYPE'] = 'SimpleCache'  # Uses In-Memory Cache
app.config['CACHE_DEFAULT_TIMEOUT'] = 60

cache = Cache(app)

# Simulated Database of User Analytics
ANALYTICS_DB = {
    101: {"user": "Alice", "transactions_count": 1420, "total_spent": 18500.50},
    102: {"user": "Bob", "transactions_count": 890, "total_spent": 9400.00}
}


# ------------------------------------------------------------------------------
# 1. Memoized Heavy Calculation Function
# ------------------------------------------------------------------------------
@cache.memoize(timeout=120)
def calculate_heavy_user_metrics(user_id):
    """Simulates a heavy 2-second DB aggregation calculation."""
    print(f"[CACHE MISS] Executing heavy DB query for User ID {user_id}...")
    time.sleep(2) # Heavy query computation
    
    data = ANALYTICS_DB.get(user_id, {"user": "Unknown", "transactions_count": 0, "total_spent": 0.0})
    return {
        "user_id": user_id,
        "metrics": data,
        "computed_at": time.strftime("%H:%M:%S")
    }


# ------------------------------------------------------------------------------
# 2. HTML Diagnostic Dashboard Template
# ------------------------------------------------------------------------------
BENCHMARK_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 20 Flask-Caching Masterclass</title>
    <style>
        body { font-family: Arial, sans-serif; background: #eef2f5; margin: 30px; }
        .card { max-width: 850px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .btn { background: #2b6cb0; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; margin-right: 5px; }
        .btn-danger { background: #c53030; }
        .output-box { background: #1a202c; color: #48bb78; padding: 15px; border-radius: 6px; font-family: monospace; font-size: 0.9em; margin-top: 15px; }
        .latency { color: #f6ad55; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🚀 High-Performance Caching Engine (Day 20)</h2>
        <p>Demonstrating Route Caching (<code>@cache.cached</code>), Function Memoization (<code>@cache.memoize</code>), and Cache Invalidation.</p>

        <div>
            <button class="btn" onclick="fetchMetrics(101)">Fetch User 101 Metrics (@cache.memoize)</button>
            <button class="btn" onclick="fetchCatalog()">Fetch Public Catalog (@cache.cached)</button>
            <button class="btn btn-danger" onclick="invalidateUser(101)">Invalidate Cache for User 101</button>
            <button class="btn btn-danger" onclick="clearAllCache()">Clear Entire Cache</button>
        </div>

        <div id="output" class="output-box">Click a button above to test execution speed...</div>
    </div>

    <script>
        async function fetchMetrics(id) {
            const start = performance.now();
            const res = await fetch('/api/analytics/users/' + id);
            const data = await res.json();
            const duration = (performance.now() - start).toFixed(2);
            
            document.getElementById('output').innerHTML = 
                `<span class="latency">Response Time: ${duration}ms</span>\n` + JSON.stringify(data, null, 2);
        }

        async function fetchCatalog() {
            const start = performance.now();
            const res = await fetch('/api/catalog?category=electronics');
            const data = await res.json();
            const duration = (performance.now() - start).toFixed(2);
            
            document.getElementById('output').innerHTML = 
                `<span class="latency">Response Time: ${duration}ms</span>\n` + JSON.stringify(data, null, 2);
        }

        async function invalidateUser(id) {
            const res = await fetch('/api/analytics/users/' + id + '/invalidate', { method: 'POST' });
            const data = await res.json();
            document.getElementById('output').innerText = JSON.stringify(data, null, 2);
        }

        async function clearAllCache() {
            const res = await fetch('/api/cache/clear', { method: 'POST' });
            const data = await res.json();
            document.getElementById('output').innerText = JSON.stringify(data, null, 2);
        }
    </script>
</body>
</html>
"""


# ------------------------------------------------------------------------------
# 3. Route Handlers
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template_string(BENCHMARK_HTML)

# Full View Caching with Query String Support
@app.route('/api/catalog')
@cache.cached(timeout=60, query_string=True)
def get_catalog_api():
    print("[CACHE MISS] Executing heavy catalog DB query...")
    time.sleep(1.5) # Simulate 1.5s DB query
    return jsonify({
        "status": "Success",
        "category": request.args.get('category', 'all'),
        "cached_at": time.strftime("%H:%M:%S"),
        "products": [
            {"id": 1, "name": "Ultra-Fast NVMe SSD", "price": 129.99},
            {"id": 2, "name": "RGB Mechanical Keyboard", "price": 89.99}
        ]
    })

# Memoized User Metrics API
@app.route('/api/analytics/users/<int:user_id>')
def get_user_analytics(user_id):
    result = calculate_heavy_user_metrics(user_id)
    return jsonify(result)

# Invalidate Specific Memoized User Cache Key
@app.route('/api/analytics/users/<int:user_id>/invalidate', methods=['POST'])
def invalidate_user_cache(user_id):
    cache.delete_memoized(calculate_heavy_user_metrics, user_id)
    return jsonify({"status": "Success", "message": f"Cache for user {user_id} invalidated successfully."})

# Clear Entire Cache
@app.route('/api/cache/clear', methods=['POST'])
def clear_all_cache():
    cache.clear()
    return jsonify({"status": "Success", "message": "Entire cache storage flushed."})


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 20 High-Performance Caching Application...")
    print("Dashboard UI at http://127.0.0.1:5000/")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
