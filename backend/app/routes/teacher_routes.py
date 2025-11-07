

# # app/routes/teacher_routes.py
# from flask import Blueprint, jsonify, request, current_app
# from app.models.teacher import Teacher
# from app.models.central import Tenant  # central DB tenant model
# from app.services.db_manager import get_tenant_engine, CENTRAL_DB_URI
# from app.modules.teachers.service import add_teacher
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import traceback
# import sys

# teacher_bp = Blueprint("teacher_bp", __name__)

# # =========================================================
# # 🧾 GET all teachers (tenant-based)
# # =========================================================
# @teacher_bp.route("/teachers/", methods=["GET"])
# def get_teachers():
#     central_session = None
#     tenant_session = None
#     try:
#         subdomain = request.headers.get("X-Subdomain")
#         if not subdomain:
#             return jsonify({"error": "Missing X-Subdomain header"}), 400

#         current_app.logger.info(f"📡 GET /teachers for subdomain: {subdomain}")

#         # 1️⃣ Connect to central DB and fetch tenant info
#         central_engine = create_engine(CENTRAL_DB_URI)
#         CentralSession = sessionmaker(bind=central_engine)
#         central_session = CentralSession()

#         tenant = central_session.query(Tenant).filter_by(subdomain=subdomain).first()
#         if not tenant:
#             return jsonify({"error": f"No tenant found for subdomain '{subdomain}'"}), 404

#         # 2️⃣ Connect to tenant’s DB
#         engine = get_tenant_engine(tenant)
#         Session = sessionmaker(bind=engine)
#         tenant_session = Session()

#         # 3️⃣ Fetch teachers
#         teachers = tenant_session.query(Teacher).all()
#         current_app.logger.info(f"✅ Found {len(teachers)} teachers for tenant '{subdomain}'")

#         return jsonify([t.to_dict() for t in teachers]), 200

#     except Exception as e:
#         print("\n🔥 ERROR fetching teachers:", file=sys.stderr)
#         traceback.print_exc()
#         current_app.logger.error(f"🔥 ERROR fetching teachers: {e}")
#         return jsonify({
#             "error": str(e),
#             "trace": traceback.format_exc()
#         }), 500

#     finally:
#         # ✅ Ensure sessions are closed properly
#         if tenant_session:
#             tenant_session.close()
#         if central_session:
#             central_session.close()


# # =========================================================
# # 🧩 Create a new teacher (tenant-based)
# # =========================================================
# @teacher_bp.route("/teachers", methods=["POST"])
# def create_teacher():
#     central_session = None
#     tenant_session = None
#     try:
#         subdomain = request.headers.get("X-Subdomain")
#         if not subdomain:
#             return jsonify({"error": "Missing X-Subdomain header"}), 400

#         data = request.get_json()
#         if not data:
#             return jsonify({"error": "Missing JSON body"}), 400

#         current_app.logger.info(f"🧩 POST /teachers for subdomain: {subdomain}, data: {data}")

#         # 1️⃣ Connect to central DB
#         central_engine = create_engine(CENTRAL_DB_URI)
#         CentralSession = sessionmaker(bind=central_engine)
#         central_session = CentralSession()

#         tenant = central_session.query(Tenant).filter_by(subdomain=subdomain).first()
#         if not tenant:
#             return jsonify({"error": f"No tenant found for subdomain '{subdomain}'"}), 404

#         # 2️⃣ Connect to tenant’s DB
#         engine = get_tenant_engine(tenant)
#         Session = sessionmaker(bind=engine)
#         tenant_session = Session()

#         # 3️⃣ Add teacher
#         result = add_teacher(tenant_session, data)
#         current_app.logger.info(f"✅ Teacher added successfully for tenant '{subdomain}'")

#         return jsonify(result), 201

#     except Exception as e:
#         print("\n🔥 ERROR adding teacher:", file=sys.stderr)
#         traceback.print_exc()
#         current_app.logger.error(f"🔥 ERROR adding teacher: {e}")
#         return jsonify({
#             "error": str(e),
#             "trace": traceback.format_exc()
#         }), 500

