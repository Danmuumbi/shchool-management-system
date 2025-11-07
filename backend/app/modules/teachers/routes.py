

# backend/app/modules/teachers/routes.py
from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import text
from werkzeug.security import generate_password_hash
from app.services.db_manager import get_tenant_session
from app.utils.tenant_resolver import get_tenant_from_request
from app.utils.auth_middleware import token_required
import traceback, secrets

teachers_bp = Blueprint("teachers_bp", __name__)


# --- Ensure teachers table exists and auto-sync columns
def ensure_teacher_table(session):
    # Create table if not exists
    session.execute(text("""
        CREATE TABLE IF NOT EXISTS teachers (
            id SERIAL PRIMARY KEY,
            teacher_number VARCHAR(50) UNIQUE NOT NULL,
            national_id VARCHAR(20) UNIQUE,
            first_name VARCHAR(100) NOT NULL,
            middle_name VARCHAR(100),
            last_name VARCHAR(100) NOT NULL,
            gender VARCHAR(10),
            date_of_birth DATE,
            email VARCHAR(120) UNIQUE NOT NULL,
            phone VARCHAR(20),
            address VARCHAR(255),
            qualification VARCHAR(255),
            profile_picture VARCHAR(255),
            date_joined DATE DEFAULT CURRENT_DATE,
            is_active BOOLEAN DEFAULT TRUE,
            created_by VARCHAR(100)
        );
    """))

    # ✅ Ensure missing columns are added (auto-sync)
    expected_columns = {
        "teacher_number": "VARCHAR(50) UNIQUE NOT NULL",
        "national_id": "VARCHAR(20) UNIQUE",
        "first_name": "VARCHAR(100) NOT NULL",
        "middle_name": "VARCHAR(100)",
        "last_name": "VARCHAR(100) NOT NULL",
        "gender": "VARCHAR(10)",
        "date_of_birth": "DATE",
        "email": "VARCHAR(120) UNIQUE NOT NULL",
        "phone": "VARCHAR(20)",
        "address": "VARCHAR(255)",
        "qualification": "VARCHAR(255)",
        "profile_picture": "VARCHAR(255)",
        "date_joined": "DATE DEFAULT CURRENT_DATE",
        "is_active": "BOOLEAN DEFAULT TRUE",
        "created_by": "VARCHAR(100)"
    }

    for col, dtype in expected_columns.items():
        try:
            session.execute(text(f"ALTER TABLE teachers ADD COLUMN {col} {dtype};"))
        except Exception:
            # ignore if column already exists
            pass

    session.commit()


# --- Ensure users table exists
def ensure_users_table(session):
    session.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(255),
            role VARCHAR(50) DEFAULT 'teacher',
            created_at TIMESTAMP DEFAULT NOW()
        );
    """))
    session.commit()


# --- Check if teachers module is active
def is_module_active(session, module_name="teachers"):
    session.execute(text("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id SERIAL PRIMARY KEY,
            module_name VARCHAR(100) UNIQUE,
            subscribed_on TIMESTAMP DEFAULT NOW()
        );
    """))
    res = session.execute(
        text("SELECT 1 FROM subscriptions WHERE module_name = :m"),
        {"m": module_name}
    ).fetchone()
    return bool(res)


# ✅ CREATE TEACHER
@teachers_bp.route("/create", methods=["POST"])
@token_required
def create_teacher():
    try:
        tenant = get_tenant_from_request(request)
        session = get_tenant_session(tenant)

        # Verify module activation
        if not is_module_active(session):
            return jsonify({"error": "Module 'teachers' not active"}), 403

        # Ensure necessary tables exist
        ensure_teacher_table(session)
        ensure_users_table(session)

        data = request.get_json() or {}
        required = ["teacher_number", "first_name", "last_name", "email"]
        for f in required:
            if not data.get(f):
                return jsonify({"error": f"Missing field: {f}"}), 400

        # Generate secure random password if not provided
        raw_password = data.get("password") or secrets.token_urlsafe(8)
        password_hash = generate_password_hash(raw_password)

        # Insert teacher record
        session.execute(text("""
            INSERT INTO teachers (
                teacher_number, national_id, first_name, middle_name, last_name,
                gender, date_of_birth, email, phone, address,
                qualification, profile_picture, date_joined,
                is_active, created_by
            )
            VALUES (
                :teacher_number, :national_id, :first_name, :middle_name, :last_name,
                :gender, :date_of_birth, :email, :phone, :address,
                :qualification, :profile_picture, CURRENT_DATE,
                :is_active, :created_by
            );
        """), {
            "teacher_number": data["teacher_number"],
            "national_id": data.get("national_id"),
            "first_name": data["first_name"],
            "middle_name": data.get("middle_name"),
            "last_name": data["last_name"],
            "gender": data.get("gender"),
            "date_of_birth": data.get("date_of_birth"),
            "email": data["email"],
            "phone": data.get("phone"),
            "address": data.get("address"),
            "qualification": data.get("qualification"),
            "profile_picture": data.get("profile_picture"),
            "is_active": data.get("is_active", True),
            "created_by": data.get("created_by")
        })

        # Insert user account for the teacher
        session.execute(text("""
            INSERT INTO users (email, password_hash, full_name, role)
            VALUES (:email, :password_hash, :full_name, 'teacher');
        """), {
            "email": data["email"],
            "password_hash": password_hash,
            "full_name": f"{data['first_name']} {data['last_name']}"
        })

        session.commit()
        return jsonify({
            "message": f"Teacher {data['first_name']} {data['last_name']} created successfully",
            "email": data["email"],
            "generated_password": raw_password
        }), 201

    except Exception as e:
        session.rollback()
        current_app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


# ✅ LIST TEACHERS
@teachers_bp.route("/", methods=["GET"])
@token_required
def list_teachers():
    try:
        tenant = get_tenant_from_request(request)
        session = get_tenant_session(tenant)

        ensure_teacher_table(session)

        result = session.execute(text("SELECT * FROM teachers ORDER BY id DESC")).fetchall()
        teachers = [dict(r._mapping) for r in result]

        return jsonify({"teachers": teachers}), 200
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500




# ✅ DELETE TEACHER
@teachers_bp.route("/<int:teacher_id>", methods=["DELETE"])
@token_required
def delete_teacher(teacher_id):
    try:
        tenant = get_tenant_from_request(request)
        session = get_tenant_session(tenant)

        ensure_teacher_table(session)
        session.execute(
            text("DELETE FROM teachers WHERE id = :id"),
            {"id": teacher_id}
        )
        session.commit()
        return jsonify({"message": f"Teacher {teacher_id} deleted successfully"}), 200
    except Exception as e:
        session.rollback()
        current_app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
