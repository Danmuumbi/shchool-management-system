

# backend/app/models/teacher.py
from sqlalchemy import (
    Column, Integer, String, Text, Date, Boolean, Table, ForeignKey
)
from app.models.tenant_base import Base

# many-to-many association table between teachers and subjects
teacher_subjects = Table(
    "teacher_subjects",
    Base.metadata,
    Column("teacher_id", Integer, ForeignKey("teachers.id", ondelete="CASCADE")),
    Column("subject_id", Integer, ForeignKey("subjects.id", ondelete="CASCADE"))
)

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    teacher_number = Column(String(50), unique=True, nullable=False)  # e.g. TSC number (Kenya)
    national_id = Column(String(20), unique=True, nullable=True)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    qualification = Column(String(255), nullable=True)
    profile_picture = Column(String(255), nullable=True)
    date_joined = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    created_by = Column(String(100), nullable=True)  # admin who created record

    # Note: we define association table above. Relationship() is not required
    # for table creation; we can add ORM relationships later if desired.

    def full_name(self):
        return f"{self.first_name} {self.middle_name or ''} {self.last_name}".strip()

    def to_dict(self):
        return {
            "id": self.id,
            "teacher_number": self.teacher_number,
            "national_id": self.national_id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "qualification": self.qualification,
            "profile_picture": self.profile_picture,
            "date_joined": self.date_joined.isoformat() if self.date_joined else None,
            "is_active": self.is_active,
            "created_by": self.created_by,
        }
