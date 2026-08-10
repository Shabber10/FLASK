"""
Day 02 Practice Application: Dynamic Routing & Request Inspection
===================================================================
This application demonstrates:
1. Registering custom regex URL path converters.
2. Handling multiple HTTP verbs (GET, POST, PUT, DELETE).
3. Extracting URL query parameters, form data, and JSON payloads.
4. Setting custom response headers and HTTP cookies using make_response().
5. Aborting requests and performing dynamic URL redirects with url_for().
"""

from flask import Flask, request, jsonify, make_response, redirect, url_for, abort
from werkzeug.routing import BaseConverter

# ------------------------------------------------------------------------------
# 1. Custom Regex URL Converter Definition
# ------------------------------------------------------------------------------
class RegexConverter(BaseConverter):
    """Custom Converter accepting regex patterns inside URL rules."""
    def __init__(self, url_map, *items):
        super().__init__(url_map)
        self.regex = items[0]


# ------------------------------------------------------------------------------
# 2. Flask Application Setup
# ------------------------------------------------------------------------------
app = Flask(__name__)

# Register custom regex converter on URL map
app.url_map.converters['regex'] = RegexConverter

# Simulated In-Memory Product Database
catalog = {
    "PRD-1001": {"name": "Mechanical Keyboard", "price": 89.99, "category": "peripherals"},
    "PRD-1002": {"name": "Gaming Mouse", "price": 49.99, "category": "peripherals"},
    "PRD-2001": {"name": "Ultra-Wide Monitor", "price": 499.99, "category": "displays"}
}


# ------------------------------------------------------------------------------
# 3. Route Handlers
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    """Index Endpoint listing sample navigation links."""
    return f"""
    <h2>Day 02: Routing & Request Handler Demo</h2>
    <ul>
        <li><a href="{url_for('get_product', sku='PRD-1001')}">Get Product (PRD-1001)</a></li>
        <li><a href="{url_for('search_products', category='peripherals', max_price=100)}">Search Products (Query Parameters)</a></li>
        <li><a href="{url_for('legacy_route')}">Legacy Route Redirect</a></li>
    </ul>
    """

# Custom Regex Route: SKUs must match PRD-XXXX format
@app.route('/product/<regex(r"PRD-\\d{4}"):sku>')
def get_product(sku):
    """Fetches product details using custom regex URL converter."""
    product = catalog.get(sku)
    if not product:
        abort(404, description=f"Product with SKU '{sku}' not found in catalog.")
    return jsonify({"sku": sku, "details": product})

@app.route('/api/search')
def search_products():
    """Demonstrates extracting query string parameters using request.args."""
    category = request.args.get('category', type=str)
    max_price = request.args.get('max_price', type=float)
    
    results = {}
    for sku, item in catalog.items():
        if category and item['category'] != category:
            continue
        if max_price and item['price'] > max_price:
            continue
        results[sku] = item
        
    return jsonify({
        "filters": {"category": category, "max_price": max_price},
        "count": len(results),
        "results": results
    })

@app.route('/api/order', methods=['POST'])
def create_order():
    """Demonstrates inspecting POST payload, headers, and setting secure cookies."""
    # Check if request body contains JSON
    payload = request.get_json(silent=True) or request.form.to_dict()
    
    if not payload.get('sku') or not payload.get('quantity'):
        return jsonify({"error": "Bad Request", "message": "Fields 'sku' and 'quantity' required"}), 400
        
    order_id = "ORD-998811"
    response_data = {
        "order_id": order_id,
        "status": "Order Placed Successfully",
        "payload_received": payload,
        "client_ip": request.remote_addr
    }
    
    resp = make_response(jsonify(response_data), 201)
    resp.headers['X-Order-Status'] = 'QUEUED'
    resp.set_cookie('last_order', order_id, max_age=300, httponly=True, samesite='Lax')
    return resp

@app.route('/legacy-catalog')
def legacy_route():
    """Performs HTTP 301 Permanent Redirect using url_for."""
    return redirect(url_for('index'), code=301)


# ------------------------------------------------------------------------------
# 4. Entrypoint
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 02 Practice Application...")
    print("Test endpoints at http://127.0.0.1:5000/")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
