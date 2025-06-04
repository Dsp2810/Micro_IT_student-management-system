# app/models/student_model.py
from flask import current_app

class Student:
    @staticmethod
    def get_collection():
        return current_app.db.students

    @staticmethod
    def create(data):
        return Student.get_collection().insert_one(data).inserted_id
    @staticmethod
    def get_all():
        return list(Student.get_collection().find({}, {
            "_id": 0,  
            "name": 1,
            "email": 1,
            "student_id": 1,
            "semester": 1,
            "division": 1
        }))