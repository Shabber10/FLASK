# Day 16 Practice App: Standardized RESTful API
from flask import Flask, jsonify, request

app = Flask(__name__)

items_db = {1: {"id": 1, "name": "Laptop", "price": 1200.0}}

def format_error(status_code, error_type, message):
    return jsonify({
        "error": {
            "code": status_code,
            "type": error_type,
            "message": message
        }
    }), status_code

@app.route('/api/items', methods=['GET', 'POST'])
def handle_items():
    if request.method == 'GET':
        return jsonify(list(items_db.values()))
    
    data = request.json or {}
    if not data.get('name') or 'price' not in data:
        return format_error(400, "BAD_REQUEST", "Missing required fields 'name' or 'price'")
        
    new_id = max(items_db.keys(), default=0) + 1
    item = {"id": new_id, "name": data['name'], "price": data['price']}
    items_db[new_id] = item
    return jsonify(item), 201

if __name__ == '__main__':
    app.run(debug=True)
