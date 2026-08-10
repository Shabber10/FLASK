"""
===============================================================================
Day 19 Practice Script: Complete JWT Auth Server with Refresh & Blacklisting
===============================================================================
This script demonstrates:
1. Configuring `Flask-JWT-Extended` with Access & Refresh Token Lifespans.
2. Issuing token pairs upon user login (`POST /api/v1/auth/login`).
3. Protecting API endpoints (`GET /api/v1/profile`) with `@jwt_required()`.
4. Refreshing access tokens (`POST /api/v1/auth/refresh`) with `@jwt_required(refresh=True)`.
5. Revoking tokens on logout via `jti` tracking (`@jwt.token_in_blocklist_loader`).
6. Interactive JWT Token Tester Portal UI and REST API.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - JWT Authentication Server with Token Refresh and Revocation.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from datetime import timedelta
from flask import Flask, jsonify, request, render_template_string
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# =============================================================================
# 1. JWT Configuration Settings
# =============================================================================
app.config['SECRET_KEY'] = 'day19-jwt-masterclass-secret'
app.config['JWT_SECRET_KEY'] = 'jwt-signing-secret-key-32bytes'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

jwt = JWTManager(app)

# In-Memory Database & JTI Token Revocation Blocklist Set
users_db = {
    "alice_dev": {"id": 101, "password": generate_password_hash("DevPass123!"), "role": "Developer"},
    "admin_boss": {"id": 102, "password": generate_password_hash("AdminPass123!"), "role": "Admin"}
}
jwt_blocklist = set()


# =============================================================================
# 2. JWT Callbacks & Error Handlers
# =============================================================================
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """Callback executing on every request to verify if JTI is blacklisted."""
    jti = jwt_payload['jti']
    return jti in jwt_blocklist

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "error": {"code": 401, "type": "TOKEN_EXPIRED", "message": "The access token has expired."}
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "error": {"code": 401, "type": "INVALID_TOKEN", "message": "Signature verification failed."}
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "error": {"code": 401, "type": "AUTHORIZATION_HEADER_MISSING", "message": "Request missing 'Authorization: Bearer <token>' header."}
    }), 401


# =============================================================================
# 3. REST API Authentication Endpoints
# =============================================================================

# POST /api/v1/auth/login -> Issues Access + Refresh Token Pair
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    user = users_db.get(username)
    if user and check_password_hash(user['password'], password):
        # Create token pair embedding user.id as identity
        access_token = create_access_token(identity=user['id'], additional_claims={"role": user['role']})
        refresh_token = create_refresh_token(identity=user['id'])
        
        return jsonify({
            "status": "success",
            "message": "Authentication successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in_seconds": 900
        }), 200

    return jsonify({"error": "Invalid username or password"}), 401


# POST /api/v1/auth/refresh -> Generates new Access Token using Refresh Token
@app.route('/api/v1/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Requires valid Refresh Token in Authorization header!
def refresh_access_token():
    current_user_id = get_jwt_identity()
    
    # Generate new Access Token
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({
        "status": "success",
        "access_token": new_access_token,
        "token_type": "Bearer"
    }), 200


# POST /api/v1/auth/logout -> Blacklists current token's JTI ID
@app.route('/api/v1/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    jwt_blocklist.add(jti)  # Blacklist JTI
    return jsonify({
        "status": "success",
        "message": f"Token JTI '{jti}' successfully revoked. Logged out."
    }), 200


# GET /api/v1/profile -> Protected API resource endpoint
@app.route('/api/v1/profile', methods=['GET'])
@jwt_required()  # Requires valid non-revoked Access Token!
def get_profile():
    user_id = get_jwt_identity()
    claims = get_jwt()
    
    return jsonify({
        "status": "success",
        "data": {
            "user_id": user_id,
            "role": claims.get('role'),
            "jti": claims.get('jti'),
            "token_type": claims.get('type')
        }
    }), 200


# =============================================================================
# 4. Interactive Web UI Tester Portal
# =============================================================================
@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Day 19 JWT Authentication Server</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #eef2f5; margin: 40px; color: #333; }
                .card { max-width: 750px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
                h2 { color: #2c3e50; margin-top: 0; }
                .badge { background: #e74c3c; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 10px; border-bottom: 1px solid #e9ecef; text-align: left; }
                th { background: #34495e; color: white; }
                code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; color: #c7254e; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>🔑 JWT Authentication & Token Revocation Server (Day 19)</h2>
                <p>Authentication Engine: <span class="badge">Flask-JWT-Extended</span></p>

                <h3>Pre-seeded Login Accounts:</h3>
                <ul>
                    <li>Username: <code>alice_dev</code> | Password: <code>DevPass123!</code></li>
                    <li>Username: <code>admin_boss</code> | Password: <code>AdminPass123!</code></li>
                </ul>

                <h3>Available Endpoints:</h3>
                <table>
                    <thead><tr><th>Verb</th><th>Endpoint</th><th>Description</th></tr></thead>
                    <tbody>
                        <tr><td><code>POST</code></td><td><code>/api/v1/auth/login</code></td><td>Issue Access & Refresh Token Pair</td></tr>
                        <tr><td><code>POST</code></td><td><code>/api/v1/auth/refresh</code></td><td>Generate new Access Token using Refresh Token</td></tr>
                        <tr><td><code>GET</code></td><td><code>/api/v1/profile</code></td><td>Protected Profile (Requires <code>Authorization: Bearer &lt;access_token&gt;</code>)</td></tr>
                        <tr><td><code>POST</code></td><td><code>/api/v1/auth/logout</code></td><td>Revoke Token JTI in Blocklist</td></tr>
                    </tbody>
                </table>
            </div>
        </body>
        </html>
    """)


# =============================================================================
# 5. Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 19 JWT Authentication Server Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("🔑 Login Endpoint at: http://127.0.0.1:5000/api/v1/auth/login")
    print("👤 Protected Profile at: http://127.0.0.1:5000/api/v1/profile")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
