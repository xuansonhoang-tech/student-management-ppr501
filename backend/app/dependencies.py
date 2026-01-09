from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.student_repo import StudentRepository 
from app.services.student_service import StudentService
from app.core.database import get_db 


async def get_student_service(db: AsyncSession = Depends(get_db)) -> StudentService:
    repo = StudentRepository(session_factory=lambda: db)
    return StudentService(student_repo=repo)
