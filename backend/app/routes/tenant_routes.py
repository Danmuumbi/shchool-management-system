

# from flask import Blueprint, request, jsonify, g, current_app
# from sqlalchemy import text
# from app.middleware import tenant_resolver
# from app.services.db_manager import get_tenant_engine
# import traceback

# tenant_bp = Blueprint("tenant", __name__)  # simpler name


# # ✅ Resolve tenant before every request
# @tenant_bp.before_request
# def before_tenant_request():
#     # Handle CORS preflight OPTIONS requests early
#     if request.method == "OPTIONS":
#         return "", 200

#     response = tenant_resolver()
#     if response is not None:
#         return response


# # ✅ Get tenant metadata
# @tenant_bp.route("/meta", methods=["GET"])
# def tenant_meta():
#     tenant = getattr(g, "tenant", None)
#     if tenant is None:
#         return jsonify({"error": "Tenant not resolved"}), 400
#     return jsonify({"tenant": tenant.to_dict()}), 200


# # ✅ Subscribe tenant to a module
# @tenant_bp.route("/subscribe", methods=["POST"])
# def subscribe_to_module():
#     try:
#         tenant = getattr(g, "tenant", None)
#         if tenant is None:
#             return jsonify({"error": "Tenant not resolved"}), 400

#         data = request.get_json()
#         module_name = data.get("module") or data.get("module_name")
#         if not module_name:
#             return jsonify({"error": "Module name required"}), 400

#         engine = get_tenant_engine(tenant)

#         with engine.begin() as conn:
#             # Ensure subscriptions table exists
#             conn.execute(text("""
#                 CREATE TABLE IF NOT EXISTS subscriptions (
#                     id SERIAL PRIMARY KEY,
#                     module_name VARCHAR(100) UNIQUE,
#                     subscribed_on TIMESTAMP DEFAULT NOW()
#                 );
#             """))

#             # Check if already subscribed
#             exists = conn.execute(
#                 text("SELECT module_name FROM subscriptions WHERE module_name = :m"),
#                 {"m": module_name}
#             ).fetchone()

#             if exists:
#                 return jsonify({"message": f"Already subscribed to {module_name}"}), 200

#             # Insert new subscription
#             conn.execute(
#                 text("INSERT INTO subscriptions (module_name) VALUES (:m)"),
#                 {"m": module_name}
#             )

#         current_app.logger.info(f"✅ Tenant '{tenant.subdomain}' subscribed to '{module_name}'")
#         return jsonify({"message": f"Subscribed to {module_name} successfully!"}), 200

#     except Exception as e:
#         current_app.logger.error(traceback.format_exc())
#         return jsonify({"error": str(e)}), 500


# # ✅ Get all subscriptions for current tenant
# @tenant_bp.route("/subscriptions", methods=["GET"])
# def get_subscriptions():
#     try:
#         tenant = getattr(g, "tenant", None)
#         if tenant is None:
#             return jsonify({"error": "Tenant not resolved"}), 400

#         engine = get_tenant_engine(tenant)

#         with engine.begin() as conn:
#             conn.execute(text("""
#                 CREATE TABLE IF NOT EXISTS subscriptions (
#                     id SERIAL PRIMARY KEY,
#                     module_name VARCHAR(100) UNIQUE,
#                     subscribed_on TIMESTAMP DEFAULT NOW()
#                 );
#             """))
#             result = conn.execute(text("SELECT module_name FROM subscriptions"))
#             modules = [r[0] for r in result]

#         return jsonify({"subscribed": {m: True for m in modules}}), 200

#     except Exception as e:
#         current_app.logger.error(traceback.format_exc())
#         return jsonify({"error": str(e)}), 500




from flask import Blueprint, request, jsonify, g, current_app
from sqlalchemy import text
from app.middleware import tenant_resolver
from app.services.db_manager import get_tenant_engine, initialize_full_tenant_schema
import traceback

# -----------------------------------
# Blueprint setup
# -----------------------------------
tenant_bp = Blueprint("tenant", __name__)

# -----------------------------------
# Tenant Pre-Request Middleware
# -----------------------------------
@tenant_bp.before_request
def before_tenant_request():
    """Resolve tenant before processing any tenant route."""
    if request.method == "OPTIONS":
        # Handle CORS preflight
        return "", 200

    response = tenant_resolver()
    if response is not None:
        return response


# -----------------------------------
# Get Tenant Metadata
# -----------------------------------
@tenant_bp.route("/meta", methods=["GET"])
def tenant_meta():
    """Fetch metadata for the resolved tenant."""
    tenant = getattr(g, "tenant", None)
    if tenant is None:
        return jsonify({"error": "Tenant not resolved"}), 400

    return jsonify({"tenant": tenant.to_dict()}), 200


# -----------------------------------
# Subscribe Tenant to a Module
# -----------------------------------
@tenant_bp.route("/subscribe", methods=["POST"])
def subscribe_to_module():
    """
    Subscribes the current tenant to a module and ensures tenant schema exists.
    """
    try:
        tenant = getattr(g, "tenant", None)
        if tenant is None:
            return jsonify({"error": "Tenant not resolved"}), 400

        data = request.get_json() or {}
        module_name = data.get("module") or data.get("module_name")

        if not module_name:
            return jsonify({"error": "Module name is required"}), 400

        # ✅ Get tenant DB engine
        engine = get_tenant_engine(tenant)

        # ✅ Ensure tenant schema and tables exist
        tenant_db_uri = str(engine.url)
        initialize_full_tenant_schema(tenant_db_uri)

        with engine.begin() as conn:
            # Create subscriptions table if missing
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id SERIAL PRIMARY KEY,
                    module_name VARCHAR(100) UNIQUE,
                    subscribed_on TIMESTAMP DEFAULT NOW()
                );
            """))

            # Check if already subscribed
            existing = conn.execute(
                text("SELECT module_name FROM subscriptions WHERE module_name = :m"),
                {"m": module_name}
            ).fetchone()

            if existing:
                return jsonify({"message": f"Already subscribed to '{module_name}'"}), 200

            # Insert new subscription
            conn.execute(
                text("INSERT INTO subscriptions (module_name) VALUES (:m)"),
                {"m": module_name}
            )

        current_app.logger.info(
            f"✅ Tenant '{tenant.subdomain}' subscribed to module '{module_name}'"
        )

        return jsonify({"message": f"Subscribed to '{module_name}' successfully!"}), 200

    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


# -----------------------------------
# Get All Subscriptions for Tenant
# -----------------------------------
@tenant_bp.route("/subscriptions", methods=["GET"])
def get_subscriptions():
    """Return all modules the current tenant is subscribed to."""
    try:
        tenant = getattr(g, "tenant", None)
        if tenant is None:
            return jsonify({"error": "Tenant not resolved"}), 400

        engine = get_tenant_engine(tenant)

        with engine.begin() as conn:
            # Ensure subscriptions table exists
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id SERIAL PRIMARY KEY,
                    module_name VARCHAR(100) UNIQUE,
                    subscribed_on TIMESTAMP DEFAULT NOW()
                );
            """))

            result = conn.execute(text("SELECT module_name FROM subscriptions"))
            modules = [row[0] for row in result]

        return jsonify({"subscribed": {m: True for m in modules}}), 200

    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
