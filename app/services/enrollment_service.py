from app.exceptions import ConflictError, NotFoundError
from app.models import Enrollment
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.user_repository import UserRepository
from app.schemas import EnrollmentCreate


class EnrollmentService:
    def __init__(
        self,
        repository: EnrollmentRepository,
        user_repository: UserRepository,
        course_repository: CourseRepository,
    ) -> None:
        self.repository = repository
        self.user_repository = user_repository
        self.course_repository = course_repository

    def create(self, data: EnrollmentCreate) -> Enrollment:
        self._ensure_user_exists(data.user_id)
        self._ensure_course_exists(data.course_id)
        self._ensure_not_already_enrolled(data.user_id, data.course_id)

        enrollment = Enrollment(user_id=data.user_id, course_id=data.course_id)
        return self.repository.create(enrollment)

    def _ensure_user_exists(self, user_id: int) -> None:
        if self.user_repository.get_by_id(user_id) is None:
            raise NotFoundError("Usuário não encontrado")

    def _ensure_course_exists(self, course_id: int) -> None:
        if self.course_repository.get_by_id(course_id) is None:
            raise NotFoundError("Curso não encontrado")

    def _ensure_not_already_enrolled(self, user_id: int, course_id: int) -> None:
        if self.repository.get_by_user_and_course(user_id, course_id) is not None:
            raise ConflictError("Matrícula duplicada")
