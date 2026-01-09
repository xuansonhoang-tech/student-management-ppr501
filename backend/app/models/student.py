from sqlalchemy import Column, String, Float, Date
from app.core.database import Base

class StudentModel(Base):
    __tablename__ = "students"

    student_id = Column(String, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True)
    dob = Column(Date)
    hometown = Column(String(100))

    math_score = Column(Float)
    literature_score = Column(Float)
    english_score = Column(Float)
