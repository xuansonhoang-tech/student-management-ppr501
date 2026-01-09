from app.models.student import StudentModel
from app.models.student_model import StudentModel as Student
from datetime import datetime

def to_entity(domain: Student) -> StudentModel:
    dob = None
    if domain.dob:
        try:
            dob = datetime.strptime(domain.dob, '%d/%m/%Y').date()
        except (ValueError, TypeError):
            try:
                dob = datetime.strptime(domain.dob, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                dob = None
    
    return StudentModel(
        student_id=domain.student_id,
        first_name=domain.first_name,
        last_name=domain.last_name,
        email=domain.email,
        dob=dob,
        hometown=domain.hometown,
        math_score=domain.math_score,
        literature_score=domain.literature_score,
        english_score=domain.english_score,
    )

def to_domain(entity: StudentModel) -> Student:
    return Student(
        student_id=entity.student_id,
        first_name=entity.first_name,
        last_name=entity.last_name,
        email=entity.email,
        dob=str(entity.dob) if entity.dob else None,
        hometown=entity.hometown,
        math_score=entity.math_score,
        literature_score=entity.literature_score,
        english_score=entity.english_score,
    )
