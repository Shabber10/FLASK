import pytest


@pytest.mark.sockets
def test_socketio_connection(socket_client):
    """Test WebSocket client connection."""
    assert socket_client.is_connected()
    received = socket_client.get_received()
    assert len(received) > 0
    assert received[0]["name"] == "connection_status"
    assert received[0]["args"][0]["status"] == "connected"


@pytest.mark.sockets
def test_socketio_ping_pong(socket_client):
    """Test ping-pong WebSocket exchange."""
    socket_client.emit("ping_server", {"client_time": "12:00:00"})
    received = socket_client.get_received()
    pong = next((item for item in received if item["name"] == "pong_server"), None)
    assert pong is not None
    assert pong["args"][0]["message"] == "pong"


@pytest.mark.sockets
def test_socketio_join_room(socket_client):
    """Test subscribing to a WebSocket room channel."""
    socket_client.emit("join_room", {"room": "analytics_feed"})
    received = socket_client.get_received()
    notification = next((item for item in received if item["name"] == "room_notification"), None)
    assert notification is not None
    assert "analytics_feed" in notification["args"][0]["message"]
