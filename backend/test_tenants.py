from app.app import create_app
from app.extensions import db
from app.models.central import Tenant
from app.services.db_manager import get_tenant_session
from sqlalchemy import text

app = create_app()
app.app_context().push()

for subdomain in ["evol", "evol1"]:
    tenant = db.session.query(Tenant).filter_by(subdomain=subdomain).first()
    session = get_tenant_session(tenant)

    print(f"\n📂 Tables in {tenant.db_name}:")
    result = session.execute(text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='public';
    """)).fetchall()
    print([r[0] for r in result])

    print(f"📑 Columns in 'teachers' table ({tenant.db_name}):")
    columns = session.execute(text("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='teachers';
    """)).fetchall()
    print([c[0] for c in columns])
