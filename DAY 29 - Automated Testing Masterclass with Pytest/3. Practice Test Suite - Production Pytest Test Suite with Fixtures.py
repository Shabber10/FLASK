# Day 29 Practice Test Suite: Pytest Automation Example
import pytest
from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)
    @app.route('/api/ping')
    def ping():
        return jsonify({"pong": True}), 200
    return app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()

def test_ping_endpoint(client):
    res = client.get('/api/ping')
    assert res.status_code == 200
    assert res.json == {"pong": True}
