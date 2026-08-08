# Day 01 Practice Script: Minimal Flask App
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Welcome to Day 01 of Flask Masterclass!</h1>"

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Flask Masterclass Day 01",
        "version": "3.0.0"
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
