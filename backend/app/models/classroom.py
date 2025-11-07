# backend/app/models/classroom.py
from sqlalchemy import Column, Integer, String
from app.models.tenant_base import Base

class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    grade = Column(String(20))
    class_teacher = Column(String(100), nullable=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "grade": self.grade, "class_teacher": self.class_teacher}
