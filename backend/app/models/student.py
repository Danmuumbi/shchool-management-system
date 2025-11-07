# backend/app/models/student.py
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from app.models.tenant_base import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    admission_number = Column(String(50), unique=True, nullable=False)
    national_id = Column(String(20), nullable=True)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    last_name = Column(String(100), nullable=False)
    gender = Column(String(10))
    date_of_birth = Column(Date)
    class_id = Column(Integer, ForeignKey("classrooms.id", ondelete="SET NULL"))
    guardian_name = Column(String(120))
    guardian_phone = Column(String(20))
    guardian_email = Column(String(120))
    address = Column(String(255))
    admission_date = Column(Date)
    profile_picture = Column(String(255))
    is_active = Column(Boolean, default=True)

    def full_name(self):
        return f"{self.first_name} {self.middle_name or ''} {self.last_name}".strip()

    def to_dict(self):
        return {
            "id": self.id,
            "admission_number": self.admission_number,
            "national_id": self.national_id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "class_id": self.class_id,
            "guardian_name": self.guardian_name,
            "guardian_phone": self.guardian_phone,
            "guardian_email": self.guardian_email,
            "address": self.address,
            "admission_date": self.admission_date.isoformat() if self.admission_date else None,
            "profile_picture": self.profile_picture,
            "is_active": self.is_active,
        }
