from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_session
from app.repositories.user_repository import UserRepository
from app.responses import success_response
from app.schemas import (
    UserCreate,
    UserOut,
    UserUpdate,
    UserWithCoursesOut,
)
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(UserRepository(session))


@router.post("")
def create_user(
    payload: UserCreate, service: UserService = Depends(get_user_service)
):
    user = service.create(payload)
    return success_response(
        "Usuário criado com sucesso",
        data=UserOut.model_validate(user),
        status_code=201,
    )


@router.get("")
def list_users(service: UserService = Depends(get_user_service)):
    users = service.list()
    return success_response(
        "Usuários listados com sucesso",
        data=[UserOut.model_validate(user) for user in users],
    )


@router.get("/{user_id}")
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = service.get(user_id)
    return success_response(
        "Usuário encontrado", data=UserOut.model_validate(user)
    )


@router.put("/{user_id}")
def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    user = service.update(user_id, payload)
    return success_response(
        "Usuário atualizado com sucesso", data=UserOut.model_validate(user)
    )


@router.delete("/{user_id}")
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    service.delete(user_id)
    return success_response("Usuário removido com sucesso", data=None)


@router.get("/{user_id}/courses")
def get_user_courses(
    user_id: int, service: UserService = Depends(get_user_service)
):
    user = service.get_with_courses(user_id)
    data = UserWithCoursesOut.model_validate(
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at,
            "courses": [enrollment.course for enrollment in user.enrollments],
        }
    )
    return success_response("Cursos do usuário listados com sucesso", data=data)
