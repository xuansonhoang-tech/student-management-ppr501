import csv
from pathlib import Path
from typing import List, Callable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.student import StudentModel as StudentEntity
from app.models.student_model import StudentModel
from app.models.base_model import BaseResponse
from app.mapper.student_mapping import to_entity, to_domain
from app.models.request_params import request_params

DATA_FILE = Path('app/seeds/students.csv')

class StudentRepository():
    
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self.session_factory = session_factory
    
    async def load_students(self) -> BaseResponse[StudentModel]:
        students: List[StudentModel] = []
        try:
            with DATA_FILE.open(mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:  
                    student = StudentModel(
                        student_id=row['student_id'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        email=row['email'],
                        dob=row['date_of_birth'],
                        hometown=row['hometown'],
                        math_score=float(row['math_score']),
                        literature_score=float(row['literature_score'])
                    )
                    students.append(student)
            return BaseResponse(success=True, data=students)
        except Exception as e:
            return BaseResponse(success=False, error=[str(e)])

    async def insert_students(self, students: List[StudentModel]) -> BaseResponse[StudentModel]:
        res = BaseResponse[StudentModel](success=True)
        data_students = students
        try: 
            async with self.session_factory() as session:
                for student in data_students:
                    session.add(to_entity(student))
                await session.commit()
        except Exception as e:
            res.success = False
            res.error = [str(e)]
        return res
    
    async def create_student(self, student: StudentModel) -> BaseResponse[StudentModel]:
        res = BaseResponse[StudentModel](success=True)
        try: 
            async with self.session_factory() as session:
                session.add(to_entity(student))
                await session.commit()
                created_student = await session.get(StudentEntity, student.student_id)
                if created_student:
                    res.data = [to_domain(created_student)]
        except Exception as e:
            res.success = False
            res.error = [str(e)]
        return res  
    
    async def test_inject(self) -> str:
        return "Dependency Injection Works!"
    
    async def get_list_students(self, request_params: request_params) -> BaseResponse[StudentModel]:
        res = BaseResponse[StudentModel](success=True) 
        try:
            async with self.session_factory() as session:
                query = select(StudentEntity)
                
                if request_params.filter_by:
                    filter_field = request_params.filter_by.field
                    filter_value = request_params.filter_by.value
                    if hasattr(StudentEntity, filter_field):
                        query = query.where(getattr(StudentEntity, filter_field) == filter_value)
                
                if request_params.sort_by:
                    sort_field = request_params.sort_by.field
                    if hasattr(StudentEntity, sort_field):
                        if request_params.sort_by.ascending:
                            query = query.order_by(getattr(StudentEntity, sort_field).asc())
                        else:
                            query = query.order_by(getattr(StudentEntity, sort_field).desc())
                
                if request_params.page_size and request_params.page:
                    offset = (request_params.page - 1) * request_params.page_size
                    query = query.offset(offset).limit(request_params.page_size)
                
                result = await session.execute(query)   
                students = result.scalars().all()
                res.data = students
                res.page_number = request_params.page
                res.page_size = request_params.page_size
                
                count_query = select(func.count()).select_from(StudentEntity)
                total_result = await session.execute(count_query)
                res.total_records = total_result.scalar()
        except Exception as e:  
            res.success = False
            res.error = [str(e)]
        return res
    
    async def get_all_students(self) -> BaseResponse[StudentModel]:
        res = BaseResponse[StudentModel](success=True)
        try:
            async with self.session_factory() as session:
                result = await session.execute(select(StudentEntity))
                students = result.scalars().all()
                res.data = [to_domain(student) for student in students]
        except Exception as e:
            res.success = False
            res.error = [str(e)]
        return res
    
    async def get_student_by_id(self, student_id: str) -> BaseResponse[StudentModel]:
        res = BaseResponse[StudentModel](success=True)
        try:
            async with self.session_factory() as session:
                student = await session.get(StudentEntity, student_id)
                if student:
                    res.data = [to_domain(student)]
                else:
                    res.success = False
                    res.error = [f'Student with ID {student_id} not found.']
        except Exception as e:
            res.success = False
            res.error = [str(e)]
        return res
    
    async def delete_student_by_id(self, student_id: str) -> BaseResponse[StudentModel]:
        res = BaseResponse[StudentModel](success=True)
        try:
            async with self.session_factory() as session:
                student = await session.get(StudentEntity, student_id)
                if student:
                    await session.delete(student)
                    await session.commit()
                else:
                    res.success = False
                    res.error = [f'Student with ID {student_id} not found.']
        except Exception as e:
            res.success = False
            res.error = [str(e)]
        return res

    async def update_student(self, student: StudentModel) -> BaseResponse[StudentModel]:
        res = BaseResponse[StudentModel](success=True)
        try:
            async with self.session_factory() as session:
                existing_student = await session.get(StudentEntity, student.student_id)
                if existing_student:
                    entity = to_entity(student)
                    for field, value in entity.__dict__.items():
                        if not field.startswith('_'):
                            setattr(existing_student, field, value)
                    await session.commit()
                    res.data = [to_domain(existing_student)]
                else:
                    res.success = False
                    res.error = [f'Student with ID {student.student_id} not found.']
        except Exception as e:
            res.success = False
            res.error = [str(e)]
        return res