# Day 11 Practice App: Multi-Blueprint Application Architecture
from flask import Flask, Blueprint, jsonify

api_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@api_bp.route('/users')
def get_api_users():
    return jsonify([{"id": 1, "username": "api_user"}])

@admin_bp.route('/dashboard')
def admin_dashboard():
    return jsonify({"status": "Admin Dashboard Active"})

app = Flask(__name__)
app.register_blueprint(api_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(debug=True)
