from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# --- User ---------------------------------------------------------------------
class UserCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr


class UserUpdate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    created_at: datetime


# --- Course -----------------------------------------------------------------
class CourseCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    workload: int = Field(gt=0)


class CourseUpdate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    workload: int = Field(gt=0)


class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    workload: int


# --- Enrollment -------------------------------------------------------------
class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int


class EnrollmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime


# --- Consulta relacional --------------------------------------------------
class UserWithCoursesOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    created_at: datetime
    courses: list[CourseOut]
