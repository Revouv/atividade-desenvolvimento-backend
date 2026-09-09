from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Enrollment


class EnrollmentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_by_user(self, user_id: int) -> list[Enrollment]:
        return list(
            self.session.scalars(
                select(Enrollment).where(Enrollment.user_id == user_id)
            )
        )

    def get_by_user_and_course(
        self, user_id: int, course_id: int
    ) -> Enrollment | None:
        return self.session.scalar(
            select(Enrollment).where(
                Enrollment.user_id == user_id,
                Enrollment.course_id == course_id,
            )
        )

    def create(self, enrollment: Enrollment) -> Enrollment:
        self.session.add(enrollment)
        self.session.commit()
        self.session.refresh(enrollment)
        return enrollment
