# Day 23 Practice App: Cached Endpoint with Invalidation
from flask import Flask, jsonify
from flask_caching import Cache
import time

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 60

cache = Cache(app)

@app.route('/slow-data')
@cache.cached(timeout=10)
def get_slow_data():
    time.sleep(2) # Simulate slow query
    return jsonify({"timestamp": time.time(), "data": "Freshly fetched slow response"})

@app.route('/clear-cache')
def clear():
    cache.clear()
    return jsonify({"message": "Cache invalidated!"})

if __name__ == '__main__':
    app.run(debug=True)
