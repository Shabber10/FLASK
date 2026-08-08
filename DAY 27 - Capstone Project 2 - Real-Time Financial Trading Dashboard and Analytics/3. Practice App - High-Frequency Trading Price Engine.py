"""
Day 27 Practice Application: Real-Time Financial Trading Engine
================================================================
This application demonstrates:
1. Spawning a cooperative background streaming task (socketio.start_background_task).
2. Generating high-frequency simulated stock & crypto price ticks.
3. Subscribing clients to specific ticker symbol rooms (join_room('AAPL'), join_room('BTC')).
4. Emitting sub-100ms real-time price updates (socketio.emit(..., to=symbol)).
5. Interactive Web Dashboard with live price streaming UI and room subscription controls.
"""

import time
import random
from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day27-trading-masterclass-secret'

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# In-Memory Ticker Prices & Background Thread Flag
PRICES = {
    'AAPL': 175.50,
    'GOOGL': 140.20,
    'TSLA': 240.10,
    'BTC': 62500.00
}
background_thread_started = False


# ------------------------------------------------------------------------------
# 1. Background Price Stream Generator
# ------------------------------------------------------------------------------
def background_price_generator():
    """Background task generating live ticks every 800ms."""
    print("[STREAM ENGINE] Background price generator thread started!")
    while True:
        socketio.sleep(0.8) # Cooperative non-blocking sleep
        for symbol in PRICES.keys():
            delta = round(random.uniform(-1.25, 1.25), 2)
            PRICES[symbol] = max(1.0, round(PRICES[symbol] + delta, 2))

            # Emit price tick strictly to clients in symbol room
            socketio.emit('price_update', {
                "symbol": symbol,
                "price": f"{PRICES[symbol]:.2f}",
                "change": delta,
                "timestamp": time.strftime("%H:%M:%S")
            }, to=symbol)


# ------------------------------------------------------------------------------
# 2. Socket.IO Event Handlers
# ------------------------------------------------------------------------------
@socketio.on('connect')
def handle_connect():
    global background_thread_started
    print(f"[SOCKETIO] Client Connected: SID={request.sid}")
    if not background_thread_started:
        socketio.start_background_task(target=background_price_generator)
        background_thread_started = True

@socketio.on('subscribe_ticker')
def handle_subscribe(data):
    symbol = data.get('symbol', 'AAPL')
    join_room(symbol)
    emit('system_notice', {"text": f"Subscribed to real-time ticker stream: {symbol}"})

@socketio.on('unsubscribe_ticker')
def handle_unsubscribe(data):
    symbol = data.get('symbol', 'AAPL')
    leave_room(symbol)
    emit('system_notice', {"text": f"Unsubscribed from ticker stream: {symbol}"})


# ------------------------------------------------------------------------------
# 3. HTML Real-Time Trading Terminal Dashboard
# ------------------------------------------------------------------------------
TRADING_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 27 Real-Time Financial Trading Engine</title>
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; margin: 25px; }
        .card { max-width: 900px; margin: auto; background: #1e293b; padding: 25px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        .ticker-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-top: 20px; }
        .ticker-card { background: #334155; padding: 15px; border-radius: 6px; text-align: center; }
        .price { font-size: 1.5em; font-weight: bold; font-family: monospace; margin: 10px 0; }
        .up { color: #4ade80; }
        .down { color: #f87171; }
        .btn { background: #3b82f6; color: white; border: none; padding: 8px 14px; border-radius: 4px; cursor: pointer; }
        .btn-danger { background: #ef4444; }
        .stream-log { background: #020617; color: #38bdf8; padding: 15px; border-radius: 6px; font-family: monospace; font-size: 0.85em; margin-top: 20px; height: 200px; overflow-y: scroll; }
    </style>
</head>
<body>
    <div class="card">
        <h2>📈 Real-Time Financial Trading Terminal (Day 27)</h2>
        <p>Sub-100ms WebSocket Streaming Engine using Socket.IO Room Channels.</p>

        <div class="ticker-grid">
            <div class="ticker-card">
                <h3>AAPL</h3>
                <div id="price_AAPL" class="price">$175.50</div>
                <button class="btn" onclick="subscribe('AAPL')">Subscribe AAPL</button>
            </div>
            <div class="ticker-card">
                <h3>GOOGL</h3>
                <div id="price_GOOGL" class="price">$140.20</div>
                <button class="btn" onclick="subscribe('GOOGL')">Subscribe GOOGL</button>
            </div>
            <div class="ticker-card">
                <h3>TSLA</h3>
                <div id="price_TSLA" class="price">$240.10</div>
                <button class="btn" onclick="subscribe('TSLA')">Subscribe TSLA</button>
            </div>
            <div class="ticker-card">
                <h3>BTC</h3>
                <div id="price_BTC" class="price">$62500.00</div>
                <button class="btn" onclick="subscribe('BTC')">Subscribe BTC</button>
            </div>
        </div>

        <div id="log" class="stream-log">Select a ticker above to subscribe to live price ticks...</div>
    </div>

    <script>
        const socket = io();
        let activeSymbol = null;

        socket.on('connect', () => {
            console.log("Connected to Real-Time Trading Engine!");
        });

        socket.on('system_notice', (data) => {
            const log = document.getElementById('log');
            log.innerHTML = `<div>[SYSTEM] ${data.text}</div>` + log.innerHTML;
        });

        socket.on('price_update', (data) => {
            const el = document.getElementById('price_' + data.symbol);
            if (el) {
                const isUp = data.change >= 0;
                el.className = 'price ' + (isUp ? 'up' : 'down');
                el.innerText = '$' + data.price;
            }

            const log = document.getElementById('log');
            log.innerHTML = `<div>[${data.timestamp}] TICK: ${data.symbol} -> $${data.price} (${data.change >= 0 ? '+' : ''}${data.change})</div>` + log.innerHTML;
        });

        function subscribe(symbol) {
            if (activeSymbol) {
                socket.emit('unsubscribe_ticker', { symbol: activeSymbol });
            }
            activeSymbol = symbol;
            socket.emit('subscribe_ticker', { symbol: symbol });
        }
    </script>
</body>
</html>
"""


# ------------------------------------------------------------------------------
# 4. Route Handlers
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template_string(TRADING_HTML)


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 27 Financial Trading Engine...")
    print("Trading Terminal UI at http://127.0.0.1:5000/")
    print("=" * 70)
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
