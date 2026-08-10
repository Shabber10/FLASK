"""
===============================================================================
Day 16 Practice Script: Standardized RESTful Microservice API
===============================================================================
This script demonstrates:
1. Full RESTful CRUD routing (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).
2. Returning proper HTTP Status Codes (200 OK, 201 Created, 204 No Content, 400, 404, 422).
3. Standardized RFC 7807 JSON Error Responses.
4. HTTP Method Idempotency mechanics.
5. Interactive REST API Tester Dashboard and Web UI.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Standardized RESTful Microservice API.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from datetime import datetime
from flask import Flask, jsonify, request, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day16-rest-api-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///day16_products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)


# =============================================================================
# 1. Product ORM Model Definition
# =============================================================================
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
            "created_at": self.created_at.isoformat()
        }


# Seed initial database records if empty
with app.app_context():
    db.create_all()
    if not db.session.execute(db.select(Product)).scalars().first():
        p1 = Product(name="Pro Gaming Laptop", category="Electronics", price=1499.99, stock=15)
        p2 = Product(name="Ergonomic Desk Chair", category="Furniture", price=299.50, stock=8)
        p3 = Product(name="Mechanical Keyboard", category="Electronics", price=89.99, stock=30)
        db.session.add_all([p1, p2, p3])
        db.session.commit()


# =============================================================================
# 2. Standardized Error Helper (RFC 7807 Style)
# =============================================================================
def make_error_response(status_code, error_type, message, details=None):
    """Helper constructing standardized JSON error payloads."""
    payload = {
        "error": {
            "code": status_code,
            "type": error_type,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details or []
        }
    }
    return jsonify(payload), status_code


# Global Error Handlers
@app.errorhandler(404)
def not_found_handler(e):
    return make_error_response(404, "NOT_FOUND", "Target API endpoint resource does not exist.")

@app.errorhandler(405)
def method_not_allowed_handler(e):
    return make_error_response(405, "METHOD_NOT_ALLOWED", "HTTP method is not supported on this resource.")


# =============================================================================
# 3. RESTful API Resource Endpoints (/api/v1/products)
# =============================================================================

# GET /api/v1/products & POST /api/v1/products
@app.route('/api/v1/products', methods=['GET', 'POST'])
def handle_products_collection():
    if request.method == 'GET':
        # 1. READ ALL (HTTP 200 OK)
        category_filter = request.args.get('category')
        query = db.select(Product)
        if category_filter:
            query = query.filter_by(category=category_filter)
            
        products = db.session.execute(query).scalars().all()
        return jsonify({
            "status": "success",
            "count": len(products),
            "data": [p.to_dict() for p in products]
        }), 200

    elif request.method == 'POST':
        # 2. CREATE NEW RESOURCE (HTTP 201 Created)
        data = request.json or {}
        
        # Validation checks
        if not data.get('name') or not data.get('category') or 'price' not in data:
            return make_error_response(422, "UNPROCESSABLE_ENTITY", "Missing required fields 'name', 'category', or 'price'.")
            
        if data['price'] <= 0:
            return make_error_response(400, "BAD_REQUEST", "Price must be a positive number greater than zero.")

        product = Product(
            name=data['name'],
            category=data['category'],
            price=float(data['price']),
            stock=int(data.get('stock', 0))
        )
        db.session.add(product)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Product created successfully",
            "data": product.to_dict()
        }), 201


# GET /api/v1/products/<id>, PUT, PATCH, DELETE
@app.route('/api/v1/products/<int:product_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def handle_single_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return make_error_response(404, "NOT_FOUND", f"Product with ID {product_id} was not found.")

    if request.method == 'GET':
        # READ SINGLE (HTTP 200 OK)
        return jsonify({"status": "success", "data": product.to_dict()}), 200

    elif request.method == 'PUT':
        # FULL REPLACE (HTTP 200 OK)
        data = request.json or {}
        if not data.get('name') or not data.get('category') or 'price' not in data:
            return make_error_response(422, "UNPROCESSABLE_ENTITY", "PUT requires complete object replacement payload ('name', 'category', 'price').")

        product.name = data['name']
        product.category = data['category']
        product.price = float(data['price'])
        product.stock = int(data.get('stock', 0))
        db.session.commit()
        return jsonify({"status": "success", "message": "Product replaced entirely", "data": product.to_dict()}), 200

    elif request.method == 'PATCH':
        # PARTIAL UPDATE (HTTP 200 OK)
        data = request.json or {}
        if 'name' in data:
            product.name = data['name']
        if 'category' in data:
            product.category = data['category']
        if 'price' in data:
            product.price = float(data['price'])
        if 'stock' in data:
            product.stock = int(data['stock'])
            
        db.session.commit()
        return jsonify({"status": "success", "message": "Product partially updated", "data": product.to_dict()}), 200

    elif request.method == 'DELETE':
        # DELETE RESOURCE (HTTP 204 No Content)
        db.session.delete(product)
        db.session.commit()
        return '', 204


# =============================================================================
# 4. Interactive Web UI API Tester Dashboard
# =============================================================================
@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Day 16 REST API Microservice</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 40px; color: #333; }
                .card { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
                h2 { color: #2c3e50; margin-top: 0; }
                .badge-verb { padding: 4px 8px; border-radius: 4px; font-weight: bold; color: white; font-size: 0.85em; font-family: monospace; }
                .get { background: #61affe; } .post { background: #49cc90; }
                .put { background: #fca130; } .patch { background: #50e3c2; }
                .delete { background: #f93e3e; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 10px; border-bottom: 1px solid #e9ecef; text-align: left; }
                th { background: #34495e; color: white; }
                code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; color: #c7254e; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>🚀 Standardized RESTful Microservice API (Day 16)</h2>
                <p>This Flask application exposes full CRUD REST endpoints following RFC 7807 error standards:</p>

                <table>
                    <thead><tr><th>HTTP Verb</th><th>Endpoint URL</th><th>Description</th><th>Status Code</th></tr></thead>
                    <tbody>
                        <tr><td><span class="badge-verb get">GET</span></td><td><code>/api/v1/products</code></td><td>List all products</td><td><code>200 OK</code></td></tr>
                        <tr><td><span class="badge-verb post">POST</span></td><td><code>/api/v1/products</code></td><td>Create new product</td><td><code>201 Created</code></td></tr>
                        <tr><td><span class="badge-verb get">GET</span></td><td><code>/api/v1/products/1</code></td><td>Fetch single product</td><td><code>200 OK / 404</code></td></tr>
                        <tr><td><span class="badge-verb put">PUT</span></td><td><code>/api/v1/products/1</code></td><td>Full replace product</td><td><code>200 OK / 422</code></td></tr>
                        <tr><td><span class="badge-verb patch">PATCH</span></td><td><code>/api/v1/products/1</code></td><td>Partial update product</td><td><code>200 OK</code></td></tr>
                        <tr><td><span class="badge-verb delete">DELETE</span></td><td><code>/api/v1/products/1</code></td><td>Delete product</td><td><code>204 No Content</code></td></tr>
                    </tbody>
                </table>

                <p style="margin-top: 25px;">
                    <a href="/api/v1/products">Test GET /api/v1/products API</a> | 
                    <a href="/api/v1/products/999">Test GET /api/v1/products/999 (Triggers 404 JSON Error)</a>
                </p>
            </div>
        </body>
        </html>
    """)


# =============================================================================
# 5. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 16 REST API Microservice...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("📡 Products API Collection at: http://127.0.0.1:5000/api/v1/products")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
