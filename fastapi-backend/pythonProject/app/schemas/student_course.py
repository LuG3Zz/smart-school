# 选课请求模型
from pydantic import BaseModel


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
