from app.exceptions import NotFoundError
from app.models import Course
from app.repositories.course_repository import CourseRepository
from app.schemas import CourseCreate, CourseUpdate


class CourseService:
    def __init__(self, repository: CourseRepository) -> None:
        self.repository = repository

    def list(self) -> list[Course]:
        return self.repository.list_all()

    def get(self, course_id: int) -> Course:
        course = self.repository.get_by_id(course_id)
        if course is None:
            raise NotFoundError("Curso não encontrado")
        return course

    def create(self, data: CourseCreate) -> Course:
        course = Course(
            title=data.title,
            description=data.description,
            workload=data.workload,
        )
        return self.repository.create(course)

    def update(self, course_id: int, data: CourseUpdate) -> Course:
        course = self.get(course_id)
        course.title = data.title
        course.description = data.description
        course.workload = data.workload
        return self.repository.update(course)

    def delete(self, course_id: int) -> None:
        course = self.get(course_id)
        self.repository.delete(course)
