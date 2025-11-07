from sqlalchemy.dialects.postgresql import JSONB
from app.extensions import db
from datetime import datetime

class Tenant(db.Model):
    __tablename__ = "tenants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    subdomain = db.Column(db.String(100), unique=True, nullable=False)  # e.g. greenschool
    db_name = db.Column(db.String(255), nullable=False)
    db_host = db.Column(db.String(255), nullable=False, default='localhost')
    db_port = db.Column(db.Integer, nullable=False, default=5432)
    db_user = db.Column(db.String(255), nullable=False)
    db_password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='trial')  # trial, active, suspended
    plan = db.Column(db.String(50), default='free')  # free, pro, premium
    features = db.Column(JSONB, default={})
    theme = db.Column(JSONB, default={})  # e.g. {"primary":"#0066cc","logo":"/uploads/logo.png"}
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "subdomain": self.subdomain,
            "status": self.status,
            "plan": self.plan,
            "features": self.features or {},
            "theme": self.theme or {},
        }
