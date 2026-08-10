"""
Day 15 Practice Application: Stateless JWT Authentication & Refresh Engine
===========================================================================
This application demonstrates:
1. Setting up Flask-JWT-Extended with Access & Refresh token lifecycles.
2. Generating Access Tokens (with custom claims) and Refresh Tokens.
3. Protecting API endpoints with @jwt_required() and @jwt_required(refresh=True).
4. Implementing token revocation / logout blocklisting via token_in_blocklist_loader.
5. Providing an interactive Web UI for testing login, token refresh, and revocation.
"""

from datetime import timedelta
from flask import Flask, jsonify, request, render_template_string
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'day15-jwt-stateless-masterclass-secret'
app.config['JWT_SECRET_KEY'] = 'jwt-crypto-signing-secret-key-30-days'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

jwt = JWTManager(app)

# In-Memory Blocklist for Revoked Token JTIs
revoked_jti_blocklist = set()

# Simulated User Database
USERS = {
    "dev_alice": {"password": "Password123!", "role": "admin"},
    "dev_bob": {"password": "Password123!", "role": "member"}
}


# ------------------------------------------------------------------------------
# 1. JWT Blocklist Loader & Error Handler Callbacks
# ------------------------------------------------------------------------------
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in revoked_jti_blocklist

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Unauthorized", "message": "Token has been revoked/logged out."}), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Unauthorized", "message": "Token has expired. Use /api/refresh to renew."}), 401

@jwt.unauthorized_loader
def missing_token_callback(error_string):
    return jsonify({"error": "Unauthorized", "message": "Request missing Authorization: Bearer <token> header."}), 401


# ------------------------------------------------------------------------------
# 2. HTML Web Tester UI
# ------------------------------------------------------------------------------
TESTER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Day 15 Stateless JWT Masterclass</title>
    <style>
        body { font-family: Arial, sans-serif; background: #eef2f5; margin: 30px; }
        .card { max-width: 850px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .token-box { background: #1a202c; color: #48bb78; padding: 12px; border-radius: 6px; font-family: monospace; font-size: 0.85em; word-break: break-all; margin-top: 10px; }
        .btn { background: #2b6cb0; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; }
        .btn-logout { background: #c53030; }
        .form-group { margin-bottom: 15px; }
        input { padding: 8px; width: 200px; border: 1px solid #ccc; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🔑 Stateless JWT Authentication Engine (Day 15)</h2>
        <p>Demonstrating Dual-Token Lifecycles (Access & Refresh Tokens) and Token Revocation Blocklisting.</p>

        <h3>1. Acquire Tokens (/api/login)</h3>
        <div class="form-group">
            <input type="text" id="username" value="dev_alice" placeholder="Username">
            <input type="password" id="password" value="Password123!" placeholder="Password">
            <button class="btn" onclick="login()">Log In & Get Tokens</button>
        </div>

        <div><strong>Access Token:</strong><div id="access_token_display" class="token-box">Not Authenticated</div></div>
        <div style="margin-top:10px;"><strong>Refresh Token:</strong><div id="refresh_token_display" class="token-box">Not Authenticated</div></div>

        <h3 style="margin-top:25px;">2. Test Protected Endpoints</h3>
        <button class="btn" onclick="testProtected()">Call /api/protected (Access Token)</button>
        <button class="btn" onclick="refreshTokens()">Call /api/refresh (Refresh Token)</button>
        <button class="btn btn-logout" onclick="logout()">Call /api/logout (Revoke JTI)</button>

        <div style="margin-top:15px;"><strong>API Response Output:</strong><div id="api_response" class="token-box">No Requests Sent</div></div>
    </div>

    <script>
        let currentAccessToken = "";
        let currentRefreshToken = "";

        async function login() {
            const u = document.getElementById('username').value;
            const p = document.getElementById('password').value;
            const res = await fetch('/api/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: u, password: p})
            });
            const data = await res.json();
            if (res.ok) {
                currentAccessToken = data.access_token;
                currentRefreshToken = data.refresh_token;
                document.getElementById('access_token_display').innerText = currentAccessToken;
                document.getElementById('refresh_token_display').innerText = currentRefreshToken;
            }
            document.getElementById('api_response').innerText = JSON.stringify(data, null, 2);
        }

        async function testProtected() {
            const res = await fetch('/api/protected', {
                headers: {'Authorization': 'Bearer ' + currentAccessToken}
            });
            const data = await res.json();
            document.getElementById('api_response').innerText = JSON.stringify(data, null, 2);
        }

        async function refreshTokens() {
            const res = await fetch('/api/refresh', {
                method: 'POST',
                headers: {'Authorization': 'Bearer ' + currentRefreshToken}
            });
            const data = await res.json();
            if (res.ok) {
                currentAccessToken = data.access_token;
                document.getElementById('access_token_display').innerText = currentAccessToken;
            }
            document.getElementById('api_response').innerText = JSON.stringify(data, null, 2);
        }

        async function logout() {
            const res = await fetch('/api/logout', {
                method: 'POST',
                headers: {'Authorization': 'Bearer ' + currentAccessToken}
            });
            const data = await res.json();
            document.getElementById('api_response').innerText = JSON.stringify(data, null, 2);
        }
    </script>
</body>
</html>
"""


# ------------------------------------------------------------------------------
# 3. Route Handlers
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template_string(TESTER_HTML)

@app.route('/api/login', methods=['POST'])
def login_api():
    payload = request.get_json(silent=True) or {}
    username = payload.get('username')
    password = payload.get('password')

    user_info = USERS.get(username)
    if not user_info or user_info['password'] != password:
        return jsonify({"error": "Unauthorized", "message": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username, additional_claims={"role": user_info['role']})
    refresh_token = create_refresh_token(identity=username)

    return jsonify({
        "status": "Login Successful",
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200

@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected_api():
    identity = get_jwt_identity()
    claims = get_jwt()
    return jsonify({
        "status": "Access Granted",
        "user_identity": identity,
        "role_claim": claims.get('role'),
        "token_jti": claims.get('jti')
    }), 200

@app.route('/api/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_api():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify({
        "status": "Access Token Renewed",
        "access_token": new_access_token
    }), 200

@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout_api():
    jti = get_jwt()['jti']
    revoked_jti_blocklist.add(jti)
    return jsonify({"status": "Logged Out", "message": f"Token JTI '{jti}' added to revocation blocklist."}), 200


if __name__ == '__main__':
    print("=" * 70)
    print("Starting Day 15 JWT Stateless Authentication Application...")
    print("Dashboard UI at http://127.0.0.1:5000/")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
