"""
===============================================================================
Day 18 Practice Script: Self-Documenting REST API with Flask-Smorest & Swagger UI
===============================================================================
This script demonstrates:
1. Building Class-Based REST Resources (`MethodView`).
2. Integrating Marshmallow Schemas for input validation and output dumping.
3. Decorating routes with `@blp.arguments` and `@blp.response`.
4. Generating OpenAPI 3.0 JSON specifications automatically.
5. Serving a live interactive Swagger UI API testing sandbox (`/swagger-ui`).

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Self-Documenting REST API with Flask-Smorest.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
4. Open the Swagger UI interactive sandbox at: http://127.0.0.1:5000/swagger-ui
"""

from flask import Flask, jsonify, render_template_string
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
from marshmallow import Schema, fields, validate

app = Flask(__name__)

# =============================================================================
# 1. OpenAPI 3.0 & Swagger UI Configuration
# =============================================================================
app.config['API_TITLE'] = 'E-Commerce Inventory Microservice API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

api = Api(app)


# =============================================================================
# 2. In-Memory Data Storage & Marshmallow Schemas
# =============================================================================
items_db = {
    1: {"id": 1, "name": "Ultra-Wide Gaming Monitor", "category": "Electronics", "price": 499.99},
    2: {"id": 2, "name": "Noise Cancelling Headphones", "category": "Electronics", "price": 199.50},
    3: {"id": 3, "name": "Bamboo Standing Desk", "category": "Furniture", "price": 350.00}
}

class ItemSchema(Schema):
    """Schema for validating and serializing Item resources."""
    id = fields.Int(dump_only=True)                                     # Output only
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    category = fields.Str(required=True, validate=validate.OneOf(['Electronics', 'Furniture', 'Books']))
    price = fields.Float(required=True, validate=validate.Range(min=0.01))


class ItemUpdateSchema(Schema):
    """Schema for partial update (PATCH) requests."""
    name = fields.Str(validate=validate.Length(min=2, max=100))
    category = fields.Str(validate=validate.OneOf(['Electronics', 'Furniture', 'Books']))
    price = fields.Float(validate=validate.Range(min=0.01))


# =============================================================================
# 3. Smorest Blueprint & Class-Based Resources (MethodView)
# =============================================================================
blp = Blueprint('items', 'items', url_prefix='/api/v1/items', description='Operations on Items Inventory')


@blp.route('/')
class ItemListResource(MethodView):
    """Class-Based Resource handling collection operations (/api/v1/items)."""

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        """List all items in the inventory catalog."""
        return list(items_db.values())

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, new_item_data):
        """Create a new item in the inventory catalog."""
        new_id = max(items_db.keys(), default=0) + 1
        new_item_data['id'] = new_id
        items_db[new_id] = new_item_data
        return new_item_data


@blp.route('/<int:item_id>')
class ItemResource(MethodView):
    """Class-Based Resource handling single item operations (/api/v1/items/<id>)."""

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        """Fetch details for a specific item by ID."""
        if item_id not in items_db:
            abort(404, message=f"Item with ID #{item_id} does not exist.")
        return items_db[item_id]

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def patch(self, update_data, item_id):
        """Partially update attributes of an existing item."""
        if item_id not in items_db:
            abort(404, message=f"Item with ID #{item_id} does not exist.")
        items_db[item_id].update(update_data)
        return items_db[item_id]

    @blp.response(204)
    def delete(self, item_id):
        """Delete an item from inventory catalog."""
        if item_id not in items_db:
            abort(404, message=f"Item with ID #{item_id} does not exist.")
        del items_db[item_id]
        return ""


# Register Smorest Blueprint on API Manager
api.register_blueprint(blp)


# =============================================================================
# 4. Main Portal Home Route
# =============================================================================
@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Day 18 Self-Documenting REST API</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 40px; color: #333; }
                .card { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
                h2 { color: #2c3e50; margin-top: 0; }
                .badge { background: #e67e22; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; }
                .btn { display: inline-block; background: #27ae60; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 15px; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 10px; border-bottom: 1px solid #e9ecef; text-align: left; }
                th { background: #34495e; color: white; }
                code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; color: #c7254e; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>📑 Self-Documenting REST API with OpenAPI 3.0 (Day 18)</h2>
                <p>Framework: <span class="badge">Flask-Smorest + Marshmallow</span></p>

                <p>This microservice automatically generates an OpenAPI 3.0 specification and interactive Swagger UI sandbox directly from Python code annotations!</p>

                <a class="btn" href="/swagger-ui" target="_blank">🚀 Open Interactive Swagger UI Sandbox (/swagger-ui)</a>

                <h3>Endpoints Summary:</h3>
                <table>
                    <thead><tr><th>Verb</th><th>URL Path</th><th>Description</th></tr></thead>
                    <tbody>
                        <tr><td><code>GET</code></td><td><code>/api/v1/items/</code></td><td>List inventory items</td></tr>
                        <tr><td><code>POST</code></td><td><code>/api/v1/items/</code></td><td>Create item (Validated with ItemSchema)</td></tr>
                        <tr><td><code>GET</code></td><td><code>/api/v1/items/1</code></td><td>Fetch single item details</td></tr>
                        <tr><td><code>PATCH</code></td><td><code>/api/v1/items/1</code></td><td>Partially update item</td></tr>
                        <tr><td><code>DELETE</code></td><td><code>/api/v1/items/1</code></td><td>Remove item</td></tr>
                    </tbody>
                </table>

                <p style="margin-top: 25px;">
                    <a href="/openapi.json" target="_blank">Inspect OpenAPI 3.0 JSON Spec (/openapi.json)</a>
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
    print("🚀 Starting Day 18 Self-Documenting REST API Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("📑 Interactive Swagger UI Sandbox at: http://127.0.0.1:5000/swagger-ui")
    print("📡 Items API Collection at: http://127.0.0.1:5000/api/v1/items/")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
