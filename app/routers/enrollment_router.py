from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_session
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.user_repository import UserRepository
from app.responses import success_response
from app.schemas import EnrollmentCreate, EnrollmentOut
from app.services.enrollment_service import EnrollmentService

router = APIRouter(prefix="/enrollments", tags=["enrollments"])


def get_enrollment_service(
    session: Session = Depends(get_session),
) -> EnrollmentService:
    return EnrollmentService(
        EnrollmentRepository(session),
        UserRepository(session),
        CourseRepository(session),
    )


@router.post("")
def create_enrollment(
    payload: EnrollmentCreate,
    service: EnrollmentService = Depends(get_enrollment_service),
):
    enrollment = service.create(payload)
    return success_response(
        "Matrícula realizada com sucesso",
        data=EnrollmentOut.model_validate(enrollment),
        status_code=201,
    )
