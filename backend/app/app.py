

# backend/app/app.py
from flask import Flask, app, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from dotenv import load_dotenv

# --- Load environment first
load_dotenv()


from app.config import Config
from app.extensions import db, mail


def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # backend/app/app.py
    CORS(
    app,
    resources={r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://*.localhost:3000"
        ]
    }},
    supports_credentials=True
)


    # Load configuration from Config class
    app.config.from_object(Config)

    # ✅ Initialize core extensions early
    db.init_app(app)
    jwt = JWTManager(app)
    mail.init_app(app)

    # ✅ Import Blueprints *after* JWT & config initialized
    from app.routes.auth_routes import auth_bp
    from app.routes.tenant_routes import tenant_bp
    from app.routes.tenant_profile_routes import profile_bp
    from app.routes.teacher_routes import teacher_bp
    from app.modules.teachers.routes import teachers_bp
    from app.modules.subjects.routes import subjects_bp

    # ✅ Register all blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(tenant_bp, url_prefix="/api/tenant")
    app.register_blueprint(profile_bp, url_prefix="/api")
    app.register_blueprint(teacher_bp, url_prefix="/api/teachers")
    app.register_blueprint(teachers_bp, url_prefix="/api/tenant/modules/teachers")
    app.register_blueprint(subjects_bp, url_prefix="/api/tenant/modules/subjects")


    

    # ✅ Uploaded files route
    @app.route("/uploads/<path:filename>")
    def serve_uploaded_file(filename):
        upload_folder = os.path.join(os.getcwd(), "uploads")
        file_path = os.path.join(upload_folder, filename)
        if not os.path.exists(file_path):
            return {"error": "File not found"}, 404
        return send_from_directory(upload_folder, filename)

    @app.route("/")
    def home():
        return {"message": "✅ EvolTechs School Management API running successfully..."}

    return app


