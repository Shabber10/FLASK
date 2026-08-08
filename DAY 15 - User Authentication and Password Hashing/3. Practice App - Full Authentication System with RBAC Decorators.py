# Day 15 Practice App: Authentication & RBAC System
from flask import Flask, jsonify, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'auth-system-key-15'

users_db = {
    "admin": {"password": generate_password_hash("admin123"), "role": "Admin"},
    "john": {"password": generate_password_hash("user123"), "role": "User"}
}

def require_role(role_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_header = request.headers.get('X-User')
            user_info = users_db.get(user_header)
            if not user_info or user_info['role'] != role_name:
                return jsonify({"error": "Forbidden - Insufficient Role Permissions"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    user = users_db.get(data.get('username'))
    if user and check_password_hash(user['password'], data.get('password', '')):
        return jsonify({"message": "Authentication successful!", "role": user['role']})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/admin/settings')
@require_role('Admin')
def admin_settings():
    return jsonify({"settings": "Protected Admin System Configuration"})

if __name__ == '__main__':
    app.run(debug=True)
