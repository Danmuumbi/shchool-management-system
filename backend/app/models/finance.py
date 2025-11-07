# backend/app/models/finance.py
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.models.tenant_base import Base

class FeeStructure(Base):
    __tablename__ = "fee_structures"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)           # e.g., "Term 1 Fees", "Tuition - Grade 1"
    description = Column(Text)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), default="KES")
    applicable_class_id = Column(Integer, nullable=True) # optionally link to classroom id
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "description": self.description,
            "amount": float(self.amount), "currency": self.currency,
            "applicable_class_id": self.applicable_class_id, "is_active": self.is_active
        }

class PaymentRecord(Base):
    __tablename__ = "payment_records"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, nullable=True)          # FK to students.id (optional; tenant DB enforces)
    fee_structure_id = Column(Integer, ForeignKey("fee_structures.id", ondelete="SET NULL"))
    reference = Column(String(120), unique=True, nullable=False)  # payment reference
    amount = Column(Numeric(12, 2), nullable=False)
    payment_method = Column(String(50), nullable=True)  # e.g., M-PESA, PayPal, Cash
    paid_on = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default="completed")    # pending, completed, failed
    notes = Column(Text)

    def to_dict(self):
        return {
            "id": self.id, "student_id": self.student_id, "fee_structure_id": self.fee_structure_id,
            "reference": self.reference, "amount": float(self.amount), "payment_method": self.payment_method,
            "paid_on": self.paid_on.isoformat() if self.paid_on else None, "status": self.status
        }
