# import os
# import psycopg2
# from sqlalchemy import create_engine, text
# from app.services.db_manager import create_tenant_tables, tenant_db_uri_from_parts

# # ✅ Configuration
# CENTRAL_DB_URI = os.getenv("CENTRAL_DB_URI") or "postgresql://postgres:%40Mmuuo2015@localhost:5432/evoltechs_central"

# # Database connection details (used for building tenant URIs)
# host = "localhost"
# port = 5432
# user = "postgres"
# password = "%40Mmuuo2015"  # adjust if you changed it

# def fetch_tenant_dbs():
#     """
#     Fetch all tenant database names from the central DB 'schools' table.
#     """
#     print("🔍 Connecting to central database to fetch tenants...")
#     conn = psycopg2.connect(CENTRAL_DB_URI)
#     cur = conn.cursor()
#     cur.execute("SELECT db_name FROM tenants;")

#     tenants = [row[0] for row in cur.fetchall()]
#     cur.close()
#     conn.close()
#     return tenants

# def sync_tenant_databases():
#     """
#     Create tables for all tenant databases listed in the central DB.
#     """
#     tenants = fetch_tenant_dbs()
#     if not tenants:
#         print("⚠️ No tenants found in central DB. Nothing to sync.")
#         return

#     for db_name in tenants:
#         uri = tenant_db_uri_from_parts(host, port, db_name, user, password)
#         print(f"🛠️ Creating tables for {db_name} ...")
#         create_tenant_tables(uri)
#         print(f"✅ Done for {db_name}\n")

# if __name__ == "__main__":
#     sync_tenant_databases()



import os
import psycopg2
from sqlalchemy import create_engine
from app.models.tenant_base import Base  # ✅ Import Base from correct file
from app.models.teacher import Teacher   # ✅ Import your model(s) so they are registered
from app.services.db_manager import tenant_db_uri_from_parts

# ✅ Configuration
CENTRAL_DB_URI = os.getenv("CENTRAL_DB_URI") or "postgresql://postgres:%40Mmuuo2015@localhost:5432/evoltechs_central"

# Database connection details (used for building tenant URIs)
host = "localhost"
port = 5432
user = "postgres"
password = "%40Mmuuo2015"  # Adjust if changed


def fetch_tenant_dbs():
    """
    Fetch all tenant database names from the central DB 'tenants' table.
    """
    print("🔍 Connecting to central database to fetch tenants...")
    conn = psycopg2.connect(CENTRAL_DB_URI)
    cur = conn.cursor()
    cur.execute("SELECT db_name FROM tenants;")
    tenants = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return tenants


def create_all_tenant_tables(uri):
    """
    Create all tables defined in app.models.tenant_base.Base for the given tenant DB.
    """
    engine = create_engine(uri)
    print(f"📦 Creating all tables for tenant DB: {uri}")
    Base.metadata.create_all(engine)
    print("✅ All tables created successfully.\n")


def sync_tenant_databases():
    """
    Go through all tenants and create their tables.
    """
    tenants = fetch_tenant_dbs()
    if not tenants:
        print("⚠️ No tenants found in central DB. Nothing to sync.")
        return

    for db_name in tenants:
        uri = tenant_db_uri_from_parts(host, port, db_name, user, password)
        print(f"🛠️ Creating tables for {db_name} ...")
        create_all_tenant_tables(uri)
        print(f"✅ Done for {db_name}\n")


if __name__ == "__main__":
    sync_tenant_databases()
