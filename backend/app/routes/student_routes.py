# app/routes/student_routes.py
from flask import Blueprint, request, jsonify
from ..models.student_model import Student
from ..models.attendance_model import Attendance
from ..utils.jwt import verify_token
from bson import ObjectId

student_bp = Blueprint('student', __name__)

@student_bp.route('/add-student', methods=['POST'])
def add_student():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({'message': 'Unauthorized'}), 401

    user_id = verify_token(token.split(" ")[1])
    if not user_id:
        return jsonify({'message': 'Invalid or expired token'}), 403

    data = request.get_json()
    required_fields = ['name', 'email', 'student_id', 'semester', 'division']

    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required student fields'}), 400

    try:
        student_id = Student.create(data)
        return jsonify({'message': 'Student added successfully', 'id': str(student_id)}), 201
    except Exception as e:
        return jsonify({'message': 'Failed to add student', 'error': str(e)}), 500

@student_bp.route('/list', methods=['GET'])
def list_students():
    token = request.headers.get("Authorization")
    if not token or not verify_token(token.split(" ")[1]):
        return jsonify({"message": "Unauthorized"}), 401

    students = list(Student.get_collection().find({}, {"_id": 0}))
    attendance_summary = Attendance.get_attendance_summary()

    # Map attendance summary by student ID
    attendance_map = {item["_id"]: item["attendance_percent"] for item in attendance_summary}

    for student in students:
        student["attendance"] = round(attendance_map.get(student["student_id"], 0), 2)

    return jsonify(students), 200