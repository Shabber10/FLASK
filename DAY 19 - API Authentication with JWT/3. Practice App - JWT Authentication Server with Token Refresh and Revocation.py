"""
===============================================================================
Day 19 Practice Script: Production JWT Auth Server with Redis Revocation & Rotation
===============================================================================
This script provides an enterprise-ready JWT authentication service.

What this script demonstrates step-by-step:
1. STEP 1: Configuring Flask-JWT-Extended with environment-driven secrets and lifespans.
2. STEP 2: Connecting to Redis for distributed JTI blocklisting (with graceful local fallback).
3. STEP 3: String identity serialization and @jwt.user_lookup_loader.
4. STEP 4: Login with brute-force rate-limiting (Flask-Limiter).
5. STEP 5: Refresh Token Rotation (revoking old refresh JTI and minting new pair).
6. STEP 6: Revoking Access / Refresh tokens on logout with Redis TTL expiration.
7. STEP 7: Short-lived token testing endpoint to demonstrate token expiration behavior.
8. STEP 8: Interactive JWT Tester Web Dashboard rendering templates/index.html.

How to run this script:
1. Open your terminal in this directory.
2. Run: python "3. Practice App - JWT Authentication Server with Token Refresh and Revocation.py"
3. Open your browser and navigate to: http://127.0.0.1:5000/
"""

import os
from datetime import datetime, timezone, timedelta
from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt, current_user
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# =============================================================================
# STEP 1: JWT & Application Configuration (Day 12 Environment Pattern)
# =============================================================================
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'day19-jwt-masterclass-secret')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-signing-secret-key-32bytes')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)
app.config['JWT_DECODE_LEEWAY'] = timedelta(seconds=10)

jwt = JWTManager(app)

# Rate Limiter (Day 20 Pattern)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)
limiter.init_app(app)


# =============================================================================
# STEP 2: Redis Blocklist Connection with Graceful In-Memory Fallback
# =============================================================================
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
redis_client = None
in_memory_blocklist = set()

try:
    import redis
    client = redis.Redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=1)
    client.ping()
    redis_client = client
    print(f"✓ Connected to Redis at {REDIS_URL} for distributed token revocation.")
except Exception as e:
    print(f"ℹ Redis not reachable ({e}). Using local in-memory blocklist fallback.")


def store_revoked_token(jti: str, exp_timestamp: float) -> None:
    """Store revoked JTI with TTL matching token lifespan."""
    now_timestamp = datetime.now(timezone.utc).timestamp()
    ttl_seconds = max(int(exp_timestamp - now_timestamp), 1)

    if redis_client:
        redis_client.setex(f"jwt:revoked:{jti}", ttl_seconds, "true")
    else:
        in_memory_blocklist.add(jti)


def is_token_revoked(jti: str) -> bool:
    """Check if JTI exists in Redis or local fallback blocklist."""
    if redis_client:
        return redis_client.get(f"jwt:revoked:{jti}") is not None
    return jti in in_memory_blocklist


# =============================================================================
# STEP 3: User Database & Identity Serialization Callbacks
# =============================================================================
users_db = {
    101: {"id": 101, "username": "alice_dev", "password": generate_password_hash("DevPass123!"), "role": "Developer"},
    102: {"id": 102, "username": "admin_boss", "password": generate_password_hash("AdminPass123!"), "role": "Admin"}
}

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """Automatically populates flask_jwt_extended.current_user."""
    user_id = int(jwt_data["sub"])
    return users_db.get(user_id)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(_jwt_header, jwt_payload: dict) -> bool:
    """Callback executing on every request to verify if JTI is revoked in Redis."""
    jti = jwt_payload['jti']
    return is_token_revoked(jti)


# Standard Error Responses
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "error": {"code": 401, "type": "TOKEN_EXPIRED", "message": "The access token has expired. Refresh your session."}
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "error": {"code": 401, "type": "TOKEN_REVOKED", "message": "Token has been revoked. Please log in again."}
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "error": {"code": 401, "type": "INVALID_TOKEN", "message": f"Signature verification failed: {error}"}
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "error": {"code": 401, "type": "AUTHORIZATION_HEADER_MISSING", "message": "Request missing 'Authorization: Bearer <token>' header."}
    }), 401


# =============================================================================
# STEP 4: Authentication Endpoints
# =============================================================================

@app.route('/api/v1/auth/login', methods=['POST'])
@limiter.limit("5 per minute")  # Protect against brute force attacks
def login():
    """Validates credentials and returns Access + Refresh Token Pair."""
    data = request.get_json(silent=True) or {}
    username = data.get('username')
    password = data.get('password')

    user = next((u for u in users_db.values() if u["username"] == username), None)
    if user and check_password_hash(user['password'], password):
        # Explicit string identity typing
        user_id_str = str(user['id'])
        
        access_token = create_access_token(
            identity=user_id_str,
            additional_claims={"role": user['role']}
        )
        refresh_token = create_refresh_token(identity=user_id_str)
        
        return jsonify({
            "status": "success",
            "message": "Authentication successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in_seconds": 900
        }), 200

    return jsonify({"error": "Invalid username or password"}), 401


@app.route('/api/v1/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_access_token():
    """
    Step 5: Refresh Token Rotation:
    Revokes the current refresh token and issues a brand new token pair.
    """
    jwt_data = get_jwt()
    old_refresh_jti = jwt_data['jti']
    user_identity = get_jwt_identity()
    user = users_db.get(int(user_identity))

    # Revoke old refresh token JTI in Redis
    store_revoked_token(old_refresh_jti, jwt_data['exp'])

    # Mint fresh token pair
    new_access_token = create_access_token(
        identity=user_identity,
        additional_claims={"role": user['role'] if user else "User"}
    )
    new_refresh_token = create_refresh_token(identity=user_identity)

    return jsonify({
        "status": "success",
        "message": "Refresh token rotated successfully",
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "Bearer"
    }), 200


@app.route('/api/v1/auth/logout', methods=['POST'])
@jwt_required(verify_type=False)
def logout():
    """Revokes active token (Access or Refresh) by adding its JTI to Redis."""
    jwt_data = get_jwt()
    jti = jwt_data['jti']
    token_type = jwt_data['type']
    
    store_revoked_token(jti, jwt_data['exp'])
    
    return jsonify({
        "status": "success",
        "message": f"{token_type.capitalize()} token JTI '{jti}' successfully revoked."
    }), 200


@app.route('/api/v1/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Returns protected user profile info from Bearer token claims."""
    claims = get_jwt()
    return jsonify({
        "status": "success",
        "data": {
            "user_id": current_user['id'],
            "username": current_user['username'],
            "role": claims.get('role'),
            "jti": claims.get('jti')
        }
    }), 200


@app.route('/api/v1/auth/test-short-expiry', methods=['POST'])
def test_short_token():
    """Helper route: generates an access token with a 5-second lifetime to test 401 expiration."""
    short_token = create_access_token(
        identity="101",
        expires_delta=timedelta(seconds=5),
        additional_claims={"role": "Tester"}
    )
    return jsonify({
        "message": "Token expires in 5 seconds. Use with /api/v1/profile immediately, then re-try in 6 seconds to see 401 TOKEN_EXPIRED.",
        "short_access_token": short_token
    }), 200


# =============================================================================
# STEP 8: Interactive Web UI Dashboard
# =============================================================================
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
