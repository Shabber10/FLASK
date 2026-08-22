import os
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required
from capstone.services.storage_service import StorageService

media_bp = Blueprint("media_v1", __name__)


@media_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    """Upload and validate media or document file."""
    if "file" not in request.files:
        return jsonify({"error": "Bad Request", "message": "No 'file' field in multipart request"}), 400

    uploaded_file = request.files["file"]
    if not uploaded_file or not uploaded_file.filename:
        return jsonify({"error": "Bad Request", "message": "No file selected"}), 400

    file_meta, err = StorageService.save_file(uploaded_file)
    if err:
        return jsonify({"error": "Unprocessable Entity", "message": err}), 422

    return jsonify({
        "message": "File uploaded successfully",
        "file": file_meta
    }), 201


@media_bp.route("/<filename>", methods=["GET"])
def get_media(filename: str):
    """Serve uploaded media file."""
    upload_folder = current_app.config.get("UPLOAD_FOLDER")
    if not os.path.exists(os.path.join(upload_folder, filename)):
        return jsonify({"error": "Not Found", "message": "File does not exist"}), 404

    return send_from_directory(upload_folder, filename)
