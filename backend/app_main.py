from flask import Flask
from flask_cors import CORS
from app.routes.auth_routes import auth_bp
from app.routes.result_routes import result_bp
from app.routes.student_routes import student_bp
from app.routes.attendance_routes import attendance_bp
from app.routes.admin_routes import dashboard_bp
from app.routes.client_routes import client_bp
from app.utils.db import init_db
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# ✅ Allow cross-origin requests from all origins (for dev). Change '*' to your frontend domain in production.
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Load configuration (like SECRET_KEY, MONGO_URI)
app.config.from_object('config.Config')

# ✅ Initialize MongoDB
init_db(app)

# ✅ Register Blueprints with proper prefixes
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(result_bp, url_prefix='/api/results')
app.register_blueprint(student_bp, url_prefix='/api/students')
app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard') 
app.register_blueprint(client_bp, url_prefix='/api/client')
# Correct prefix for dashboard

# ✅ Run the app
if __name__ == '__main__':
    app.run(debug=True)
