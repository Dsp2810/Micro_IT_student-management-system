from flask import Blueprint, request, jsonify, current_app
from ..utils.jwt import verify_token
from ..models.attendance_model import Attendance

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/summary", methods=["GET"])
def dashboard_summary():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return jsonify({"message": "Unauthorized"}), 401

    user_id = verify_token(token.split(" ")[1])
    if not user_id:
        return jsonify({"message": "Invalid token"}), 401

    try:
        # Count total students
        total_students = current_app.db.students.count_documents({})

        # Get attendance summary using aggregation
        attendance = Attendance.get_attendance_summary()

        # Count students below and above 75% attendance
        low_attendance = len([a for a in attendance if a.get("alert")])
        active = len([a for a in attendance if not a.get("alert")])

        return jsonify({
            "total_students": total_students,
            "active_students": active,
            "low_attendance": low_attendance
        }), 200
    except Exception as e:
        return jsonify({
            "message": "Error loading dashboard summary",
            "error": str(e)
        }), 500
