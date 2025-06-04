from flask import current_app

class Attendance:
    @staticmethod
    def get_collection():
        return current_app.db.attendance

    @staticmethod
    def mark(student_id, date, present):
        collection = Attendance.get_collection()
        return collection.update_one(
            {"student_id": student_id, "date": date},
            {"$set": {"present": present}},
            upsert=True
        )

    @staticmethod
    def get_attendance_summary():
        collection = Attendance.get_collection()
        pipeline = [
            {"$group": {
                "_id": "$student_id",
                "total_days": {"$sum": 1},
                "present_days": {
                    "$sum": {"$cond": ["$present", 1, 0]}
                }
            }},
            {"$project": {
                "attendance_percent": {
                    "$multiply": [{"$divide": ["$present_days", "$total_days"]}, 100]
                },
                "alert": {
                    "$cond": [
                        {"$lt": [
                            {"$multiply": [{"$divide": ["$present_days", "$total_days"]}, 100]},
                            75
                        ]},
                        True,
                        False
                    ]
                }
            }}
        ]
        return list(collection.aggregate(pipeline))
