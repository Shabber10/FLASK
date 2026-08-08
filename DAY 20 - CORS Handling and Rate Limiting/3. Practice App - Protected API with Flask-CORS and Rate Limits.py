# Day 20 Practice App: CORS & Rate Limiting Protection
from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["100 per day", "10 per minute"]
)

@app.route('/api/public')
def public_endpoint():
    return jsonify({"message": "Public access endpoint"})

@app.route('/api/strict')
@limiter.limit("3 per minute")
def strict_endpoint():
    return jsonify({"message": "Strict rate-limited endpoint (max 3 req/min)"})

if __name__ == '__main__':
    app.run(debug=True)
