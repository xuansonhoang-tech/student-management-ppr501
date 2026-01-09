from fastapi import FastAPI
from app.routes.student_router import router

app = FastAPI(title="Student Management API")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

