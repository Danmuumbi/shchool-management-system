

import sqlite3, os
from flask_mail import Message
from werkzeug.security import generate_password_hash
from flask import current_app
from app.extensions import db  # ✅ db lives here
from app.models.central import Tenant
from sqlalchemy import create_engine
from app.services.db_manager import tenant_db_uri_from_parts  # ✅ This line is crucial





def create_school_database(school_id):
    """Creates a separate database for each school."""
    db_path = f"instance/school_{school_id}.db"
    if not os.path.exists('instance'):
        os.makedirs('instance')
    conn = sqlite3.connect(db_path)
    conn.execute('CREATE TABLE IF NOT EXISTS example_table (id INTEGER PRIMARY KEY, data TEXT)')
    conn.close()
    return db_path


def send_welcome_email(mail, recipient, subdomain):
    """Send welcome email after school registration."""
    msg = Message(
        "Welcome to EvolTechs School System",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[recipient],
    )
    msg.html = f"""
    <h3>Welcome!</h3>
    <p>Your school subdomain: <b>{subdomain}.evoltechs.top</b></p>
    <p>You can now log in and begin setup.</p>
    """
    mail.send(msg)


def get_tenant_engine(subdomain):
    """
    Returns a SQLAlchemy engine connected to the tenant's actual database.
    Example:
      - subdomain: evol
      - db_name in central: evol_evoltechs_central
      => connects to that DB directly
    """
    tenant = Tenant.query.filter_by(subdomain=subdomain).first()
    if not tenant:
        raise ValueError(f"❌ Tenant '{subdomain}' not found in central database.")

    # ✅ Build the real tenant DB URI
    tenant_uri = tenant_db_uri_from_parts(
        tenant.db_host,
        tenant.db_port,
        tenant.db_name,
        tenant.db_user,
        tenant.db_password
    )

    print(f"✅ Connecting to tenant DB: {tenant_uri}")  # optional debug
    return create_engine(tenant_uri)
