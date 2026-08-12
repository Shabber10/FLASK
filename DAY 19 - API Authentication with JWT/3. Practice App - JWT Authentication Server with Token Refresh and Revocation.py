"""
===============================================================================
Day 19 Practice Script: Complete JWT Auth Server with Refresh & Blacklisting
===============================================================================
This script starts from pure zero basics for beginner Flask developers.

What this script demonstrates step-by-step:
1. STEP 1: Configuring `Flask-JWT-Extended` with Access & Refresh Token Lifespans.
2. STEP 2: Defining JWT Callbacks & Error Handlers (`@jwt.token_in_blocklist_loader`).
3. STEP 3: Initializing in-memory database with salted password hashes (`generate_password_hash`).
4. STEP 4: Auth Endpoints (`login` token pair, `refresh` access token, `logout` JTI blocklisting).
5. STEP 5: Protected API Profile endpoint (`GET /api/v1/profile`) with `@jwt_required()`.
6. STEP 6: Interactive JWT Token Tester Portal UI rendering `templates/index.html`.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - JWT Authentication Server with Token Refresh and Revocation.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

from datetime import timedelta
from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# =============================================================================
# STEP 1: JWT Configuration Settings
# =============================================================================
app.config['SECRET_KEY'] = 'day19-jwt-masterclass-secret'
app.config['JWT_SECRET_KEY'] = 'jwt-signing-secret-key-32bytes'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

jwt = JWTManager(app)


# =============================================================================
# STEP 3: In-Memory Database & JTI Token Revocation Blocklist Set
# =============================================================================
users_db = {
    "alice_dev": {"id": 101, "password": generate_password_hash("DevPass123!"), "role": "Developer"},
    "admin_boss": {"id": 102, "password": generate_password_hash("AdminPass123!"), "role": "Admin"}
}
jwt_blocklist = set()


# =============================================================================
# STEP 2: JWT Callbacks & Error Handlers
# =============================================================================
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """Step 2a: Callback executing on every request to verify if JTI is blacklisted."""
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
# STEP 4: REST API Authentication Endpoints (Login, Refresh, Logout)
# =============================================================================

# POST /api/v1/auth/login -> Issues Access + Refresh Token Pair
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """Step 4a: Validates credentials and returns Access + Refresh Token Pair."""
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
    """Step 4b: Generates a new 15-minute Access Token using Refresh Token."""
    current_user_id = get_jwt_identity()
    
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
    """Step 4c: Adds active token JTI UUID to revocation blocklist set."""
    jti = get_jwt()['jti']
    jwt_blocklist.add(jti)  # Blacklist JTI
    return jsonify({
        "status": "success",
        "message": f"Token JTI '{jti}' successfully revoked. Logged out."
    }), 200


# =============================================================================
# STEP 5: Protected API Resource Endpoint
# =============================================================================
@app.route('/api/v1/profile', methods=['GET'])
@jwt_required()  # Requires valid non-revoked Access Token!
def get_profile():
    """Step 5: Returns protected user profile info from Bearer token claims."""
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
# STEP 6: Interactive Web UI Tester Dashboard Route Handler (render_template)
# =============================================================================
@app.route('/')
def home():
    """Step 6: Renders templates/index.html dashboard."""
    return render_template('index.html')


# =============================================================================
# Main Entrypoint
# =============================================================================
if __name__ == '__main__':
    print("=" * 75)
    print("🚀 Starting Day 19 JWT Authentication Server Application...")
    print("🌐 Dashboard UI at: http://127.0.0.1:5000/")
    print("🔑 Login Endpoint at: http://127.0.0.1:5000/api/v1/auth/login")
    print("👤 Protected Profile at: http://127.0.0.1:5000/api/v1/profile")
    print("=" * 75)
    app.run(host='127.0.0.1', port=5000, debug=True)
