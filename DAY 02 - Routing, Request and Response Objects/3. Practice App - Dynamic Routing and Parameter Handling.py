"""
===============================================================================
Day 02 Practice Script: Dynamic Routing, Converters & Request Handling
===============================================================================
This script demonstrates:
1. Registering custom regex URL path converters on `app.url_map`.
2. Handling multiple HTTP methods (GET, POST).
3. Extracting URL query parameters (`request.args`), form data, and JSON payloads.
4. Setting custom response headers and secure cookies using `make_response()`.
5. Aborting requests with `abort()` and performing dynamic redirects with `url_for()`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Dynamic Routing and Parameter Handling.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from flask import Flask, request, jsonify, make_response, redirect, url_for, abort
from werkzeug.routing import BaseConverter

# =============================================================================
# 1. Custom Regex URL Converter Definition
# =============================================================================
class RegexConverter(BaseConverter):
    """
    Custom URL Converter that accepts regular expression patterns inside route rules.
    Example: @app.route('/product/<regex(r"PRD-\\d{4}"):sku>')
    """
    def __init__(self, url_map, *items):
        super().__init__(url_map)
        self.regex = items[0]


# =============================================================================
# 2. Flask Application Initialization & Setup
# =============================================================================
app = Flask(__name__)

# Register custom regex converter on Flask's url_map converters dictionary
app.url_map.converters['regex'] = RegexConverter

# Simulated In-Memory Product Database
catalog = {
    "PRD-1001": {"name": "Mechanical Keyboard", "price": 89.99, "category": "peripherals"},
    "PRD-1002": {"name": "Gaming Mouse", "price": 49.99, "category": "peripherals"},
    "PRD-2001": {"name": "Ultra-Wide Monitor", "price": 499.99, "category": "displays"}
}


# =============================================================================
# 3. Route Handlers (View Functions)
# =============================================================================

@app.route('/')
def index():
    """
    Route 1: Index Page ('/')
    Generates dynamic HTML links using url_for().
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Day 02: Routing & Parameters</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f8f9fa; color: #333; }}
            .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }}
            a {{ color: #0d6efd; font-weight: bold; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
            code {{ background: #e9ecef; padding: 2px 6px; border-radius: 4px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>⚙️ Day 02: Routing & Request Handler Demo</h1>
            <p>Click links below to test dynamic routes, query parameters, and redirects:</p>
            <ul>
                <li><a href="{url_for('get_product', sku='PRD-1001')}">Custom Regex Route: Get Product (<code>PRD-1001</code>)</a></li>
                <li><a href="{url_for('search_products', category='peripherals', max_price=100)}">Query Parameters: Search Products (<code>?category=peripherals&max_price=100</code>)</a></li>
                <li><a href="{url_for('legacy_route')}">301 Redirect: Legacy Route (<code>/legacy-catalog</code>)</a></li>
                <li><a href="{url_for('admin_panel')}">Forbidden Route Test: Abort 403 (<code>/admin</code>)</a></li>
            </ul>
        </div>
    </body>
    </html>
    """


@app.route('/product/<regex(r"PRD-\\d{4}"):sku>')
def get_product(sku):
    """
    Route 2: Custom Regex Parameter Route ('/product/<sku>')
    Matches SKUs in the exact format PRD-XXXX (e.g., PRD-1001).
    """
    product = catalog.get(sku)
    if not product:
        # Abort request with HTTP 404 Not Found error
        abort(404, description=f"Product SKU '{sku}' was not found in catalog.")
    
    return jsonify({
        "status": "success",
        "sku": sku,
        "product_details": product
    }), 200


@app.route('/api/search')
def search_products():
    """
    Route 3: Query Parameter Search ('/api/search')
    Demonstrates extracting query string parameters using request.args.
    """
    category = request.args.get('category', default=None, type=str)
    max_price = request.args.get('max_price', default=None, type=float)
    
    results = {}
    for sku, item in catalog.items():
        if category and item['category'] != category:
            continue
        if max_price and item['price'] > max_price:
            continue
        results[sku] = item
        
    return jsonify({
        "applied_filters": {"category": category, "max_price": max_price},
        "total_results": len(results),
        "products": results
    }), 200


@app.route('/api/order', methods=['POST'])
def create_order():
    """
    Route 4: Order Creation POST Endpoint ('/api/order')
    Demonstrates inspecting POST JSON payloads, creating custom HTTP responses,
    setting custom headers, and storing secure cookies.
    """
    # Safely parse JSON payload (returns None if body is not valid JSON)
    payload = request.get_json(silent=True) or request.form.to_dict()
    
    if not payload or not payload.get('sku') or not payload.get('quantity'):
        return jsonify({
            "error": "Bad Request",
            "message": "Fields 'sku' and 'quantity' are required."
        }), 400
        
    order_id = "ORD-998811"
    response_data = {
        "status": "success",
        "order_id": order_id,
        "message": "Order placed successfully",
        "payload_received": payload,
        "client_ip": request.remote_addr
    }
    
    # 1. Create explicit HTTP 201 Created response
    resp = make_response(jsonify(response_data), 201)
    
    # 2. Attach custom HTTP headers
    resp.headers['X-Order-Status'] = 'QUEUED'
    
    # 3. Set secure HTTP-only cookie
    resp.set_cookie('last_order_id', order_id, max_age=300, httponly=True, samesite='Lax')
    
    return resp


@app.route('/legacy-catalog')
def legacy_route():
    """
    Route 5: HTTP 301 Permanent Redirect ('/legacy-catalog')
    Redirects incoming visitors dynamically to the index page.
    """
    return redirect(url_for('index'), code=301)


@app.route('/admin')
def admin_panel():
    """
    Route 6: Aborting Request Test ('/admin')
    Immediately halts execution and returns HTTP 403 Forbidden.
    """
    abort(403, description="Access restricted to authorized administrators only.")


# =============================================================================
# 4. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 02 Practice Application...")
    print("🌐 Open browser at: http://127.0.0.1:5000/")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
