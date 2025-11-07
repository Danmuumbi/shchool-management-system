# backend/app/models/library.py
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.models.tenant_base import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    isbn = Column(String(30), unique=True, nullable=True)
    title = Column(String(255), nullable=False)
    author = Column(String(200))
    publisher = Column(String(200))
    year = Column(String(10))
    copies_total = Column(Integer, default=1)
    copies_available = Column(Integer, default=1)
    category = Column(String(100))
    description = Column(Text)

    def to_dict(self):
        return {
            "id": self.id, "isbn": self.isbn, "title": self.title, "author": self.author,
            "publisher": self.publisher, "year": self.year, "copies_total": self.copies_total,
            "copies_available": self.copies_available, "category": self.category
        }

class BorrowLog(Base):
    __tablename__ = "borrow_logs"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="SET NULL"))
    student_id = Column(Integer, nullable=True)   # link to students.id
    borrowed_on = Column(DateTime(timezone=True), server_default=func.now())
    due_on = Column(DateTime)
    returned_on = Column(DateTime, nullable=True)
    status = Column(String(50), default="borrowed")  # borrowed, returned, overdue
    fine_amount = Column(Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id, "book_id": self.book_id, "student_id": self.student_id,
            "borrowed_on": self.borrowed_on.isoformat() if self.borrowed_on else None,
            "due_on": self.due_on.isoformat() if self.due_on else None,
            "returned_on": self.returned_on.isoformat() if self.returned_on else None,
            "status": self.status, "fine_amount": self.fine_amount
        }
