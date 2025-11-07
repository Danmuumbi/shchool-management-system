# backend/app/models/module_registry.py
"""
Registry that imports all tenant models so that Base.metadata.create_all()
discovers them during tenant schema initialization.
"""

# Core entity models
from app.models.tenant_base import Base  # ensures Base is defined
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.classroom import Classroom
from app.models.timetable import Timetable

# Academic
# from app.models.subject import Subject 
from app.models.academic import Exam, Grade  # academic module (also contains Subject if you prefer)

# Finance
from app.models.finance import FeeStructure, PaymentRecord

# Library
from app.models.library import Book, BorrowLog

# Subscription & profile (central to tenant functionality)
from app.models.subscription import Subscription

# Export names (optional)
__all__ = [
    "Teacher", "Student", "Classroom", "Timetable",
     "Exam", "Grade",
    "FeeStructure", "PaymentRecord",
    "Book", "BorrowLog",
    "Subscription"
]
