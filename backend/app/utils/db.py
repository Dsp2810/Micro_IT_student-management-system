from flask import current_app
from pymongo import MongoClient
import os

mongo = MongoClient()

def init_db(app):
    mongo_uri = app.config.get("MONGO_URI")
    if not mongo_uri:
        raise Exception("MONGO_URI is not set in config")
    
    client = MongoClient(mongo_uri)
    db_name = mongo_uri.rsplit("/", 1)[-1]  # Extract DB name from URI
    db = client[db_name]
    
    app.mongo_client = client
    app.db = db  # ✅ This sets app.db so you can access current_app.db later
