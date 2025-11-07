# app/services/tenant_session.py
from app.services.db_manager import tenant_db_uri_from_parts
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_tenant_session(tenant):
    """
    Returns a SQLAlchemy session for the given tenant object.
    Assumes the tenant has db_host, db_port, db_name, db_user, db_password attributes.
    """
    uri = tenant_db_uri_from_parts(
        tenant.db_host,
        tenant.db_port,
        tenant.db_name,
        tenant.db_user,
        tenant.db_password,
    )
    engine = create_engine(uri)
    Session = sessionmaker(bind=engine)
    return Session()
