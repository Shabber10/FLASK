# Day 14 Practice App: Cookie Security & Session Management
from flask import Flask, session, jsonify, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secure-signing-key-day-14'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

@app.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    session['user_id'] = data.get('user_id', 101)
    session['username'] = data.get('username', 'test_user')
    return jsonify({"message": "Session created successfully"})

@app.route('/me')
def me():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"user_id": session['user_id'], "username": session['username']})

@app.route('/logout')
def logout():
    session.clear()
    return jsonify({"message": "Logged out and session cleared"})

if __name__ == '__main__':
    app.run(debug=True)
