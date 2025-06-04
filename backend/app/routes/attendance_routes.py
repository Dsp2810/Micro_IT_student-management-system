# app/routes/attendance_routes.py
from flask import Blueprint, request, jsonify
from ..models.attendance_model import Attendance
from ..utils.jwt import verify_token
from bson import ObjectId

attendance_bp = Blueprint('attendance', __name__)

def authenticate():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return None
    return verify_token(token.split(" ")[1])

@attendance_bp.route("/mark-attendance", methods=["POST"])
def mark_attendance():
    user_id = authenticate()
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    student_id = data.get("studentId")
    date = data.get("date")
    present = data.get("present")

    if not student_id or not date:
        return jsonify({"message": "Missing data"}), 400

    Attendance.mark(student_id, date, present)
    return jsonify({"message": "Attendance recorded successfully"}), 200

@attendance_bp.route("/summary", methods=["GET"])
def attendance_summary():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Unauthorized"}), 401

    try:
        summary = Attendance.get_attendance_summary()
        return jsonify({"summary": summary}), 200
    except Exception as e:
        return jsonify({"message": "Failed to fetch summary", "error": str(e)}), 500