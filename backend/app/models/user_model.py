from ..utils.db import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from flask import current_app

class User:
    
    @staticmethod
    def get_collection():
        return current_app.db.users

    @staticmethod
    def create(email, password, role='admin'):
        hashed_password = generate_password_hash(password)
        return User.get_collection().insert_one({
            'email': email,
            'password': hashed_password,
            'role': role
        }).inserted_id

    @staticmethod
    def find_by_email(email):
        return User.get_collection().find_one({'email': email})

    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)

    @staticmethod
    def add_user(email, password, role):
        if User.find_by_email(email):
            return None
        return User.create(email, password, role)