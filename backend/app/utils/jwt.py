import jwt
from flask import current_app
from datetime import datetime, timedelta

def generate_token(user_id):
    payload = {
        'user_id': str(user_id),  # MongoDB ObjectId to string
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        print("Decoded JWT payload:", payload)  # 🔍 Debug output
        return payload.get('user_id')  # Use .get() to avoid KeyError
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return None
    except jwt.InvalidTokenError as e:
        print("Invalid token:", str(e))
        return None
