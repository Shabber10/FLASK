"""
===============================================================================
Day 24 Practice Script: Real-Time Multi-Room Chat Application with WebSockets
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Setting up `Flask-SocketIO` bi-directional event handlers.
2. STEP 2: Built-in connection and disconnection event handlers (`@socketio.on('connect')`).
3. STEP 3: Multi-room channel management (`join_room`, `leave_room`, `emit(..., to=room)`).
4. STEP 4: REST API telemetry endpoint (`GET /api/v1/socket-stats`).
5. STEP 5: Web UI dashboard route handler rendering `templates/index.html`.
6. STEP 6: Launching WebSocket server using `socketio.run(app)`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Real-Time Multi-Room Chat Application.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import datetime
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day24-websocket-masterclass-secret'

# =============================================================================
# STEP 1: Initialize Flask-SocketIO
# =============================================================================
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# In-Memory Tracking for Active Sockets, Users & Rooms
connected_users = {}  # Maps SID -> {"username": str, "room": str}
active_rooms = {"Lobby": set(), "Tech-Support": set(), "General-Chat": set()}


# =============================================================================
# STEP 2: Built-In Connection & Disconnection Event Handlers
# =============================================================================
@socketio.on('connect')
def handle_connect():
    """Step 2a: Triggered when a new client connects via WebSocket handshake."""
    client_sid = request.sid
    connected_users[client_sid] = {"username": "Guest", "room": None}
    print(f"🔌 [CONNECTED] Socket SID: {client_sid}")
    emit('system_notification', {
        'msg': f'Connected to WebSocket Server (SID: {client_sid[:8]}...)',
        'active_users_count': len(connected_users)
    })


@socketio.on('disconnect')
def handle_disconnect():
    """Step 2b: Triggered when a client disconnects."""
    client_sid = request.sid
    user_info = connected_users.pop(client_sid, None)
    if user_info and user_info['room']:
        room = user_info['room']
        username = user_info['username']
        if room in active_rooms:
            active_rooms[room].discard(client_sid)
        print(f"❌ [DISCONNECTED] {username} (SID: {client_sid[:8]}) left room '{room}'")
        emit('room_notice', {
            'username': 'SYSTEM',
            'message': f"{username} disconnected.",
            'timestamp': datetime.datetime.now().strftime("%H:%M:%S")
        }, to=room)


# =============================================================================
# STEP 3: Multi-Room Channel Handlers (join_room, leave_room, room messages)
# =============================================================================
@socketio.on('join_room_channel')
def handle_join_room(data):
    """Step 3a: Adds client SID to a room channel."""
    client_sid = request.sid
    username = data.get('username', 'Anonymous')
    target_room = data.get('room', 'Lobby')

    # Leave old room if already in one
    old_room = connected_users[client_sid].get('room')
    if old_room and old_room != target_room:
        leave_room(old_room)
        if old_room in active_rooms:
            active_rooms[old_room].discard(client_sid)
        emit('room_notice', {'username': 'SYSTEM', 'message': f"{username} left channel."}, to=old_room)

    # Join target room
    join_room(target_room)
    connected_users[client_sid] = {"username": username, "room": target_room}
    if target_room not in active_rooms:
        active_rooms[target_room] = set()
    active_rooms[target_room].add(client_sid)

    print(f"👥 [JOIN] {username} joined channel '{target_room}'")

    # Notify room members
    emit('room_notice', {
        'username': 'SYSTEM',
        'message': f"🚀 {username} joined #{target_room}!",
        'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
        'room_user_count': len(active_rooms[target_room])
    }, to=target_room)


@socketio.on('send_room_message')
def handle_send_message(data):
    """Step 3b: Broadcasts chat message to all clients in target room."""
    client_sid = request.sid
    user_info = connected_users.get(client_sid, {})
    username = user_info.get('username', 'Anonymous')
    room = user_info.get('room', 'Lobby')
    message_text = data.get('message', '').strip()

    if message_text:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        # Target emission exclusively to clients in room
        emit('receive_room_message', {
            'username': username,
            'message': message_text,
            'room': room,
            'timestamp': timestamp
        }, to=room)


@socketio.on('typing_indicator')
def handle_typing(data):
    """Step 3c: Broadcasts 'typing...' status to other clients in room."""
    client_sid = request.sid
    user_info = connected_users.get(client_sid, {})
    username = user_info.get('username')
    room = user_info.get('room')
    is_typing = data.get('is_typing', False)

    if room:
        emit('user_typing_status', {
            'username': username,
            'is_typing': is_typing
        }, to=room, include_self=False)


# =============================================================================
# STEP 4: REST API Telemetry Endpoint
# =============================================================================
@app.route('/api/v1/socket-stats', methods=['GET'])
def get_stats():
    """Step 4: Returns active sockets and room count statistics."""
    room_stats = {r: len(sids) for r, sids in active_rooms.items()}
    return jsonify({
        "status": "success",
        "total_connected_sockets": len(connected_users),
        "active_rooms": room_stats
    }), 200


# =============================================================================
# STEP 5: Web UI Dashboard Route Handler (render_template)
# =============================================================================
@app.route('/')
def home():
    """Step 5: Renders templates/index.html dashboard."""
    return render_template('index.html')


# =============================================================================
# STEP 6: Main Entrypoint (socketio.run)
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 24 Real-Time WebSockets Server...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("📡 Socket Stats Telemetry at: http://127.0.0.1:5000/api/v1/socket-stats")
    print("=" * 75)
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
