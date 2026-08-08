# Day 28 Practice App: Response Compression & Query Profiler
from flask import Flask, jsonify
from flask_compress import Compress
import time

app = Flask(__name__)
Compress(app)

@app.route('/large-data')
def get_large_payload():
    large_list = [{"id": i, "name": f"Item_{i}", "details": "Performance tuning test"} for i in range(10000)]
    return jsonify(large_list)

if __name__ == '__main__':
    app.run(debug=True)
