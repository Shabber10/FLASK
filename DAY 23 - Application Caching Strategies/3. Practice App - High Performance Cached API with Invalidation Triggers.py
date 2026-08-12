"""
===============================================================================
Day 23 Practice Script: High Performance Cached API & Invalidation Pipeline
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Configuring `Flask-Caching` with `SimpleCache` / `RedisCache`.
2. STEP 2: Performance Measurement Middleware injecting `X-Response-Time-MS` headers.
3. STEP 3: Function Memoization (`@cache.memoize()`) for expensive calculations.
4. STEP 4: View Caching (`@cache.cached()`) and explicit Cache Invalidation (`cache.delete()`, `cache.delete_memoized()`).
5. STEP 5: Interactive Web UI Performance Benchmark Dashboard rendering `templates/index.html`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - High Performance Cached API with Invalidation Triggers.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import time
from flask import Flask, jsonify, request, g, render_template
from flask_caching import Cache

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day23-caching-masterclass-secret'

# =============================================================================
# STEP 1: Configure Flask-Caching
# =============================================================================
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
# STEP 2: Performance Measurement Middleware
# =============================================================================
@app.before_request
def start_timer():
    """Step 2a: Captures request start time."""
    g.start_time = time.time()


@app.after_request
def inject_latency_headers(response):
    """Step 2b: Calculates request execution time in milliseconds."""
    if hasattr(g, 'start_time'):
        elapsed_ms = round((time.time() - g.start_time) * 1000, 2)
        response.headers['X-Response-Time-MS'] = f"{elapsed_ms}ms"
    return response


# =============================================================================
# STEP 3: Internal Memoized Computation Helper (@cache.memoize)
# =============================================================================
@cache.memoize(timeout=60)
def calculate_heavy_product_analytics(product_id):
    """Step 3: Simulates an expensive 1.5-second mathematical analytics calculation."""
    time.sleep(1.5)  # Heavy computation delay
    product = products_db.get(product_id, {})
    revenue_projection = product.get('price', 0) * product.get('stock', 0) * 1.25
    return {
        "product_id": product_id,
        "projected_annual_revenue": round(revenue_projection, 2),
        "computed_at_timestamp": time.strftime("%H:%M:%S")
    }


# =============================================================================
# STEP 4: REST API Endpoints (View Caching & Cache Invalidation)
# =============================================================================

# GET /api/v1/products -> View Cached Catalog Response (2-second simulated delay on Cache Miss)
@app.route('/api/v1/products', methods=['GET'])
@cache.cached(timeout=20, key_prefix='all_products_catalog')
def get_products():
    """Step 4a: View Caching endpoint storing complete HTTP response."""
    time.sleep(2.0)  # Simulate slow database query (Cache Miss)
    return jsonify({
        "status": "success",
        "data": list(products_db.values()),
        "fetched_from": "Database (Cache Miss)"
    }), 200


# GET /api/v1/products/<int:id>/analytics -> Memoized Function Endpoint
@app.route('/api/v1/products/<int:product_id>/analytics', methods=['GET'])
def get_analytics(product_id):
    """Step 4b: Function Memoization endpoint."""
    if product_id not in products_db:
        return jsonify({"error": "Product not found"}), 404

    analytics = calculate_heavy_product_analytics(product_id)
    return jsonify({
        "status": "success",
        "data": analytics
    }), 200


# PUT /api/v1/products/<int:id> -> Updates Product & Triggers Cache Invalidation
@app.route('/api/v1/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Step 4c: Updates database and explicitly flushes stale cache keys."""
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
    """Step 4d: Flushes all active application caches."""
    cache.clear()
    return jsonify({"status": "success", "message": "All application caches flushed!"}), 200


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
    print("🚀 Starting Day 23 High Performance Caching Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("🛒 Cached Products Catalog at: http://127.0.0.1:5000/api/v1/products")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
