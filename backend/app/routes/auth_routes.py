# from flask import Blueprint, request, jsonify, current_app
# from app.extensions import db
# from app.models.central import Tenant
# from app.services.db_manager import create_tenant_database, create_tenant_tables, tenant_db_uri_from_parts
# from sqlalchemy import create_engine, text
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_jwt_extended import create_access_token
# from urllib.parse import urlparse
# from datetime import timedelta
# import smtplib, ssl

# auth_bp = Blueprint("auth", __name__)

# # ----------------------
# # EMAIL FUNCTION
# # ----------------------
# def send_welcome_email(to_email, school_name, login_url):
#     """Send a welcome email when a new school is registered."""
#     smtp_host = current_app.config['SMTP_HOST']
#     smtp_port = current_app.config['SMTP_PORT']
#     smtp_user = current_app.config['SMTP_USER']
#     smtp_pass = current_app.config['SMTP_PASS']

#     subject = f"Welcome to EvolTechs - {school_name}"
#     body = f"Your school '{school_name}' has been created successfully.\n\nLogin at: {login_url}"
#     message = f"Subject: {subject}\n\n{body}"

#     context = ssl.create_default_context()
#     try:
#         with smtplib.SMTP(smtp_host, smtp_port) as server:
#             server.starttls(context=context)
#             server.login(smtp_user, smtp_pass)
#             server.sendmail(smtp_user, to_email, message)
#     except Exception as e:
#         current_app.logger.warning(f"Failed to send email to {to_email}: {e}")




# # ----------------------
# # SCHOOL REGISTRATION
# # ----------------------
# @auth_bp.route("/register", methods=["POST"])
# def register_school():
#     """Register a new school and create its tenant database."""
#     from app.services.db_manager import initialize_full_tenant_schema  # ✅ import here

#     data = request.get_json()
#     school_name = data.get("school_name")
#     subdomain = data.get("subdomain", "").lower().strip()
#     admin_email = data.get("admin_email")
#     admin_password = data.get("admin_password")
#     primary_color = data.get("primary_color") or "#0066cc"

#     # Validate input
#     if not school_name or not subdomain or not admin_email or not admin_password:
#         return jsonify({"error": "Missing required fields"}), 400

#     # Check if subdomain already exists
#     if Tenant.query.filter_by(subdomain=subdomain).first():
#         return jsonify({"error": "Subdomain already taken"}), 400

#     db_name = f"evoltechs_{subdomain}"

#     # ✅ Create tenant DB
#     central_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
#     create_tenant_database(central_uri, db_name)

#     # Extract DB details
#     parsed = urlparse(central_uri)
#     db_host = parsed.hostname or "localhost"
#     db_port = parsed.port or 5432
#     db_user = parsed.username
#     db_password = parsed.password

#     # ✅ Save tenant in central database
#     tenant = Tenant(
#         name=school_name,
#         subdomain=subdomain,
#         db_name=db_name,
#         db_host=db_host,
#         db_port=db_port,
#         db_user=db_user,
#         db_password=db_password,
#         status="trial",
#         plan="free",
#         features={"core": True},
#         theme={"primary": primary_color}
#     )

#     db.session.add(tenant)
#     db.session.commit()

#     # ✅ Build tenant DB URI
#     tenant_db_uri = tenant_db_uri_from_parts(db_host, db_port, db_name, db_user, db_password)

#     # ✅ Initialize all module and default tables automatically
#     initialize_full_tenant_schema(tenant_db_uri)

#     # ✅ Insert admin user into tenant's users table
#     engine = create_engine(tenant_db_uri)
#     with engine.connect() as conn:
#         hashed = generate_password_hash(admin_password)
#         conn.execute(
#             text("INSERT INTO users (email, password_hash, role) VALUES (:email, :password_hash, :role)"),
#             {"email": admin_email, "password_hash": hashed, "role": "admin"}
#         )
#         conn.commit()
#     engine.dispose()

#     # ✅ Send welcome email
#     login_url = f"http://{subdomain}.localhost:3000/login"
#     send_welcome_email(admin_email, school_name, login_url)

#     return jsonify({
#         "message": "School registered successfully. Check your email to login.",
#         "login_url": login_url
#     }), 201

# # ----------------------
# # LOGIN
# # ----------------------
# @auth_bp.route("/login", methods=["POST"])
# def login():
#     """Login to a tenant school."""
#     data = request.get_json()
#     subdomain = data.get("subdomain")
#     email = data.get("email")
#     password = data.get("password")

#     # Validate tenant
#     tenant = Tenant.query.filter_by(subdomain=subdomain).first()
#     if not tenant:
#         return jsonify({"error": "School not found"}), 404
#     if tenant.status == "suspended":
#         return jsonify({"error": "School suspended"}), 403

#     # Connect to tenant DB
#     tenant_db_uri = tenant_db_uri_from_parts(
#         tenant.db_host, tenant.db_port, tenant.db_name, tenant.db_user, tenant.db_password
#     )
#     engine = create_engine(tenant_db_uri)
#     with engine.connect() as conn:
#         row = conn.execute(
#             text("SELECT id, email, password_hash, role FROM users WHERE email = :email"),
#             {"email": email}
#         ).fetchone()

#     engine.dispose()

#     if not row:
#         return jsonify({"error": "Invalid credentials"}), 401

#     _, user_email, password_hash, role = row
#     if not check_password_hash(password_hash, password):
#         return jsonify({"error": "Invalid credentials"}), 401

