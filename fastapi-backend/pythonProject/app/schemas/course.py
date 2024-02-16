from pydantic import BaseModel
from typing import Optional


class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None
    credits: int
    department_id: int
    teacher_id: str


class CourseCreate(CourseBase):
    pass


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


# 选课请求模型


# 选课请求模型
class StudentCourseCreate(BaseModel):
    student_id: str
    course_id: int
    semester: str


# 更新选课请求模型
class StudentCourseUpdate(BaseModel):
    grade: str


# 完整的选课模型，包含自动生成的字段
class StudentCourseModel(StudentCourseCreate):
    enrollment_id: str
    grade: None  # 成绩可以在选课后更新

    class Config:
        orm_mode = True
