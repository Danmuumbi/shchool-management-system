# upgrade_existing_tenants.py

from app.app import create_app
from app.extensions import db
from app.models.central import Tenant
from app.services.db_manager import get_tenant_session
from app.models import tenant_base
from sqlalchemy import text, inspect

app = create_app()
app.app_context().push()

# Fetch all tenants
tenants = db.session.query(Tenant).all()

for tenant in tenants:
    print(f"\n🔧 Upgrading database: {tenant.db_name}")

    session = get_tenant_session(tenant)
    engine = session.get_bind()
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    # --- Drop old teachers table with dependencies ---
    if "teachers" in existing_tables:
        print(f"🧹 Forcing drop of 'teachers' table (and dependents) in {tenant.db_name}...")
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE teachers CASCADE;"))
            conn.commit()

    # --- Recreate all missing tables ---
    print(f"🆕 Recreating missing tables in {tenant.db_name}...")
    tenant_base.Base.metadata.create_all(engine)

    print(f"✅ Database '{tenant.db_name}' upgraded successfully!")

print("\n🎯 All tenant databases upgraded with latest table definitions!")
