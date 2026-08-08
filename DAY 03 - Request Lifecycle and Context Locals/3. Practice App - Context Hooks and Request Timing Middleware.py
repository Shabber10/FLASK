# Day 03 Practice App: Request Timing & Global Contexts
import time
from flask import Flask, g, request, jsonify

app = Flask(__name__)

@app.before_request
def start_timer():
    g.start_time = time.time()
    g.user_ip = request.remote_addr

@app.after_request
def log_duration(response):
    if hasattr(g, 'start_time'):
        duration = round((time.time() - g.start_time) * 1000, 2)
        response.headers['X-Response-Time-MS'] = str(duration)
    return response

@app.route('/data')
def get_data():
    return jsonify({"message": "Data loaded", "ip": g.user_ip})

if __name__ == '__main__':
    app.run(debug=True)
