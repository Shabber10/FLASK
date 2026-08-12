"""
===============================================================================
Day 18 Practice Script: Self-Documenting REST API with Flask-Smorest & Swagger UI
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Configuring OpenAPI 3.0 & Swagger UI settings (`OPENAPI_SWAGGER_UI_PATH`).
2. STEP 2: Defining Marshmallow Schemas (`ItemSchema`, `ItemUpdateSchema`) for input/output.
3. STEP 3: Class-Based Resource for Collection operations (`ItemListResource` using `MethodView`).
4. STEP 4: Class-Based Resource for Single Resource operations (`ItemResource` for `get`, `patch`, `delete`).
5. STEP 5: Registering Smorest Blueprint on API Manager (`api.register_blueprint(blp)`).
6. STEP 6: Main Portal Home Route rendering `templates/index.html` with links to `/swagger-ui` and `/openapi.json`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Self-Documenting REST API with Flask-Smorest.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
4. Open the Swagger UI interactive sandbox at: http://127.0.0.1:5000/swagger-ui
"""

from flask import Flask, jsonify, render_template
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
from marshmallow import Schema, fields, validate

app = Flask(__name__)

# =============================================================================
# STEP 1: OpenAPI 3.0 & Swagger UI Configuration
# =============================================================================
app.config['API_TITLE'] = 'E-Commerce Inventory Microservice API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

api = Api(app)


# =============================================================================
# STEP 2: In-Memory Data Storage & Marshmallow Schemas
# =============================================================================
items_db = {
    1: {"id": 1, "name": "Ultra-Wide Gaming Monitor", "category": "Electronics", "price": 499.99},
    2: {"id": 2, "name": "Noise Cancelling Headphones", "category": "Electronics", "price": 199.50},
    3: {"id": 3, "name": "Bamboo Standing Desk", "category": "Furniture", "price": 350.00}
}

class ItemSchema(Schema):
    """Step 2a: Schema for validating and serializing Item resources."""
    id = fields.Int(dump_only=True)                                     # Output only
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    category = fields.Str(required=True, validate=validate.OneOf(['Electronics', 'Furniture', 'Books']))
    price = fields.Float(required=True, validate=validate.Range(min=0.01))


class ItemUpdateSchema(Schema):
    """Step 2b: Schema for partial update (PATCH) requests."""
    name = fields.Str(validate=validate.Length(min=2, max=100))
    category = fields.Str(validate=validate.OneOf(['Electronics', 'Furniture', 'Books']))
    price = fields.Float(validate=validate.Range(min=0.01))


# =============================================================================
# STEP 3 & 4: Smorest Blueprint & Class-Based Resources (MethodView)
# =============================================================================
blp = Blueprint('items', 'items', url_prefix='/api/v1/items', description='Operations on Items Inventory')


@blp.route('/')
class ItemListResource(MethodView):
    """Step 3: Class-Based Resource handling collection operations (/api/v1/items)."""

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
    """Step 4: Class-Based Resource handling single item operations (/api/v1/items/<id>)."""

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


# =============================================================================
# STEP 5: Register Smorest Blueprint on API Manager
# =============================================================================
api.register_blueprint(blp)


# =============================================================================
# STEP 6: Main Portal Home Route (render_template)
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
    print("🚀 Starting Day 18 Self-Documenting REST API Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("📑 Interactive Swagger UI Sandbox at: http://127.0.0.1:5000/swagger-ui")
    print("📡 Items API Collection at: http://127.0.0.1:5000/api/v1/items/")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
