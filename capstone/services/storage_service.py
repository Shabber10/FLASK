import os
import uuid
import mimetypes
from typing import Tuple, Optional
from werkzeug.utils import secure_filename
from flask import current_app

class StorageService:
    """Storage service handling media file validation, saving, and retrieval."""

    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "csv", "json", "txt"}
    FORBIDDEN_EXTENSIONS = {"exe", "sh", "bat", "py", "php", "pl", "js", "html"}

    @classmethod
    def is_allowed_file(cls, filename: str, content_type: Optional[str] = None) -> bool:
        """Validate filename extension."""
        if not filename or "." not in filename:
            return False
        
        ext = filename.rsplit(".", 1)[1].lower()
        if ext in cls.FORBIDDEN_EXTENSIONS:
            return False
            
        return ext in cls.ALLOWED_EXTENSIONS

    @classmethod
    def save_file(cls, file_obj) -> Tuple[Optional[dict], Optional[str]]:
        """Safely store an uploaded file to storage."""
        if not file_obj or not file_obj.filename:
            return None, "No file provided"

        raw_filename = secure_filename(file_obj.filename)
        if not cls.is_allowed_file(raw_filename, file_obj.content_type):
            return None, "File type or extension not permitted"

        ext = raw_filename.rsplit(".", 1)[1].lower()
        unique_name = f"{uuid.uuid4().hex}.{ext}"
        
        upload_folder = current_app.config.get("UPLOAD_FOLDER")
        os.makedirs(upload_folder, exist_ok=True)
        
        dest_path = os.path.join(upload_folder, unique_name)
        file_obj.save(dest_path)
        file_size = os.path.getsize(dest_path)

        return {
            "original_name": raw_filename,
            "filename": unique_name,
            "size_bytes": file_size,
            "extension": ext,
            "url": f"/api/v1/media/{unique_name}"
        }, None