#     # Generate JWT token
#     token = create_access_token(
#         identity={"email": user_email, "subdomain": subdomain, "role": role},
#         expires_delta=timedelta(days=1)
#     )

#     return jsonify({
#         "token": token,
#         "role": role,
#         "email": user_email
#     }), 200





from flask import Blueprint, request, jsonify, current_app
from app.extensions import db
from app.models.central import Tenant
from app.services.db_manager import create_tenant_database, create_tenant_tables, tenant_db_uri_from_parts
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required
)
from urllib.parse import urlparse
from datetime import timedelta
import smtplib, ssl

auth_bp = Blueprint("auth", __name__)

# ----------------------
# EMAIL FUNCTION
# ----------------------
def send_welcome_email(to_email, school_name, login_url):
    """Send a welcome email when a new school is registered."""
    smtp_host = current_app.config['SMTP_HOST']
    smtp_port = current_app.config['SMTP_PORT']
    smtp_user = current_app.config['SMTP_USER']
    smtp_pass = current_app.config['SMTP_PASS']

    subject = f"Welcome to EvolTechs - {school_name}"
    body = f"Your school '{school_name}' has been created successfully.\n\nLogin at: {login_url}"
    message = f"Subject: {subject}\n\n{body}"

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls(context=context)
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, to_email, message)
    except Exception as e:
        current_app.logger.warning(f"Failed to send email to {to_email}: {e}")


# ----------------------
# SCHOOL REGISTRATION
# ----------------------
@auth_bp.route("/register", methods=["POST"])
def register_school():
    """Register a new school and create its tenant database."""
    from app.services.db_manager import initialize_full_tenant_schema  # ✅ import here

    data = request.get_json()
    school_name = data.get("school_name")
    subdomain = data.get("subdomain", "").lower().strip()
    admin_email = data.get("admin_email")
    admin_password = data.get("admin_password")
    primary_color = data.get("primary_color") or "#0066cc"

    # Validate input
    if not school_name or not subdomain or not admin_email or not admin_password:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if subdomain already exists
    if Tenant.query.filter_by(subdomain=subdomain).first():
        return jsonify({"error": "Subdomain already taken"}), 400

    db_name = f"evoltechs_{subdomain}"

    # ✅ Create tenant DB
    central_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
    create_tenant_database(central_uri, db_name)

    # Extract DB details
    parsed = urlparse(central_uri)
    db_host = parsed.hostname or "localhost"
    db_port = parsed.port or 5432
    db_user = parsed.username
    db_password = parsed.password

    # ✅ Save tenant in central database
    tenant = Tenant(
        name=school_name,
        subdomain=subdomain,
        db_name=db_name,
        db_host=db_host,
        db_port=db_port,
        db_user=db_user,
        db_password=db_password,
        status="trial",
        plan="free",
        features={"core": True},
        theme={"primary": primary_color}
    )

    db.session.add(tenant)
    db.session.commit()

    # ✅ Build tenant DB URI
    tenant_db_uri = tenant_db_uri_from_parts(db_host, db_port, db_name, db_user, db_password)

    # ✅ Initialize all module and default tables automatically
    initialize_full_tenant_schema(tenant_db_uri)

    # ✅ Insert admin user into tenant's users table
    engine = create_engine(tenant_db_uri)
    with engine.connect() as conn:
        hashed = generate_password_hash(admin_password)
        conn.execute(
            text("INSERT INTO users (email, password_hash, role) VALUES (:email, :password_hash, :role)"),
            {"email": admin_email, "password_hash": hashed, "role": "admin"}
        )
        conn.commit()
    engine.dispose()

    # ✅ Send welcome email
    login_url = f"http://{subdomain}.localhost:3000/login"
    send_welcome_email(admin_email, school_name, login_url)

    return jsonify({
        "message": "School registered successfully. Check your email to login.",
        "login_url": login_url
    }), 201


# ----------------------
# LOGIN
# ----------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    """Login to a tenant school."""
    data = request.get_json()
    subdomain = data.get("subdomain")
    email = data.get("email")
    password = data.get("password")

    # Validate tenant
    tenant = Tenant.query.filter_by(subdomain=subdomain).first()
    if not tenant:
        return jsonify({"error": "School not found"}), 404
    if tenant.status == "suspended":
        return jsonify({"error": "School suspended"}), 403

    # Connect to tenant DB
    tenant_db_uri = tenant_db_uri_from_parts(
        tenant.db_host, tenant.db_port, tenant.db_name, tenant.db_user, tenant.db_password
    )
    engine = create_engine(tenant_db_uri)
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT id, email, password_hash, role FROM users WHERE email = :email"),
            {"email": email}
        ).fetchone()

    engine.dispose()

    if not row:
        return jsonify({"error": "Invalid credentials"}), 401

    _, user_email, password_hash, role = row
    if not check_password_hash(password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # ✅ Generate JWT token (fix “Subject must be a string” issue)
    token = create_access_token(
        identity=user_email,
        additional_claims={
            "subdomain": subdomain,
            "role": role
        },
        expires_delta=timedelta(days=1)
    )

    return jsonify({
        "token": token,
        "role": role,
        "email": user_email
    }), 200


# ----------------------
# VERIFY TOKEN
# ----------------------
@auth_bp.route("/verify", methods=["GET"])
@jwt_required()
def verify_token():
    """Verify a JWT token."""
    jwt_data = get_jwt()
    identity = get_jwt_identity()
    return jsonify({
        "status": "Token is valid ✅",
        "identity": identity,
        "claims": jwt_data
    }), 200
