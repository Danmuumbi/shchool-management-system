from flask import Blueprint, request, jsonify, send_from_directory
from sqlalchemy import create_engine, text
from app.services.db_manager import tenant_db_uri_from_parts
from app.models.central import Tenant
import os

# -----------------------------------
# Blueprint setup
# -----------------------------------
profile_bp = Blueprint("profile", __name__)

# -----------------------------------
# Uploads configuration
# -----------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.normpath(os.path.join(BASE_DIR, "../../uploads"))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


# Helper to check allowed file types
def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


# -----------------------------------
# Route: Update School Profile
# -----------------------------------
@profile_bp.route("/profile/update", methods=["POST"])
def update_profile():
    data = request.form
    subdomain = data.get("subdomain")

    # Validate tenant
    tenant = Tenant.query.filter_by(subdomain=subdomain).first()
    if not tenant:
        return jsonify({"error": "School not found"}), 404

    # Build DB connection string for tenant
    tenant_db_uri = tenant_db_uri_from_parts(
        tenant.db_host, tenant.db_port, tenant.db_name, tenant.db_user, tenant.db_password
    )
    engine = create_engine(tenant_db_uri)

    logo_url, hero_url = None, None

    # ✅ Handle image uploads safely
    if "logo" in request.files and request.files["logo"].filename:
        logo = request.files["logo"]
        if allowed_file(logo.filename):
            ext = os.path.splitext(logo.filename)[1].lower()
            logo_filename = f"{subdomain}_logo{ext}"
            save_path = os.path.join(UPLOAD_FOLDER, logo_filename)
            logo.save(save_path)
            logo_url = f"/uploads/{logo_filename}"

    if "hero" in request.files and request.files["hero"].filename:
        hero = request.files["hero"]
        if allowed_file(hero.filename):
            ext = os.path.splitext(hero.filename)[1].lower()
            hero_filename = f"{subdomain}_hero{ext}"
            save_path = os.path.join(UPLOAD_FOLDER, hero_filename)
            hero.save(save_path)
            hero_url = f"/uploads/{hero_filename}"

    # ✅ Save or update the database record
    with engine.begin() as conn:
        # Ensure table exists
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS school_profile (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                motto TEXT,
                about TEXT,
                email VARCHAR(255),
                phone VARCHAR(100),
                color VARCHAR(50),
                logo_url TEXT,
                hero_url TEXT
            )
        """))

        # Keep only one record
        conn.execute(text("DELETE FROM school_profile"))

        # Insert new data
        conn.execute(text("""
            INSERT INTO school_profile (name, motto, about, email, phone, color, logo_url, hero_url)
            VALUES (:name, :motto, :about, :email, :phone, :color, :logo_url, :hero_url)
        """), {
            "name": data.get("name"),
            "motto": data.get("motto"),
            "about": data.get("about"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "color": data.get("color"),
            "logo_url": logo_url,
            "hero_url": hero_url
        })

    engine.dispose()
    return jsonify({"message": "Profile updated successfully"}), 200


# -----------------------------------
# Route: Fetch School Profile
# -----------------------------------
@profile_bp.route("/profile/<subdomain>", methods=["GET"])
def get_profile(subdomain):
    tenant = Tenant.query.filter_by(subdomain=subdomain).first()
    if not tenant:
        return jsonify({"error": "School not found"}), 404

    tenant_db_uri = tenant_db_uri_from_parts(
        tenant.db_host, tenant.db_port, tenant.db_name, tenant.db_user, tenant.db_password
    )

    engine = create_engine(tenant_db_uri)
    with engine.connect() as conn:
        row = conn.execute(text("SELECT * FROM school_profile LIMIT 1")).fetchone()
    engine.dispose()

    if not row:
        return jsonify({"message": "Profile not yet set"}), 200

    return jsonify(dict(row._mapping))


# -----------------------------------
# Route: Serve Uploaded Images
# -----------------------------------
@profile_bp.route("/uploads/<path:filename>")
def serve_uploaded_file(filename):
    """
    Serves image files directly from the uploads folder.
    Example URL: http://localhost:5000/uploads/evol_logo.png
    """
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
