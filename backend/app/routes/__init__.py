from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

# Extract DB name from URI
db_name = mongo_uri.rsplit("/", 1)[-1]
db = client[db_name]
