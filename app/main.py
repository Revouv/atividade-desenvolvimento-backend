from fastapi import FastAPI

from app.database import create_tables
from app.exception_handlers import register_exception_handlers
from app.routers import course_router, enrollment_router, user_router


def create_app() -> FastAPI:
    app = FastAPI(title="StudyManager API")

    create_tables()

    register_exception_handlers(app)
    app.include_router(user_router.router)
    app.include_router(course_router.router)
    app.include_router(enrollment_router.router)

    return app


app = create_app()
