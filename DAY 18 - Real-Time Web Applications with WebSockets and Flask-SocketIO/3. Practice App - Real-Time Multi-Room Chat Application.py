"""
Day 18 Practice Application: Real-Time Multi-Room Chat System
============================================================
This application demonstrates:
1. Initializing Flask-SocketIO with event handlers (@socketio.on).
2. Handling connect/disconnect lifecycle events and tracking client sid.
3. Implementing multi-room channel join & leave mechanics (join_room, leave_room).
4. Emitting targeted room messages (emit(..., to=room)) and global broadcasts.
5. Providing an interactive Web UI with Socket.IO client JS library integration.
"""

from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day18-socketio-masterclass-secret'

# Initialize Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Track online clients and room rosters
ACTIVE_ROOMS = ['#general', '#python', '#flask']
ONLINE_CLIENTS = {}


# ------------------------------------------------------------------------------
# 1. Socket.IO Event Handlers
# ------------------------------------------------------------------------------
@socketio.on('connect')
def handle_connect():
    sid = request.sid
    ONLINE_CLIENTS[sid] = {"username": "Guest", "room": None}
    print(f"[SOCKETIO] Client Connected: SID={sid}")
    emit('system_status', {"online_count": len(ONLINE_CLIENTS), "rooms": ACTIVE_ROOMS}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    client_info = ONLINE_CLIENTS.pop(sid, None)
    if client_info and client_info['room']:
        leave_room(client_info['room'])
        emit('chat_message', {
            "username": "System",
            "text": f"{client_info['username']} disconnected.",
            "type": "system"
        }, to=client_info['room'])
    print(f"[SOCKETIO] Client Disconnected: SID={sid}")
    emit('system_status', {"online_count": len(ONLINE_CLIENTS), "rooms": ACTIVE_ROOMS}, broadcast=True)

@socketio.on('join_room')
def handle_join_room(data):
    username = data.get('username', 'Anonymous').strip()
    room = data.get('room', '#general')
    sid = request.sid

    if sid in ONLINE_CLIENTS:
        old_room = ONLINE_CLIENTS[sid]['room']
        if old_room:
            leave_room(old_room)
            emit('chat_message', {"username": "System", "text": f"{username} left {old_room}", "type": "system"}, to=old_room)

        ONLINE_CLIENTS[sid]['username'] = username
        ONLINE_CLIENTS[sid]['room'] = room
        join_room(room)

        emit('chat_message', {
            "username": "System",
            "text": f"Welcome {username}! You joined {room}",
            "type": "system"
        })
        
        emit('chat_message', {
            "username": "System",
            "text": f"{username} has joined {room}",
            "type": "system"
        }, to=room, include_self=False)

@socketio.on('send_message')
def handle_send_message(data):
    sid = request.sid
    client_info = ONLINE_CLIENTS.get(sid)
    if not client_info or not client_info['room']:
        return

    text = data.get('text', '').strip()
    if text:
        emit('chat_message', {
            "username": client_info['username'],
            "text": text,
            "room": client_info['room'],
            "type": "user"
        }, to=client_info['room'])


# ------------------------------------------------------------------------------
# 2. HTML & Socket.IO Client Web UI
# ------------------------------------------------------------------------------
CHAT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 18 Real-Time Chat Engine</title>
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; background: #eef2f5; margin: 20px; }
        .card { max-width: 800px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .chat-box { height: 350px; border: 1px solid #ccc; border-radius: 6px; padding: 15px; overflow-y: scroll; background: #fafafa; margin-top: 15px; }
        .msg { margin-bottom: 10px; padding: 8px 12px; border-radius: 6px; width: fit-content; max-width: 80%; }
        .msg-user { background: #3182ce; color: white; margin-left: auto; }
        .msg-other { background: #e2e8f0; color: #2d3748; }
        .msg-system { background: #feebc8; color: #744210; font-style: italic; font-size: 0.85em; margin: 5px auto; text-align: center; }
        .controls { display: flex; gap: 10px; margin-top: 15px; }
        input, select { padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
        input[type="text"] { flex: 1; }
        .btn { background: #27ae60; color: white; border: none; padding: 10px 18px; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <h2>💬 Real-Time Multi-Room Chat Engine (Day 18)</h2>
        <p>Online Users: <strong id="online_count">0</strong> | Active Channel: <strong id="active_room">None</strong></p>

        <div class="controls">
            <input type="text" id="username" value="DevAlice" placeholder="Username">
            <select id="room_select">
                <option value="#general">#general</option>
                <option value="#python">#python</option>
                <option value="#flask">#flask</option>
            </select>
            <button class="btn" onclick="joinRoom()">Join Room Channel</button>
        </div>

        <div class="chat-box" id="chat_box"></div>

        <div class="controls">
            <input type="text" id="message_input" placeholder="Type message..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button class="btn" onclick="sendMessage()">Send Message</button>
        </div>
    </div>

    <script>
        const socket = io();
        let currentUsername = "";
        let currentRoom = "";

        socket.on('connect', () => {
            console.log("Connected to Socket.IO server!");
        });

        socket.on('system_status', (data) => {
            document.getElementById('online_count').innerText = data.online_count;
        });

        socket.on('chat_message', (data) => {
            const chatBox = document.getElementById('chat_box');
            const msgDiv = document.createElement('div');

            if (data.type === 'system') {
                msgDiv.className = 'msg msg-system';
                msgDiv.innerText = data.text;
            } else {
                const isSelf = data.username === currentUsername;
                msgDiv.className = 'msg ' + (isSelf ? 'msg-user' : 'msg-other');
                msgDiv.innerText = data.username + ": " + data.text;
            }

            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        });

        function joinRoom() {
            currentUsername = document.getElementById('username').value.trim() || 'Anonymous';
            currentRoom = document.getElementById('room_select').value;
            document.getElementById('active_room').innerText = currentRoom;
            
            socket.emit('join_room', {
                username: currentUsername,
                room: currentRoom
            });
        }

        function sendMessage() {
            const input = document.getElementById('message_input');
            const text = input.value.trim();
            if (text && currentRoom) {
                socket.emit('send_message', { text: text });
                input.value = '';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(CHAT_HTML)


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 18 Real-Time Socket.IO Chat Application...")
    print("Chat Web UI at http://127.0.0.1:5000/")
    print("=" * 70)
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
