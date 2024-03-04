from pydantic import BaseModel
from typing import Optional


class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None
    credits: int
    department_id: int
    teacher_id: Optional[str]


class CourseCreate(CourseBase):
    pass
    semester: str


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None
    teacher_id: Optional[str] = None


class CourseInDBBase(CourseBase):
    class Config:
        orm_mode = True


class Course(CourseInDBBase):
    pass


class CourseInDB(CourseInDBBase):
    pass
