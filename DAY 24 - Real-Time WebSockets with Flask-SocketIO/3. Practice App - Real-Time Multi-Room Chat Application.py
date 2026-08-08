# Day 24 Practice App: WebSocket Server Setup
from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'socketio-secret-day-24'

socketio = SocketIO(app, cors_allowed_origins="*")

HTML_LAYOUT = '''
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
    <script>
        const socket = io();
        socket.on('connect', () => { console.log("Connected to WebSocket Server!"); });
        socket.on('chat_msg', (data) => {
            document.getElementById('messages').innerHTML += '<p>' + data.msg + '</p>';
        });
        function sendMsg() {
            const input = document.getElementById('msg_input');
            socket.emit('send_msg', {msg: input.value});
            input.value = '';
        }
    </script>
</head>
<body>
    <h2>WebSocket Chat Demo</h2>
    <div id="messages"></div>
    <input id="msg_input" type="text">
    <button onclick="sendMsg()">Send</button>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_LAYOUT)

@socketio.on('send_msg')
def handle_chat(data):
    emit('chat_msg', {'msg': data['msg']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
