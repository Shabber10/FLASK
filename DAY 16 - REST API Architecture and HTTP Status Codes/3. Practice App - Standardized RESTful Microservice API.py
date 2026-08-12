"""
===============================================================================
Day 16 Practice Script: Standardized RESTful Microservice API
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Defining Product ORM model with `to_dict()` JSON serialization method.
2. STEP 2: Authoring standardized RFC 7807 JSON error helper (`make_error_response`) & global error handlers.
3. STEP 3: Seeding initial database product records.
4. STEP 4: RESTful Collection Endpoints (`GET /api/v1/products` [200 OK], `POST /api/v1/products` [201 Created]).
5. STEP 5: RESTful Single Resource Endpoints (`GET`, `PUT`, `PATCH`, `DELETE` [204 No Content]).
6. STEP 6: Web UI API tester dashboard rendering `templates/index.html`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Standardized RESTful Microservice API.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from datetime import datetime
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day16-rest-api-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///day16_products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)


# =============================================================================
# STEP 1: Product ORM Model Definition with to_dict() Helper
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
        """Step 1: Converts SQLAlchemy model object into serializable Python dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
            "created_at": self.created_at.isoformat()
        }


# =============================================================================
# STEP 2: Standardized Error Helper (RFC 7807 Style) & Global Error Handlers
# =============================================================================
def make_error_response(status_code, error_type, message, details=None):
    """Step 2: Helper constructing standardized JSON error payloads."""
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
# STEP 3: Initial Database Seeding
# =============================================================================
with app.app_context():
    db.create_all()
    if not db.session.execute(db.select(Product)).scalars().first():
        p1 = Product(name="Pro Gaming Laptop", category="Electronics", price=1499.99, stock=15)
        p2 = Product(name="Ergonomic Desk Chair", category="Furniture", price=299.50, stock=8)
        p3 = Product(name="Mechanical Keyboard", category="Electronics", price=89.99, stock=30)
        db.session.add_all([p1, p2, p3])
        db.session.commit()


# =============================================================================
# STEP 4: RESTful Collection Endpoints (/api/v1/products)
# =============================================================================
@app.route('/api/v1/products', methods=['GET', 'POST'])
def handle_products_collection():
    if request.method == 'GET':
        # Step 4a: READ ALL (HTTP 200 OK)
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
        # Step 4b: CREATE NEW RESOURCE (HTTP 201 Created)
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


# =============================================================================
# STEP 5: RESTful Single Resource Endpoints (/api/v1/products/<id>)
# =============================================================================
@app.route('/api/v1/products/<int:product_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def handle_single_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return make_error_response(404, "NOT_FOUND", f"Product with ID {product_id} was not found.")

    if request.method == 'GET':
        # Step 5a: READ SINGLE (HTTP 200 OK)
        return jsonify({"status": "success", "data": product.to_dict()}), 200

    elif request.method == 'PUT':
        # Step 5b: FULL REPLACE (HTTP 200 OK)
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
        # Step 5c: PARTIAL UPDATE (HTTP 200 OK)
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
        # Step 5d: DELETE RESOURCE (HTTP 204 No Content)
        db.session.delete(product)
        db.session.commit()
        return '', 204


# =============================================================================
# STEP 6: Interactive Web UI API Tester Dashboard Handler (render_template)
# =============================================================================
@app.route('/')
def home():
    """Step 6: Renders templates/index.html REST API dashboard."""
    return render_template('index.html')


# =============================================================================
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 16 REST API Microservice...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("📡 Products API Collection at: http://127.0.0.1:5000/api/v1/products")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
