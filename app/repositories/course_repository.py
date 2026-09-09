from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Course


class CourseRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self) -> list[Course]:
        return list(self.session.scalars(select(Course)))

    def get_by_id(self, course_id: int) -> Course | None:
        return self.session.get(Course, course_id)

    def create(self, course: Course) -> Course:
        self.session.add(course)
        self.session.commit()
        self.session.refresh(course)
        return course

    def update(self, course: Course) -> Course:
        self.session.commit()
        self.session.refresh(course)
        return course

    def delete(self, course: Course) -> None:
        self.session.delete(course)
        self.session.commit()
