# backend/app/models/timetable.py
from sqlalchemy import Column, Integer, String, Time, ForeignKey, Date
from app.models.tenant_base import Base

class Timetable(Base):
    __tablename__ = "timetable"

    id = Column(Integer, primary_key=True)
    day_of_week = Column(String(20), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"))
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"))
    classroom_id = Column(Integer, ForeignKey("classrooms.id", ondelete="CASCADE"))
    created_on = Column(Date)

    def to_dict(self):
        return {
            "id": self.id,
            "day_of_week": self.day_of_week,
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
            "subject_id": self.subject_id,
            "teacher_id": self.teacher_id,
            "classroom_id": self.classroom_id,
        }
