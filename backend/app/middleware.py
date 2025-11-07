

from flask import request, g, jsonify, current_app
from sqlalchemy import create_engine
from app.models.central import Tenant
from app.extensions import db
from app.services.db_manager import tenant_db_uri_from_parts


def get_subdomain_from_request() -> str | None:
    """
    Determine the tenant subdomain from:
    1️⃣  X-Tenant header (preferred for API calls)
    2️⃣  Host header for browser-based requests

    Examples:
      - evol.localhost:3000 -> evol
      - greenschool.evoltechs.top -> greenschool
    """
    # Priority 1: Custom header
    if "X-Tenant" in request.headers:
        header_subdomain = request.headers.get("X-Tenant", "").strip().lower()
        if header_subdomain:
            return header_subdomain

    # Priority 2: Host header
    host = request.headers.get("Host", "").split(":")[0]
    parts = host.split(".")

    # Localhost style e.g. evol.localhost
    if "localhost" in host:
        if host != "localhost" and len(parts) > 1:
            return parts[0]
        return None

    # Production domain e.g. greenschool.evoltechs.top
    if len(parts) >= 3:
        return parts[0]

    return None


def tenant_resolver():
    """
    Middleware that resolves the tenant before each request.
    It attaches tenant info and a database engine to flask.g.
    Should be registered via app.before_request().
    """
    subdomain = get_subdomain_from_request()

    if not subdomain:
        current_app.logger.warning("❌ Tenant subdomain missing in request.")
        return jsonify({"error": "Tenant subdomain missing"}), 400

    tenant = Tenant.query.filter_by(subdomain=subdomain).first()

    if not tenant:
        current_app.logger.warning(f"❌ Tenant not found: {subdomain}")
        return jsonify({"error": f"Tenant '{subdomain}' not found"}), 404

    if tenant.status == "suspended":
        current_app.logger.warning(f"🚫 Tenant '{subdomain}' suspended.")
        return jsonify({"error": "Tenant suspended. Contact support."}), 403

    # ✅ Build the tenant-specific DB URI
    tenant_db_uri = tenant_db_uri_from_parts(
        tenant.db_host,
        tenant.db_port,
        tenant.db_name,
        tenant.db_user,
        tenant.db_password
    )

    # ✅ Store in request context (available for the entire request)
    g.tenant = tenant
    g.tenant_db_uri = tenant_db_uri
    g.tenant_engine = create_engine(tenant_db_uri, pool_pre_ping=True)

    current_app.logger.info(f"✅ Tenant resolved: {tenant.name} ({tenant.subdomain})")
