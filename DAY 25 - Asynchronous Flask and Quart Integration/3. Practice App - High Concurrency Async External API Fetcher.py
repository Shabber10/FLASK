# Day 25 Practice App: Async Route Handler in Flask
import asyncio
from flask import Flask, jsonify

app = Flask(__name__)

async def fetch_remote_service(service_id):
    await asyncio.sleep(0.5)
    return {"service_id": service_id, "status": "UP"}

@app.route('/services')
async def get_services():
    results = await asyncio.gather(
        fetch_remote_service(1),
        fetch_remote_service(2),
        fetch_remote_service(3)
    )
    return jsonify({"services": results})

if __name__ == '__main__':
    app.run(debug=True)
