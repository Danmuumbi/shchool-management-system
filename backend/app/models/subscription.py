# backend/app/models/subscription.py

from app.models.tenant_base import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    module_name = Column(String(100), nullable=False)
    subscribed_on = Column(DateTime, server_default=func.now())
