"""
Day 19 Practice Application: WSGI Middleware & Signal Dispatcher Engine
========================================================================
This application demonstrates:
1. Creating a custom PEP 3333 WSGI Middleware (AuditLoggingWSGIMiddleware)
   wrapping app.wsgi_app to intercept requests/responses and measure latency.
2. Integrating ProxyFix middleware for reverse proxy header parsing.
3. Defining custom Blinker Signals (user_registered_signal, order_placed_signal).
4. Subscribing decoupled event handlers to signals for audit logging.
5. Providing an interactive Web UI displaying real-time middleware and signal logs.
"""

import time
from flask import Flask, jsonify, request, render_template_string
from werkzeug.middleware.proxy_fix import ProxyFix
from blinker import Namespace

# ------------------------------------------------------------------------------
# 1. Custom PEP 3333 WSGI Middleware
# ------------------------------------------------------------------------------
WSGI_LOG_BUFFER = []

class AuditLoggingWSGIMiddleware:
    """Custom WSGI Middleware intercepting WSGI environ and start_response."""
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        start_time = time.time()
        path = environ.get('PATH_INFO', '')
        method = environ.get('REQUEST_METHOD', '')

        status_container = []

        def custom_start_response(status, headers, exc_info=None):
            status_container.append(status)
            latency_ms = round((time.time() - start_time) * 1000, 2)
            headers.append(('X-WSGI-Execution-Time-MS', str(latency_ms)))
            
            # Record execution log in buffer
            WSGI_LOG_BUFFER.append({
                "method": method,
                "path": path,
                "status": status,
                "latency_ms": latency_ms,
                "timestamp": time.strftime("%H:%M:%S")
            })
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)


# ------------------------------------------------------------------------------
# 2. Custom Application Signals (Blinker)
# ------------------------------------------------------------------------------
SIGNAL_LOG_BUFFER = []

signals = Namespace()
user_registered_signal = signals.signal('user-registered')
order_placed_signal = signals.signal('order-placed')

# Signal Subscribers
@user_registered_signal.connect
def handle_user_registered(sender, username, email, **extra):
    log_msg = f"[SIGNAL: user-registered] Account '{username}' ({email}) created!"
    print(log_msg)
    SIGNAL_LOG_BUFFER.append({"event": "user-registered", "details": log_msg, "time": time.strftime("%H:%M:%S")})

@order_placed_signal.connect
def handle_order_placed(sender, order_id, amount, **extra):
    log_msg = f"[SIGNAL: order-placed] Order #{order_id} placed for ${amount:.2f}"
    print(log_msg)
    SIGNAL_LOG_BUFFER.append({"event": "order-placed", "details": log_msg, "time": time.strftime("%H:%M:%S")})


# ------------------------------------------------------------------------------
# 3. Flask Application Setup & Middleware Registration
# ------------------------------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'day19-middleware-signals-secret'

# Wrap app.wsgi_app with ProxyFix and AuditLoggingWSGIMiddleware
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
app.wsgi_app = AuditLoggingWSGIMiddleware(app.wsgi_app)


# ------------------------------------------------------------------------------
# 4. HTML Dashboard UI
# ------------------------------------------------------------------------------
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 19 WSGI Middleware & Signals Masterclass</title>
    <style>
        body { font-family: Arial, sans-serif; background: #eef2f5; margin: 30px; }
        .card { max-width: 900px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
        .log-box { background: #1a202c; color: #a0aec0; padding: 15px; border-radius: 6px; font-family: monospace; font-size: 0.85em; height: 250px; overflow-y: scroll; }
        .btn { background: #2b6cb0; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; margin-right: 5px; }
        .badge { background: #319795; color: white; padding: 3px 6px; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🌐 Custom WSGI Middleware & Flask Signals (Day 19)</h2>
        <p>Demonstrating lower-level WSGI request/response wrapping and decoupled Blinker Signals.</p>

        <div>
            <button class="btn" onclick="triggerRegister()">Emit User Registration Signal</button>
            <button class="btn" onclick="triggerOrder()">Emit Order Placement Signal</button>
            <button class="btn" onclick="location.reload()">Refresh Page Logs</button>
        </div>

        <div class="grid">
            <div>
                <h3>WSGI Middleware Interception Log</h3>
                <div class="log-box">
                    {% for w in wsgi_logs %}
                        <div>[{{ w.timestamp }}] <span class="badge">{{ w.method }}</span> {{ w.path }} -> {{ w.status }} ({{ w.latency_ms }}ms)</div>
                    {% else %}
                        <div>No WSGI logs captured yet.</div>
                    {% endfor %}
                </div>
            </div>

            <div>
                <h3>Blinker Signals Event Log</h3>
                <div class="log-box">
                    {% for s in signal_logs %}
                        <div style="color: #68d391;">[{{ s.time }}] {{ s.details }}</div>
                    {% else %}
                        <div>No signals emitted yet. Click buttons above!</div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>

    <script>
        async function triggerRegister() {
            await fetch('/api/signup', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: 'user_' + Math.floor(Math.random()*1000), email: 'user@test.com'})
            });
            location.reload();
        }

        async function triggerOrder() {
            await fetch('/api/checkout', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({amount: (Math.random()*200 + 10).toFixed(2)})
            });
            location.reload();
        }
    </script>
</body>
</html>
"""


# ------------------------------------------------------------------------------
# 5. Route Handlers
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML, wsgi_logs=list(reversed(WSGI_LOG_BUFFER)), signal_logs=list(reversed(SIGNAL_LOG_BUFFER)))

@app.route('/api/signup', methods=['POST'])
def signup():
    payload = request.get_json(silent=True) or {}
    username = payload.get('username', 'new_user')
    email = payload.get('email', 'new@user.com')

    # Emit Custom Blinker Signal
    user_registered_signal.send(app, username=username, email=email)
    
    return jsonify({"status": "Success", "message": f"User {username} created and signal dispatched."}), 201

@app.route('/api/checkout', methods=['POST'])
def checkout():
    payload = request.get_json(silent=True) or {}
    amount = float(payload.get('amount', 49.99))
    order_id = int(time.time())

    # Emit Custom Blinker Signal
    order_placed_signal.send(app, order_id=order_id, amount=amount)

    return jsonify({"status": "Success", "order_id": order_id, "amount": amount}), 201


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 19 WSGI Middleware & Signals Application...")
    print("Dashboard UI at http://127.0.0.1:5000/")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
