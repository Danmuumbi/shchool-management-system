# backend/init_existing_tenants.py

from flask import Flask
from app.extensions import db
from app.models.central import Tenant
from app.services.db_manager import initialize_full_tenant_schema, tenant_db_uri_from_parts
from config import Config  # ✅ adjust if your config file name is different

# ✅ Create a minimal Flask app context
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    tenants = Tenant.query.all()
    print(f"🧩 Found {len(tenants)} tenants.")

    for tenant in tenants:
        print(f"➡️ Initializing schema for: {tenant.name} ({tenant.subdomain})")
        tenant_db_uri = tenant_db_uri_from_parts(
            tenant.db_host,
            tenant.db_port,
            tenant.db_name,
            tenant.db_user,
            tenant.db_password,
        )
        initialize_full_tenant_schema(tenant_db_uri)

    print("✅ All existing tenants initialized successfully!")
