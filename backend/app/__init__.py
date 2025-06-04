from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_pymongo import PyMongo
import os
from pymongo import MongoClient

bcrypt = Bcrypt()
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    # CORS(app)
    
    # Load config
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # MongoDB client setup with error handling
    try:
        app.db_client = MongoClient(app.config['MONGO_URI'])
        app.db = app.db_client.get_default_database()
    except Exception as e:
        print(f"Database connection error: {e}")

    bcrypt.init_app(app)

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app
