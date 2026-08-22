from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from sqlalchemy import select
from capstone.extensions import db, cache
from capstone.models.user import User, Role

users_bp = Blueprint("users_v1", __name__)


def admin_required():
    """Helper to check if caller has admin privileges."""
    claims = get_jwt()
    return claims.get("is_admin", False)


@users_bp.route("", methods=["GET"])
@jwt_required()
@cache.cached(timeout=60, query_string=True)
def list_users():
    """Retrieve paginated list of users."""
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)

    stmt = select(User).order_by(User.id.asc()).offset((page - 1) * per_page).limit(per_page)
    users = db.session.execute(stmt).scalars().all()
    
    total_count = db.session.execute(select(db.func.count(User.id))).scalar_one()

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": total_count,
        "users": [u.to_dict() for u in users]
    }), 200


@users_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id: int):
    """Retrieve specific user details."""
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "Not Found", "message": "User not found"}), 404
    return jsonify({"user": user.to_dict()}), 200


@users_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id: int):
    """Update user information."""
    current_user_id = int(get_jwt_identity())
    claims = get_jwt()

    if current_user_id != user_id and not claims.get("is_admin", False):
        return jsonify({"error": "Forbidden", "message": "You do not have permission to update this user"}), 403

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "Not Found", "message": "User not found"}), 404

    data = request.get_json(silent=True) or {}
    if "email" in data:
        user.email = data["email"].strip()
    if "is_active" in data and claims.get("is_admin", False):
        user.is_active = bool(data["is_active"])

    db.session.commit()
    return jsonify({"message": "User updated successfully", "user": user.to_dict()}), 200


@users_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id: int):
    """Delete a user account (Admin only)."""
    claims = get_jwt()
    if not claims.get("is_admin", False):
        return jsonify({"error": "Forbidden", "message": "Administrator privileges required"}), 403

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "Not Found", "message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {user_id} deleted successfully"}), 200
