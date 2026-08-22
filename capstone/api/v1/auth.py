from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, get_jwt, create_access_token
)
from capstone.services.auth_service import AuthService
from capstone.models.user import User
from capstone.extensions import db, limiter

auth_bp = Blueprint("auth_v1", __name__)


@auth_bp.route("/register", methods=["POST"])
@limiter.limit("10 per minute")
def register():
    """Register a new user account."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Bad Request", "message": "JSON body is required"}), 400

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({"error": "Validation Error", "message": "Username, email, and password are required"}), 422

    if len(password) < 8:
        return jsonify({"error": "Validation Error", "message": "Password must be at least 8 characters"}), 422

    user, err = AuthService.register_user(username, email, password)
    if err:
        return jsonify({"error": "Conflict", "message": err}), 409

    return jsonify({
        "message": "User registered successfully",
        "user": user.to_dict()
    }), 201


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    """Authenticate and receive access and refresh JWT tokens."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Bad Request", "message": "JSON body is required"}), 400

    username_or_email = data.get("username_or_email") or data.get("username") or data.get("email")
    password = data.get("password")

    if not username_or_email or not password:
        return jsonify({"error": "Validation Error", "message": "Username/Email and password required"}), 422

    auth_payload, err = AuthService.authenticate(
        username_or_email=username_or_email,
        password=password,
        ip_address=request.remote_addr
    )
    if err:
        return jsonify({"error": "Unauthorized", "message": err}), 401

    return jsonify(auth_payload), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Generate a new access token using a valid refresh token."""
    identity = get_jwt_identity()
    claims = get_jwt()
    
    additional_claims = {
        "is_admin": claims.get("is_admin", False),
        "roles": claims.get("roles", [])
    }
    
    new_access_token = create_access_token(
        identity=identity, 
        additional_claims=additional_claims
    )
    return jsonify({"access_token": new_access_token}), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """Logout current session by revoking the access token."""
    raw_jwt = get_jwt()
    AuthService.revoke_token(raw_jwt)
    return jsonify({"message": "Successfully logged out. Token revoked."}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """Retrieve the currently authenticated user's profile."""
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "Not Found", "message": "User profile not found"}), 404

    return jsonify({"user": user.to_dict()}), 200
