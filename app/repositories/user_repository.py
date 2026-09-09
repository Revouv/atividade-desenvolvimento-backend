from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Enrollment, User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self) -> list[User]:
        return list(self.session.scalars(select(User)))

    def get_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.session.scalar(select(User).where(User.email == email))

    def get_with_courses(self, user_id: int) -> User | None:
        """Carrega o usuário com as matrículas e os cursos relacionados."""
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.enrollments).selectinload(Enrollment.course))
        )
        return self.session.scalar(stmt)

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(self, user: User) -> User:
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()
