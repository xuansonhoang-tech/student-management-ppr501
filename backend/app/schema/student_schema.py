from typing import Optional
from pydantic import BaseModel

class CreateStudent(BaseModel):
    student_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    dob: Optional[str] = None
    hometown: Optional[str] = None
    math_score: Optional[float] = None
    literature_score: Optional[float] = None
    english_score: Optional[float] = None
    
class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    dob: Optional[str] = None
    hometown: Optional[str] = None
    math_score: Optional[float] = None
    literature_score: Optional[float] = None
    english_score: Optional[float] = None


class StudentResponse(CreateStudent):
    pass