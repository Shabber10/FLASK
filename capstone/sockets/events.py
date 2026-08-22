from flask import request
from flask_socketio import emit, join_room, leave_room
from capstone.extensions import socketio

connected_clients = set()


@socketio.on("connect")
def handle_connect():
    """Handle new WebSocket client connection."""
    client_id = request.sid
    connected_clients.add(client_id)
    emit("connection_status", {"status": "connected", "sid": client_id})


@socketio.on("disconnect")
def handle_disconnect():
    """Handle WebSocket client disconnection."""
    client_id = request.sid
    if client_id in connected_clients:
        connected_clients.remove(client_id)


@socketio.on("join_room")
def handle_join_room(data):
    """Allow clients to subscribe to specific room channels."""
    room = data.get("room")
    if room:
        join_room(room)
        emit("room_notification", {"message": f"Subscribed to room: {room}"}, room=room)


@socketio.on("leave_room")
def handle_leave_room(data):
    """Allow clients to unsubscribe from room channels."""
    room = data.get("room")
    if room:
        leave_room(room)
        emit("room_notification", {"message": f"Left room: {room}"}, to=request.sid)


@socketio.on("ping_server")
def handle_ping(data):
    """Handle ping and return pong."""
    emit("pong_server", {"message": "pong", "payload": data})


def broadcast_task_update(task_id: str, status: str, progress: int = 100, result: str = None):
    """Broadcast an async task update to all connected clients in the task room."""
    socketio.emit(
        "task_update",
        {
            "task_id": task_id,
            "status": status,
            "progress": progress,
            "result": result
        },
        room=f"task_{task_id}"
    )
