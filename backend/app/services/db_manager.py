

import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
from app.models.tenant_base import Base, User
import psycopg2
from urllib.parse import urlparse

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CENTRAL_DB_URI = os.getenv("CENTRAL_DB_URI") or os.getenv("CENTRAL_DB_URI")  # fallback


def create_tenant_database(db_admin_uri, tenant_db_name):
    """Create a new PostgreSQL database using an admin connection string."""
    url = urlparse(db_admin_uri)
    conn = psycopg2.connect(db_admin_uri)
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(f"CREATE DATABASE {tenant_db_name};")
        logger.info(f"✅ Created tenant database: {tenant_db_name}")
    except psycopg2.errors.DuplicateDatabase:
        logger.info(f"⚠️ Database {tenant_db_name} already exists, skipping creation.")
    finally:
        cur.close()
        conn.close()


def create_tenant_tables(tenant_db_uri):
    """Use SQLAlchemy Base.metadata.create_all to create tenant tables."""
    engine = create_engine(tenant_db_uri)

    try:
        Base.metadata.create_all(engine)
        logger.info("✅ Base SQLAlchemy tables created successfully.")
    except ProgrammingError as e:
        logger.error(f"Error creating ORM tables: {e}")

    with engine.connect() as conn:
        logger.info(f"📦 Initializing default tables for tenant DB: {tenant_db_uri}")
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS school_profile (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                motto TEXT,
                about TEXT,
                email VARCHAR(255),
                phone VARCHAR(100),
                color VARCHAR(50),
                logo_url TEXT,
                hero_url TEXT
            );
        """))
        logger.info("✅ Default table 'school_profile' created (if not exists).")

    engine.dispose()


def tenant_db_uri_from_parts(host, port, db_name, user, password):
    """Build tenant DB URI dynamically."""
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_tenant_engine(tenant):
    """Return SQLAlchemy engine for a specific tenant."""
    uri = tenant_db_uri_from_parts(
        tenant.db_host,
        tenant.db_port,
        tenant.db_name,
        tenant.db_user,
        tenant.db_password,
    )
    return create_engine(uri)





# backend/app/services/db_manager.py
from app.models.module_registry import *  # imports all modules
def initialize_full_tenant_schema(tenant_db_uri):
    """
    Creates all module tables for a new tenant by loading the module registry.
    This ensures every module's models are included during database creation.
    """

    engine = create_engine(tenant_db_uri)

    try:
        Base.metadata.create_all(engine)
        logger.info("✅ Full tenant schema initialized successfully (all modules).")
    except ProgrammingError as e:
        logger.error(f"❌ Error creating full tenant schema: {e}")
    finally:
        engine.dispose()



from sqlalchemy.orm import sessionmaker
# backend/app/services/db_manager.py

from sqlalchemy.orm import sessionmaker
from app.extensions import db
from app.models.central import Tenant  # ✅ Make sure this file exists and defines Tenant

def get_tenant_session(tenant):
    """
    Returns a SQLAlchemy session bound to the tenant's specific database.
    Can accept either a Tenant object or a subdomain (string).
    """
    # ✅ If tenant is a string, fetch the tenant record from the central DB
    if isinstance(tenant, str):
        central_session = db.session
        tenant_obj = central_session.query(Tenant).filter_by(subdomain=tenant).first()
        if not tenant_obj:
            raise Exception(f"Tenant '{tenant}' not found in central database.")
        tenant = tenant_obj

    # ✅ Now it's a proper tenant object
    engine = get_tenant_engine(tenant)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()
