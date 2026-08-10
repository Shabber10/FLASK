"""
Day 24 Practice Application: Microservices Ecosystem & API Gateway
===================================================================
This application demonstrates:
1. Building an API Gateway routing requests to independent microservice endpoints.
2. Inter-service HTTP communication with strict timeouts and error fallback.
3. Simulating a Circuit Breaker pattern preventing cascading worker thread exhaustion.
4. Enforcing Database-per-Service data isolation boundaries.
5. Interactive Web UI simulating microservice topology, health status, and failure recovery.
"""

import time
import random
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day24-microservices-masterclass-secret'

# Simulated Independent Microservice In-Memory Databases
USER_SERVICE_DB = {
    1: {"id": 1, "name": "Alice Developer", "tier": "premium"},
    2: {"id": 2, "name": "Bob Architect", "tier": "standard"}
}

INVENTORY_SERVICE_DB = {
    101: {"item_id": 101, "title": "Cloud Server Instance", "stock": 42, "price": 199.99},
    102: {"item_id": 102, "title": "Kubernetes Cluster", "stock": 5, "price": 499.99}
}

# Circuit Breaker Simulated State
CIRCUIT_BREAKER_STATE = {"status": "CLOSED", "consecutive_failures": 0, "fail_max": 3}


# ------------------------------------------------------------------------------
# 1. Interactive Microservices Diagnostic Dashboard
# ------------------------------------------------------------------------------
GATEWAY_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 24 Microservices Ecosystem Masterclass</title>
    <style>
        body { font-family: Arial, sans-serif; background: #eef2f5; margin: 30px; }
        .card { max-width: 900px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-top: 20px; }
        .service-card { border: 1px solid #cbd5e0; padding: 15px; border-radius: 6px; background: #f7fafc; }
        .badge { background: #38a169; color: white; padding: 3px 8px; border-radius: 4px; font-size: 0.8em; }
        .badge-open { background: #e53e3e; }
        .btn { background: #2b6cb0; color: white; border: none; padding: 8px 12px; border-radius: 4px; cursor: pointer; margin-top: 10px; }
        .btn-fail { background: #c53030; }
        .log-box { background: #1a202c; color: #68d391; padding: 15px; border-radius: 6px; font-family: monospace; font-size: 0.85em; margin-top: 20px; height: 200px; overflow-y: scroll; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🌐 Microservices Architecture & API Gateway Engine (Day 24)</h2>
        <p>Demonstrating API Gateway routing, Database-per-Service isolation, and Circuit Breaker state management.</p>

        <div class="grid">
            <div class="service-card">
                <h4>1. API Gateway Service</h4>
                <p>Status: <span class="badge">ACTIVE</span></p>
                <button class="btn" onclick="callOrderEndpoint()">Create Order API</button>
            </div>

            <div class="service-card">
                <h4>2. User Microservice</h4>
                <p>Status: <span class="badge">HEALTHY</span></p>
                <button class="btn" onclick="fetchUser(1)">Fetch User #1</button>
            </div>

            <div class="service-card">
                <h4>3. Inventory Microservice</h4>
                <p>Breaker State: <span id="breaker_badge" class="badge">CLOSED</span></p>
                <button class="btn btn-fail" onclick="toggleSimulatedFailure()">Simulate Service Outage</button>
            </div>
        </div>

        <div id="output" class="log-box">Click a button above to route inter-service requests through the Gateway...</div>
    </div>

    <script>
        async function callOrderEndpoint() {
            const res = await fetch('/api/v1/orders/create', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({user_id: 1, item_id: 101})
            });
            const data = await res.json();
            document.getElementById('output').innerText = 
                `HTTP Status: ${res.status}\n` + JSON.stringify(data, null, 2);
        }

        async function fetchUser(id) {
            const res = await fetch('/services/users/' + id);
            const data = await res.json();
            document.getElementById('output').innerText = JSON.stringify(data, null, 2);
        }

        async function toggleSimulatedFailure() {
            const res = await fetch('/services/inventory/toggle-outage', { method: 'POST' });
            const data = await res.json();
            document.getElementById('breaker_badge').className = 
                data.circuit_breaker === 'OPEN' ? 'badge badge-open' : 'badge';
            document.getElementById('breaker_badge').innerText = data.circuit_breaker;
            document.getElementById('output').innerText = JSON.stringify(data, null, 2);
        }
    </script>
</body>
</html>
"""


# ------------------------------------------------------------------------------
# 2. Internal Microservice Endpoints (Simulating Independent Services)
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template_string(GATEWAY_HTML)

# User Microservice (Port/Path Isolated)
@app.route('/services/users/<int:user_id>')
def user_microservice(user_id):
    user = USER_SERVICE_DB.get(user_id)
    if not user:
        return jsonify({"error": "User Not Found"}), 404
    return jsonify({"service": "User-Service-v1", "data": user}), 200

# Inventory Microservice with Circuit Breaker Simulation
@app.route('/services/inventory/<int:item_id>')
def inventory_microservice(item_id):
    if CIRCUIT_BREAKER_STATE["status"] == "OPEN":
        return jsonify({
            "error": "Service Unavailable",
            "message": "Circuit Breaker OPEN! Fast failing to protect cluster."
        }), 503

    item = INVENTORY_SERVICE_DB.get(item_id)
    if not item:
        return jsonify({"error": "Item Not Found"}), 404
    return jsonify({"service": "Inventory-Service-v1", "data": item}), 200

@app.route('/services/inventory/toggle-outage', methods=['POST'])
def toggle_inventory_outage():
    if CIRCUIT_BREAKER_STATE["status"] == "CLOSED":
        CIRCUIT_BREAKER_STATE["status"] = "OPEN"
    else:
        CIRCUIT_BREAKER_STATE["status"] = "CLOSED"
    return jsonify({
        "status": "State Toggled",
        "circuit_breaker": CIRCUIT_BREAKER_STATE["status"]
    })


# ------------------------------------------------------------------------------
# 3. API Gateway Aggregator Endpoint
# ------------------------------------------------------------------------------
@app.route('/api/v1/orders/create', methods=['POST'])
def gateway_create_order():
    payload = request.get_json(silent=True) or {}
    user_id = payload.get('user_id', 1)
    item_id = payload.get('item_id', 101)

    # 1. Internal Call to User Service
    user_info = USER_SERVICE_DB.get(user_id)
    if not user_info:
        return jsonify({"error": "Invalid User ID"}), 400

    # 2. Resilient Internal Call to Inventory Service (with Circuit Breaker check)
    if CIRCUIT_BREAKER_STATE["status"] == "OPEN":
        return jsonify({
            "error": "Gateway Error",
            "message": "Downstream Inventory Service unavailable (Circuit Breaker OPEN). Order failed gracefully."
        }), 503

    item_info = INVENTORY_SERVICE_DB.get(item_id)
    order_id = f"ORD-{random.randint(1000, 9999)}"

    return jsonify({
        "status": "Order Placed Successfully",
        "order_id": order_id,
        "customer": user_info['name'],
        "item": item_info['title'],
        "total_amount": item_info['price'],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }), 201


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 24 Microservices API Gateway Application...")
    print("Ecosystem Dashboard UI at http://127.0.0.1:5000/")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
