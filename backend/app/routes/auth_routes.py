from flask import Blueprint, request, jsonify,current_app
from ..models.user_model import User
from ..utils.jwt import generate_token, verify_token
import datetime
import werkzeug
import jwt
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.find_by_email(data['email'])
    if not user or not User.verify_password(user['password'], data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode({
        'user_id': str(user['_id']),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        'token': token,
        'role': user.get('role', 'client'),
        'email': user.get('email')
    }), 200


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')  # Not used but stored for completeness

    if User.find_by_email(email):
        return jsonify({'message': 'Email already registered'}), 400

    user_id = User.create(email, password, role='admin')
    return jsonify({'message': 'Admin account created', 'user_id': str(user_id)}), 201

@auth_bp.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing'}), 401

    user_id = verify_token(token.split(" ")[1])  # Expecting "Bearer <token>"
    if not user_id:
        return jsonify({'message': 'Invalid or expired token'}), 401

    return jsonify({'message': 'Access granted', 'user_id': user_id}), 200

@auth_bp.route('/settings', methods=['PUT'])
def update_settings():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Unauthorized'}), 401

    user_id = verify_token(token.split(" ")[1])
    if not user_id:
        return jsonify({'message': 'Invalid or expired token'}), 401

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email and not password:
        return jsonify({'message': 'Nothing to update'}), 400

    update_data = {}
    if email:
        update_data['email'] = email
    if password:
        from werkzeug.security import generate_password_hash
        update_data['password'] = generate_password_hash(password)

    from bson import ObjectId
    result = User.get_collection().update_one({'_id': ObjectId(user_id)}, {'$set': update_data})
    
    return jsonify({'message': 'Settings updated successfully'}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # In a stateless JWT system, logout is handled client-side by deleting the token.
    return jsonify({'message': 'Logged out successfully'}), 200 

@auth_bp.route('/check_token', methods=['GET'])
def check_token():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing'}), 401

    user_id = verify_token(token.split(" ")[1])
    if not user_id:
        return jsonify({'message': 'Invalid or expired token'}), 401

    return jsonify({'message': 'Token is valid', 'user_id': user_id}), 200

@auth_bp.route('/set-password', methods=['POST'])
def set_password():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password required'}), 400

    user = User.find_by_email(email)
    
    if user:
        if 'password' in user and user['password']:
            return jsonify({'message': 'Password already set. Please login.'}), 400
        hashed = generate_password_hash(password)
        User.get_collection().update_one({'email': email}, {'$set': {'password': hashed}})
        return jsonify({'message': 'Password set successfully'}), 200

    # ✅ Check in students collection
    student = current_app.db.students.find_one({'email': email})
    if student:
        hashed = generate_password_hash(password)
        new_user = {
            'email': email,
            'password': hashed,
            'role': 'client',  # ✅ Add role for proper login match
            'student_id': student.get('student_id'),
            'name': student.get('name')  # optional
        }
        User.get_collection().insert_one(new_user)
        return jsonify({'message': 'Password set successfully and account created.'}), 200


    return jsonify({'message': 'Email not registered'}), 404
