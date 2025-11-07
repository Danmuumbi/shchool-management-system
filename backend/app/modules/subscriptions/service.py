


from datetime import datetime, timedelta
from flask import current_app
from app.extensions import db
from utils import get_tenant_engine
from app.models.teacher import Teacher
from app.models.central import Tenant

def subscribe_to_module(subdomain, module_name, plan_type="free"):
    """
    Subscribe a tenant to a specific module.
    Creates module tables in tenant DB and updates central DB.
    """
    tenant_engine = get_tenant_engine(subdomain)

    # ✅ 1. Create tables for selected module
    if module_name == "teachers":
        Teacher.metadata.create_all(bind=tenant_engine)

    # ✅ 2. Update tenant record (features)
    tenant = Tenant.query.filter_by(subdomain=subdomain).first()
    if not tenant:
        return {"error": f"Tenant with subdomain '{subdomain}' not found"}

    features = tenant.features or {}
    features[module_name] = {
        "subscribed": True,
        "plan_type": plan_type,
        "subscribed_at": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + timedelta(days=120)).isoformat()
    }
    tenant.features = features
    db.session.commit()

    return {"message": f"Subscribed to {module_name} successfully!"}
