from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from capstone.services.task_service import TaskService
from capstone.tasks.celery_tasks import generate_pdf_report, send_async_email
from capstone.models.task import AsyncTaskRecord
from capstone.extensions import db
from sqlalchemy import select

tasks_bp = Blueprint("tasks_v1", __name__)


@tasks_bp.route("/report", methods=["POST"])
@jwt_required()
def trigger_report_task():
    """Trigger background PDF report generation."""
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    report_title = data.get("title", "Quarterly Financial Overview")

    # Dispatch Celery async job
    async_job = generate_pdf_report.delay(user_id=user_id, report_title=report_title)

    # Persist tracking record in DB
    record = TaskService.create_task_record(
        task_id=async_job.id,
        name="PDF_REPORT_GENERATION",
        user_id=user_id,
        meta_data={"title": report_title}
    )

    return jsonify({
        "message": "Async task dispatched",
        "task_id": async_job.id,
        "status": record.status,
        "poll_url": f"/api/v1/tasks/{async_job.id}"
    }), 202


@tasks_bp.route("/email", methods=["POST"])
@jwt_required()
def trigger_email_task():
    """Trigger background async email sending."""
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    recipient = data.get("recipient")
    subject = data.get("subject", "Notification")
    body = data.get("body", "Hello from Enterprise Flask!")

    if not recipient:
        return jsonify({"error": "Validation Error", "message": "Recipient email required"}), 422

    async_job = send_async_email.delay(recipient=recipient, subject=subject, body=body)

    TaskService.create_task_record(
        task_id=async_job.id,
        name="ASYNC_EMAIL",
        user_id=user_id,
        meta_data={"recipient": recipient, "subject": subject}
    )

    return jsonify({
        "message": "Email task queued",
        "task_id": async_job.id,
        "status": "QUEUED"
    }), 202


@tasks_bp.route("/<task_id>", methods=["GET"])
@jwt_required()
def get_task_status(task_id: str):
    """Poll the status and result of a background Celery task."""
    record = TaskService.get_task(task_id)
    if not record:
        return jsonify({"error": "Not Found", "message": "Task ID not recognized"}), 404

    return jsonify({"task": record.to_dict()}), 200


@tasks_bp.route("", methods=["GET"])
@jwt_required()
def list_user_tasks():
    """Retrieve all async tasks dispatched by the authenticated user."""
    user_id = int(get_jwt_identity())
    stmt = select(AsyncTaskRecord).where(AsyncTaskRecord.user_id == user_id).order_by(AsyncTaskRecord.created_at.desc())
    records = db.session.execute(stmt).scalars().all()
    
    return jsonify({
        "tasks": [r.to_dict() for r in records]
    }), 200
