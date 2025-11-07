# backend/app/models/academic.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func
from app.models.tenant_base import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    code = Column(String(30), unique=True, nullable=False)  # e.g., "ENG-101"
    name = Column(String(120), nullable=False)
    description = Column(Text)

    def to_dict(self):
        return {"id": self.id, "code": self.code, "name": self.name, "description": self.description}


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)               # e.g., "Term 1 Exams"
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"))
    class_id = Column(Integer, nullable=True)                # classroom id (optional)
    max_marks = Column(Numeric(8,2), default=100)
    date = Column(DateTime)
    created_on = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "subject_id": self.subject_id,
            "class_id": self.class_id, "max_marks": float(self.max_marks),
            "date": self.date.isoformat() if self.date else None
        }


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey("exams.id", ondelete="CASCADE"))
    student_id = Column(Integer, nullable=False)  # link to students.id
    marks_obtained = Column(Numeric(8,2), nullable=False)
    grade = Column(String(10), nullable=True)     # e.g., A, B+, C-
    remarks = Column(Text)

    def to_dict(self):
        return {
            "id": self.id, "exam_id": self.exam_id, "student_id": self.student_id,
            "marks_obtained": float(self.marks_obtained), "grade": self.grade, "remarks": self.remarks
        }
