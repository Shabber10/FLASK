"""
===============================================================================
Day 23 Practice Script: High Performance Cached API & Invalidation Pipeline
===============================================================================
This script demonstrates:
1. Configuring `Flask-Caching` with `SimpleCache` / `RedisCache`.
2. View Caching (`@cache.cached()`) for full HTTP API response payloads.
3. Function Memoization (`@cache.memoize()`) for expensive calculations.
4. Cache Invalidation (`cache.delete()`, `cache.delete_memoized()`).
5. Measuring performance latency headers (`X-Response-Time-MS`, `X-Cache-Status`).
6. Interactive Web UI Performance Benchmark Dashboard.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - High Performance Cached API with Invalidation Triggers.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import time
from flask import Flask, jsonify, request, g, render_template_string
from flask_caching import Cache

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day23-caching-masterclass-secret'

# Configure Flask-Caching (Uses SimpleCache; easily switched to RedisCache)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 60

cache = Cache(app)

# In-Memory Products Database
products_db = {
    1: {"id": 1, "name": "4K Ultra HD Monitor", "price": 499.99, "stock": 45},
    2: {"id": 2, "name": "Ergonomic Mechanical Keyboard", "price": 129.50, "stock": 120},
    3: {"id": 3, "name": "Wireless Noise-Cancelling Headphones", "price": 249.99, "stock": 80}
}


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
# 2. Internal Memoized Computation Helper
# =============================================================================
@cache.memoize(timeout=60)
def calculate_heavy_product_analytics(product_id):
    """Simulates an expensive 1.5-second mathematical analytics calculation."""
    time.sleep(1.5)  # Heavy computation delay
    product = products_db.get(product_id, {})
    revenue_projection = product.get('price', 0) * product.get('stock', 0) * 1.25
    return {
        "product_id": product_id,
        "projected_annual_revenue": round(revenue_projection, 2),
        "computed_at_timestamp": time.strftime("%H:%M:%S")
    }


# =============================================================================
# 3. REST API Endpoints
# =============================================================================

# GET /api/v1/products -> View Cached Catalog Response (2-second simulated delay on Cache Miss)
@app.route('/api/v1/products', methods=['GET'])
@cache.cached(timeout=20, key_prefix='all_products_catalog')
def get_products():
    time.sleep(2.0)  # Simulate slow database query (Cache Miss)
    return jsonify({
        "status": "success",
        "data": list(products_db.values()),
        "fetched_from": "Database (Cache Miss)"
    }), 200


# GET /api/v1/products/<int:id>/analytics -> Memoized Function Endpoint
@app.route('/api/v1/products/<int:product_id>/analytics', methods=['GET'])
def get_analytics(product_id):
    if product_id not in products_db:
        return jsonify({"error": "Product not found"}), 404

    # Call Memoized Function
    analytics = calculate_heavy_product_analytics(product_id)
    return jsonify({
        "status": "success",
        "data": analytics
    }), 200


# PUT /api/v1/products/<int:id> -> Updates Product & Triggers Cache Invalidation
@app.route('/api/v1/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    if product_id not in products_db:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json() or {}
    if 'price' in data:
        products_db[product_id]['price'] = float(data['price'])
    if 'name' in data:
        products_db[product_id]['name'] = data['name']

    # 1. Invalidate View Cache for catalog
    cache.delete('all_products_catalog')
    
    # 2. Invalidate Memoized Function Cache for this specific product
    cache.delete_memoized(calculate_heavy_product_analytics, product_id)

    return jsonify({
        "status": "success",
        "message": f"Product #{product_id} updated successfully. Cache invalidated!",
        "updated_product": products_db[product_id]
    }), 200


# POST /api/v1/cache/clear -> Flushes Cache Completely
@app.route('/api/v1/cache/clear', methods=['POST'])
def clear_cache():
    cache.clear()
    return jsonify({"status": "success", "message": "All application caches flushed!"}), 200


# =============================================================================
# 4. Interactive Web UI Performance Benchmark Dashboard
# =============================================================================
@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Day 23 Caching Masterclass</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 40px; color: #333; }
                .card { max-width: 850px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
                h2 { color: #2c3e50; margin-top: 0; }
                .badge { background: #27ae60; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; }
                .btn { display: inline-block; background: #2980b9; color: white; padding: 10px 16px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-right: 8px; border: none; cursor: pointer; }
                .btn-danger { background: #c0392b; }
                .btn-warning { background: #d35400; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 10px; border-bottom: 1px solid #e9ecef; text-align: left; }
                th { background: #34495e; color: white; }
                code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; color: #c7254e; font-weight: bold; }
                .metric { font-size: 24px; font-weight: bold; color: #e74c3c; margin-top: 10px; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>⚡ High Performance Application Caching Engine (Day 23)</h2>
                <p>Caching Extension: <span class="badge">Flask-Caching (SimpleCache Active)</span></p>

                <h3>Test Benchmark Controls:</h3>
                <p>
                    <button class="btn" onclick="testEndpoint('/api/v1/products')">🛒 Fetch Catalog (View Cache 2s vs 0.5ms)</button>
                    <button class="btn btn-warning" onclick="testEndpoint('/api/v1/products/1/analytics')">📊 Fetch Product #1 Analytics (Memoized 1.5s)</button>
                    <button class="btn btn-danger" onclick="invalidateCache()">🔄 Invalidate Product #1 Cache</button>
                </p>

                <h3>Live Response Benchmark Results:</h3>
                <div id="output" style="background: #1e1e1e; color: #00ff00; padding: 15px; border-radius: 5px; font-family: monospace; min-height: 120px;">
                    Click a benchmark button above to test caching latency...
                </div>

                <script>
                    function testEndpoint(url) {
                        const out = document.getElementById('output');
                        out.innerHTML = "Fetching endpoint '" + url + "'...";
                        const startTime = performance.now();

                        fetch(url)
                        .then(res => {
                            const latencyHeader = res.headers.get('X-Response-Time-MS');
                            return res.json().then(data => ({ data, latencyHeader }));
                        })
                        .then(item => {
                            const clientMs = Math.round(performance.now() - startTime);
                            out.innerHTML = "STATUS 200 OK!<br>" +
                                "Server Latency Header: <span class='metric'>" + item.latencyHeader + "</span><br>" +
                                "Total Roundtrip Time: " + clientMs + "ms<br><br>" +
                                "Response Data: " + JSON.stringify(item.data, null, 2);
                        });
                    }

                    function invalidateCache() {
                        const out = document.getElementById('output');
                        fetch('/api/v1/products/1', {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ price: (Math.random() * 500 + 100).toFixed(2) })
                        })
                        .then(r => r.json())
                        .then(data => {
                            out.innerHTML = "<strong>CACHE INVALIDATED!</strong><br>" + JSON.stringify(data, null, 2);
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
    print("🚀 Starting Day 23 High Performance Caching Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("🛒 Cached Products Catalog at: http://127.0.0.1:5000/api/v1/products")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
