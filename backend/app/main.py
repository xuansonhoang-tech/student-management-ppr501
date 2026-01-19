from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.student_router import router

app = FastAPI(title="Student Management API")

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


#------------------------------------import data to db script------------------------------------
# import asyncio

# from app.repositories.student_repo import StudentRepository
# from app.services.student_service import StudentService
# from app.core.database import AsyncSessionLocal

# DATASET_PATH = "app/seeds/students_100.csv"


# async def main():
#     service = StudentService(
#         student_repo=StudentRepository(AsyncSessionLocal)
#     )

#     students = await service.student_repo.load_students(DATASET_PATH)
#     print("students:", students)

#     if not students.success or not students.data:
#         print(f"Error loading students: {students.error}")
#         return

#     print(f"Loaded {len(students.data)} students")
#     for student in students.data:
#         result = await service.create_student(student)
#         if result.success:
#             print(f"Created student: {student.student_id}")
#         else:
#             print(f"Error creating student {student.student_id}: {result.error}")

#     print("Data seeding completed!")


# if __name__ == "__main__":
#     asyncio.run(main())
