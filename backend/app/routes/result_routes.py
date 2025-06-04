from flask import Blueprint, request, jsonify
from ..utils.jwt import verify_token
from ..models.user_model import User
from ..models.result_model import Result
from bson import ObjectId

result_bp = Blueprint('results', __name__)

def authenticate_admin():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing'}), 401

    user_id = verify_token(token.split(" ")[1])
    if not user_id:
        return jsonify({'message': 'Invalid or expired token'}), 401

    user = User.collection.find_one({'_id': ObjectId(user_id)})
    if user['role'] != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    return user_id

@result_bp.route('/add-user', methods=['POST'])
def add_user():
    user_id = authenticate_admin()
    if isinstance(user_id, dict):  # Error response
        return user_id

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    new_user_id = User.add_user(email, password, role)
    if not new_user_id:
        return jsonify({'message': 'Email already registered'}), 400

    return jsonify({'message': 'User added successfully', 'user_id': str(new_user_id)}), 201

@result_bp.route('/add-result', methods=['POST'])
def add_result():
    user_id = authenticate_admin()
    if isinstance(user_id, dict):  # Error response
        return user_id

    data = request.get_json()
    student_id = data.get('student_id')
    subject = data.get('subject')
    marks = data.get('marks')

    result_id = Result.create(student_id, subject, marks)
    return jsonify({'message': 'Result added successfully', 'result_id': str(result_id)}), 201