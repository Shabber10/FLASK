"""
===============================================================================
Day 24 Practice Script: Real-Time Multi-Room Chat Application with WebSockets
===============================================================================
This script demonstrates:
1. Setting up `Flask-SocketIO` bi-directional event handlers.
2. Managing multi-room channels (`join_room`, `leave_room`).
3. Targeted broadcasting to rooms (`emit('event', payload, to=room)`).
4. Real-time typing indicators and user connection status tracking.
5. REST API telemetry endpoint (`GET /api/v1/socket-stats`).
6. Complete interactive HTML/JS Web UI chat portal with Socket.IO client.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - Real-Time Multi-Room Chat Application.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import datetime
from flask import Flask, jsonify, render_template_string, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day24-websocket-masterclass-secret'

# Initialize Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# In-Memory Tracking for Active Sockets, Users & Rooms
connected_users = {}  # Maps SID -> {"username": str, "room": str}
active_rooms = {"Lobby": set(), "Tech-Support": set(), "General-Chat": set()}


# =============================================================================
# 1. Socket.IO Event Handlers
# =============================================================================

@socketio.on('connect')
def handle_connect():
    """Triggered when a new client connects via WebSocket handshake."""
    client_sid = request.sid
    connected_users[client_sid] = {"username": "Guest", "room": None}
    print(f"🔌 [CONNECTED] Socket SID: {client_sid}")
    emit('system_notification', {
        'msg': f'Connected to WebSocket Server (SID: {client_sid[:8]}...)',
        'active_users_count': len(connected_users)
    })


@socketio.on('disconnect')
def handle_disconnect():
    """Triggered when a client disconnects."""
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


@socketio.on('join_room_channel')
def handle_join_room(data):
    """Adds client SID to a room channel."""
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
    """Broadcasts chat message to all clients in target room."""
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
    """Broadcasts 'typing...' status to other clients in room."""
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
# 2. REST API Telemetry Endpoint
# =============================================================================
@app.route('/api/v1/socket-stats', methods=['GET'])
def get_stats():
    room_stats = {r: len(sids) for r, sids in active_rooms.items()}
    return jsonify({
        "status": "success",
        "total_connected_sockets": len(connected_users),
        "active_rooms": room_stats
    }), 200


# =============================================================================
# 3. Interactive Web UI Chat Portal with Socket.IO CDN Client
# =============================================================================
@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Day 24 WebSocket Multi-Room Chat</title>
            <!-- Load Official Socket.IO Browser Client -->
            <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 30px; color: #333; }
                .card { max-width: 900px; margin: auto; background: white; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); overflow: hidden; display: flex; flex-direction: column; }
                .header { background: #2c3e50; color: white; padding: 20px; text-align: center; }
                .chat-container { display: flex; height: 480px; }
                .sidebar { width: 220px; background: #34495e; color: white; padding: 15px; }
                .sidebar h4 { margin-top: 0; color: #16a085; }
                .room-btn { width: 100%; padding: 10px; background: #2c3e50; color: white; border: none; text-align: left; margin-bottom: 8px; border-radius: 4px; cursor: pointer; font-weight: bold; }
                .room-btn.active { background: #16a085; }
                .main-chat { flex: 1; display: flex; flex-direction: column; background: #f8f9fa; }
                .messages { flex: 1; padding: 15px; overflow-y: auto; font-family: monospace; font-size: 14px; }
                .msg-bubble { margin-bottom: 10px; padding: 8px 12px; border-radius: 6px; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
                .msg-system { background: #e8f8f5; color: #16a085; font-style: italic; }
                .input-bar { display: flex; padding: 12px; background: white; border-top: 1px solid #e9ecef; }
                .input-bar input { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 4px; margin-right: 10px; }
                .input-bar button { padding: 10px 20px; background: #27ae60; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; }
                .typing-text { padding: 4px 15px; font-size: 12px; color: #7f8c8d; font-style: italic; }
            </style>
        </head>
        <body>
            <div class="card">
                <div class="header">
                    <h2 style="margin:0;">💬 Real-Time Multi-Room Chat (Day 24)</h2>
                    <small>Engine: Flask-SocketIO WebSockets</small>
                </div>

                <div class="chat-container">
                    <div class="sidebar">
                        <h4>Channels:</h4>
                        <button class="room-btn active" onclick="switchRoom('Lobby')"># Lobby</button>
                        <button class="room-btn" onclick="switchRoom('Tech-Support')"># Tech-Support</button>
                        <button class="room-btn" onclick="switchRoom('General-Chat')"># General-Chat</button>

                        <h4 style="margin-top: 30px;">User Setup:</h4>
                        <input type="text" id="username_input" value="User_" style="width:90%; padding:6px; border-radius:4px; border:none;" onchange="updateUsername()">
                    </div>

                    <div class="main-chat">
                        <div class="messages" id="messages_box">
                            <div class="msg-bubble msg-system">Connecting to WebSocket server...</div>
                        </div>

                        <div class="typing-text" id="typing_box"></div>

                        <div class="input-bar">
                            <input type="text" id="msg_input" placeholder="Type a message and press Enter..." oninput="handleTyping()" onkeypress="if(event.key==='Enter') sendMessage()">
                            <button onclick="sendMessage()">Send</button>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                const socket = io();
                let currentRoom = 'Lobby';
                let currentUsername = 'DevUser_' + Math.floor(Math.random() * 1000);
                document.getElementById('username_input').value = currentUsername;

                socket.on('connect', () => {
                    joinChannel(currentRoom);
                });

                socket.on('system_notification', (data) => {
                    appendMessage("SYSTEM", data.msg, "msg-system");
                });

                socket.on('room_notice', (data) => {
                    appendMessage("SYSTEM", data.message, "msg-system");
                });

                socket.on('receive_room_message', (data) => {
                    appendMessage(data.username, data.message + " <small style='color:#999;'>(" + data.timestamp + ")</small>");
                });

                socket.on('user_typing_status', (data) => {
                    const typingBox = document.getElementById('typing_box');
                    typingBox.innerHTML = data.is_typing ? data.username + " is typing..." : "";
                });

                function joinChannel(room) {
                    currentRoom = room;
                    socket.emit('join_room_channel', { username: currentUsername, room: currentRoom });
                    document.getElementById('messages_box').innerHTML = "<div class='msg-bubble msg-system'>Joined channel #" + room + "</div>";
                }

                function switchRoom(room) {
                    document.querySelectorAll('.room-btn').forEach(b => b.classList.remove('active'));
                    event.target.classList.add('active');
                    joinChannel(room);
                }

                function updateUsername() {
                    currentUsername = document.getElementById('username_input').value || 'Anonymous';
                    joinChannel(currentRoom);
                }

                function sendMessage() {
                    const input = document.getElementById('msg_input');
                    const text = input.value.trim();
                    if (text) {
                        socket.emit('send_room_message', { message: text });
                        socket.emit('typing_indicator', { is_typing: false });
                        input.value = '';
                    }
                }

                let typingTimeout;
                function handleTyping() {
                    socket.emit('typing_indicator', { is_typing: true });
                    clearTimeout(typingTimeout);
                    typingTimeout = setTimeout(() => {
                        socket.emit('typing_indicator', { is_typing: false });
                    }, 1500);
                }

                function appendMessage(user, msg, extraClass = '') {
                    const box = document.getElementById('messages_box');
                    const div = document.createElement('div');
                    div.className = 'msg-bubble ' + extraClass;
                    div.innerHTML = "<strong>" + user + ":</strong> " + msg;
                    box.appendChild(div);
                    box.scrollTop = box.scrollHeight;
                }
            </script>
        </body>
        </html>
    """)


# =============================================================================
# 4. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 24 Real-Time WebSockets Server...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("📡 Socket Stats Telemetry at: http://127.0.0.1:5000/api/v1/socket-stats")
    print("=" * 75)
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
