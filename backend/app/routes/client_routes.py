from flask import Blueprint, request, jsonify, current_app
from ..utils.jwt import verify_token
from bson import ObjectId

client_bp = Blueprint('client', __name__)

@client_bp.route('/dashboard', methods=['GET'])
def client_dashboard():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return jsonify({"message": "Unauthorized"}), 401

    user_id = verify_token(token.split(" ")[1])
    if not user_id:
        return jsonify({"message": "Invalid token"}), 401

    db = current_app.db

    # Fetch user
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user or 'student_id' not in user:
        return jsonify({"message": "Student record not linked to this user"}), 404

    student_id = user['student_id']

    # Fetch student info
    student = db.students.find_one({"student_id": student_id})
    if not student:
        return jsonify({"message": "Student not found"}), 404

    # Fetch attendance summary
    attendance_records = list(db.attendance.find({"student_id": student_id}))
    total_days = len(attendance_records)
    present_days = sum(1 for record in attendance_records if record.get("present") == True)
    attendance_percent = round((present_days / total_days) * 100, 2) if total_days else 0

    # Fetch latest grade
    result = db.results.find_one({"student_id": student_id}, sort=[("_id", -1)])  # Latest result
    grade = f"{result['subject']}: {result['marks']}" if result else "No result"

    return jsonify({
        "studentName": student.get("name"),
        "attendance": f"{attendance_percent}%",
        "grades": grade,
        "next_class": "Maths - 10:00 AM"  # You can replace this with real data later
    }), 200