#     finally:
#         # ✅ Close sessions
#         if tenant_session:
#             tenant_session.close()
#         if central_session:
#             central_session.close()



# app/routes/teacher_routes.py
from flask import Blueprint, jsonify, request, current_app
from app.models.teacher import Teacher
from app.models.central import Tenant  # central DB tenant model
from app.services.db_manager import get_tenant_engine, CENTRAL_DB_URI
from app.modules.teachers.service import add_teacher
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import traceback
import sys

teacher_bp = Blueprint("teacher_bp", __name__)

# =========================================================
# Helper: Resolve tenant from request host
# =========================================================
def resolve_tenant():
    """
    Automatically determine tenant subdomain from request.host.
    Works for localhost (dev) and real subdomains.
    """
    host = request.host.split(':')[0]  # remove port if present
    parts = host.split('.')

    if len(parts) < 2:
        # fallback for localhost: use default tenant
        return "evol"

    return parts[0]  # first part of host is treated as subdomain


# =========================================================
# 🧾 GET all teachers (tenant-based)
# =========================================================
@teacher_bp.route("/teachers/", methods=["GET"])
def get_teachers():
    central_session = None
    tenant_session = None
    try:
        subdomain = resolve_tenant()
        current_app.logger.info(f"📡 GET /teachers for subdomain: {subdomain}")

        # 1️⃣ Connect to central DB and fetch tenant info
        central_engine = create_engine(CENTRAL_DB_URI)
        CentralSession = sessionmaker(bind=central_engine)
        central_session = CentralSession()

        tenant = central_session.query(Tenant).filter_by(subdomain=subdomain).first()
        if not tenant:
            return jsonify({"error": f"No tenant found for subdomain '{subdomain}'"}), 404

        # 2️⃣ Connect to tenant DB
        engine = get_tenant_engine(tenant)
        Session = sessionmaker(bind=engine)
        tenant_session = Session()

        # 3️⃣ Fetch teachers
        teachers = tenant_session.query(Teacher).all()
        current_app.logger.info(f"✅ Found {len(teachers)} teachers for tenant '{subdomain}'")

        return jsonify([t.to_dict() for t in teachers]), 200

    except Exception as e:
        print("\n🔥 ERROR fetching teachers:", file=sys.stderr)
        traceback.print_exc()
        current_app.logger.error(f"🔥 ERROR fetching teachers: {e}")
        return jsonify({
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500

    finally:
        # ✅ Ensure sessions are closed properly
        if tenant_session:
            tenant_session.close()
        if central_session:
            central_session.close()


# =========================================================
# 🧩 Create a new teacher (tenant-based)
# =========================================================
@teacher_bp.route("/teachers", methods=["POST"])
def create_teacher():
    central_session = None
    tenant_session = None
    try:
        subdomain = resolve_tenant()
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        current_app.logger.info(f"🧩 POST /teachers for subdomain: {subdomain}, data: {data}")

        # 1️⃣ Connect to central DB and fetch tenant
        central_engine = create_engine(CENTRAL_DB_URI)
        CentralSession = sessionmaker(bind=central_engine)
        central_session = CentralSession()

        tenant = central_session.query(Tenant).filter_by(subdomain=subdomain).first()
        if not tenant:
            return jsonify({"error": f"No tenant found for subdomain '{subdomain}'"}), 404

        # 2️⃣ Connect to tenant DB
        engine = get_tenant_engine(tenant)
        Session = sessionmaker(bind=engine)
        tenant_session = Session()

        # 3️⃣ Add teacher
        result = add_teacher(tenant_session, data)
        current_app.logger.info(f"✅ Teacher added successfully for tenant '{subdomain}'")

        return jsonify(result), 201

    except Exception as e:
        print("\n🔥 ERROR adding teacher:", file=sys.stderr)
        traceback.print_exc()
        current_app.logger.error(f"🔥 ERROR adding teacher: {e}")
        return jsonify({
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500

    finally:
        # ✅ Close sessions
        if tenant_session:
            tenant_session.close()
        if central_session:
            central_session.close()
