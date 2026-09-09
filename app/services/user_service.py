from app.exceptions import ConflictError, NotFoundError
from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def list(self) -> list[User]:
        return self.repository.list_all()

    def get(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("Usuário não encontrado")
        return user

    def create(self, data: UserCreate) -> User:
        self._ensure_email_is_available(data.email)
        user = User(name=data.name, email=data.email)
        return self.repository.create(user)

    def update(self, user_id: int, data: UserUpdate) -> User:
        user = self.get(user_id)
        self._ensure_email_is_available(data.email, current_user_id=user.id)
        user.name = data.name
        user.email = data.email
        return self.repository.update(user)

    def delete(self, user_id: int) -> None:
        user = self.get(user_id)
        self.repository.delete(user)

    def get_with_courses(self, user_id: int) -> User:
        user = self.repository.get_with_courses(user_id)
        if user is None:
            raise NotFoundError("Usuário não encontrado")
        return user

    def _ensure_email_is_available(
        self, email: str, current_user_id: int | None = None
    ) -> None:
        existing = self.repository.get_by_email(email)
        if existing is not None and existing.id != current_user_id:
            raise ConflictError("E-mail já cadastrado")
