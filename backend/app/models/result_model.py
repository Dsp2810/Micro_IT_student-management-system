from ..utils.db import mongo
from bson import ObjectId
from flask import current_app

class Result:
    @staticmethod
    def get_collection():
        return current_app.db.results

    @staticmethod
    def create(student_id, subject, marks):
        return Result.get_collection().insert_one({
            'student_id': student_id,
            'subject': subject,
            'marks': int(marks)
        }).inserted_id