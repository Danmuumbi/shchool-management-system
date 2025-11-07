

# backend/app/modules/subjects/routes.py
from flask import Blueprint, jsonify, request, current_app, g
from sqlalchemy import text
from app.services.db_manager import get_tenant_session
from app.utils.tenant_resolver import get_tenant_from_request
import traceback

subjects_bp = Blueprint("subjects_bp", __name__)

@subjects_bp.route("/", methods=["GET"])
def get_subjects():
    """List all subjects for the current tenant."""
    try:
        tenant = get_tenant_from_request(request)
        g.tenant = tenant

        session = get_tenant_session(tenant)

        # Ensure subjects table exists
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS subjects (
                id SERIAL PRIMARY KEY,
                code VARCHAR(20) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                description TEXT
            );
        """))

        rows = session.execute(text("SELECT id, code, name, description FROM subjects ORDER BY name ASC")).fetchall()
        subjects = [dict(r._mapping) for r in rows]

        return jsonify(subjects), 200

    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@subjects_bp.route("/create", methods=["POST"])
def create_subject():
    """Create a new subject for this tenant."""
    try:
        tenant = get_tenant_from_request(request)
        g.tenant = tenant

        session = get_tenant_session(tenant)
        data = request.get_json() or {}

        required = ["code", "name"]
        for f in required:
            if not data.get(f):
                return jsonify({"error": f"Missing field: {f}"}), 400

        session.execute(text("""
            INSERT INTO subjects (code, name, description)
            VALUES (:code, :name, :description)
        """), {
            "code": data["code"],
            "name": data["name"],
            "description": data.get("description")
        })

        session.commit()
        return jsonify({"message": "Subject created successfully"}), 201

    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        session.rollback()
        return jsonify({"error": str(e)}), 500
