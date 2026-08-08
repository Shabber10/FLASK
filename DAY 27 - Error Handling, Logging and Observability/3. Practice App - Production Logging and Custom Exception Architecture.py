# Day 27 Practice App: Structured Error Handling & Logging
import logging
from flask import Flask, jsonify, request

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

class APIException(Exception):
    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        self.status_code = status_code

@app.errorhandler(APIException)
def handle_api_exception(error):
    app.logger.warning(f"APIException [{error.status_code}]: {error.message}")
    return jsonify({"error": error.message}), error.status_code

@app.route('/divide')
def divide():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if b == 0:
        raise APIException("Cannot divide by zero", 422)
    return jsonify({"result": a / b if (a and b) else 0})

if __name__ == '__main__':
    app.run(debug=True)
