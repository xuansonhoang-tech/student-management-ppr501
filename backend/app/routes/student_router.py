from fastapi import APIRouter, Depends, Query
from app.services.student_service import StudentService
from app.schema.student_schema import CreateStudent, StudentResponse
from app.models.request_params import request_params, sort_params, filter_params
from app.dependencies import get_student_service
from typing import Optional

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/insert", response_model=dict)
async def create_student(students: list[CreateStudent], service: StudentService = Depends(get_student_service)):
    return await service.insert_students(students)

@router.get("/list")
async def list_students(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    filter_field: Optional[str] = None,
    filter_value: Optional[str] = None,
    sort_field: Optional[str] = None,
    ascending: bool = True,
    service: StudentService = Depends(get_student_service)
):
    sort_by = sort_params(field=sort_field, ascending=ascending) if sort_field else None
    filter_by = filter_params(field=filter_field, value=filter_value) if filter_field and filter_value else None
    params = request_params(page=page, page_size=page_size, sort_by=sort_by, filter_by=filter_by)
    
    return await service.get_list_students(params)

@router.get("/{student_id}")
async def get_student(student_id: str, service: StudentService = Depends(get_student_service)):
    return await service.student_repo.get_student_by_id(student_id)

@router.delete("/{student_id}")
async def delete_student(student_id: str, service: StudentService = Depends(get_student_service)):
    return await service.delete_student(student_id)

@router.post("/")
async def create_new_student(student: CreateStudent, service: StudentService = Depends(get_student_service)):
    return await service.create_student(student)

@router.patch("/")
async def update_existing_student(student: CreateStudent, service: StudentService = Depends(get_student_service)):
    return await service.update_student(student)

@router.get("/analysis/points")
async def analyze_student_points(service: StudentService = Depends(get_student_service)):
    return await service.analysis_point()