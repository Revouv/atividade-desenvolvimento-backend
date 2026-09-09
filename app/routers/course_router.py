from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_session
from app.repositories.course_repository import CourseRepository
from app.responses import success_response
from app.schemas import CourseCreate, CourseOut, CourseUpdate
from app.services.course_service import CourseService

router = APIRouter(prefix="/courses", tags=["courses"])


def get_course_service(session: Session = Depends(get_session)) -> CourseService:
    return CourseService(CourseRepository(session))


@router.post("")
def create_course(
    payload: CourseCreate, service: CourseService = Depends(get_course_service)
):
    course = service.create(payload)
    return success_response(
        "Curso criado com sucesso",
        data=CourseOut.model_validate(course),
        status_code=201,
    )


@router.get("")
def list_courses(service: CourseService = Depends(get_course_service)):
    courses = service.list()
    return success_response(
        "Cursos listados com sucesso",
        data=[CourseOut.model_validate(course) for course in courses],
    )


@router.get("/{course_id}")
def get_course(
    course_id: int, service: CourseService = Depends(get_course_service)
):
    course = service.get(course_id)
    return success_response(
        "Curso encontrado", data=CourseOut.model_validate(course)
    )


@router.put("/{course_id}")
def update_course(
    course_id: int,
    payload: CourseUpdate,
    service: CourseService = Depends(get_course_service),
):
    course = service.update(course_id, payload)
    return success_response(
        "Curso atualizado com sucesso", data=CourseOut.model_validate(course)
    )


@router.delete("/{course_id}")
def delete_course(
    course_id: int, service: CourseService = Depends(get_course_service)
):
    service.delete(course_id)
    return success_response("Curso removido com sucesso", data=None)
