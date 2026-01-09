from typing import List
from app.models.student_model import StudentModel
from app.repositories.student_repo import StudentRepository
from app.models.base_model import BaseResponse

class StudentService: 
    
    def __init__(self, student_repo: StudentRepository):
        self.student_repo = student_repo
    
    async def load_students(self):
        return await self.student_repo.load_students()
    
    async def insert_students(self, students: List[StudentModel]) -> BaseResponse[StudentModel]:
        print('go to here')
        return await self.student_repo.insert_students(students)
    
    async def get_list_students(self, request_params) -> BaseResponse[StudentModel]:
        return await self.student_repo.get_list_students(request_params)

    async def delete_student(self, student_id: str) -> BaseResponse[StudentModel]:
        return await self.student_repo.delete_student_by_id(student_id)
    
    async def create_student(self, student: StudentModel) -> BaseResponse[StudentModel]:
        return await self.student_repo.create_student(student)
    
    async def update_student(self, student: StudentModel) -> BaseResponse[StudentModel]:
        return await self.student_repo.update_student(student)
    
    async def analysis_point(self) -> BaseResponse[dict]:
        students = await self.student_repo.get_all_students()
        if not students.success:
            return BaseResponse(success=False, error=students.error)
        total_students = len(students.data) if students.data else 0
        if total_students == 0:
            return BaseResponse(success=True, data=[])
        total_math_excellent = sum(1 for s in students.data if s.math_score is not None and s.math_score >= 8)
        total_math_average = sum(1 for s in students.data if s.math_score is not None and 5 <= s.math_score < 8)
        total_math_poor = sum(1 for s in students.data if s.math_score is not None and s.math_score < 5)
        max_math_point = max(s.math_score for s in students.data if s.math_score is not None)
        min_math_point = min(s.math_score for s in students.data if s.math_score is not None)
        math_analysis = {
            "excellent_percentage": (total_math_excellent / total_students) * 100,
            "average_percentage": (total_math_average / total_students) * 100,
            "poor_percentage": (total_math_poor / total_students) * 100,
            "max_point": max_math_point,
            "min_point": min_math_point
        }
        total_english_excellent = sum(1 for s in students.data if s.english_score is not None and s.english_score >= 8)
        total_english_average = sum(1 for s in students.data if s.english_score is not None and 5 <= s.english_score < 8)
        total_english_poor = sum(1 for s in students.data if s.english_score is not None and s.english_score < 5)
        max_english_point = max(s.english_score for s in students.data if s.english_score is not None)
        min_english_point = min(s.english_score for s in students.data if s.english_score is not None)
        english_analysis = {
            "excellent_percentage": (total_english_excellent / total_students) * 100,
            "average_percentage": (total_english_average / total_students) * 100,
            "poor_percentage": (total_english_poor / total_students) * 100,
            "max_point": max_english_point,
            "min_point": min_english_point
        }
        
        analysis_result = {
            "math": math_analysis,
            "english": english_analysis
        }
        return BaseResponse(success=True, data=[analysis_result])