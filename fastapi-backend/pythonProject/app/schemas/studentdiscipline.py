# 定义学生违纪处分表对应的 schemas 结构
from typing import Optional

from pydantic import Field, BaseModel


class StudentDisciplineBase(BaseModel):
    student_id: Optional[str] = None
    discipline_type: Optional[str] = None
    discipline_date: Optional[str] = None
    discipline_detail: Optional[str] = None
    discipline_result: Optional[str] = None
    handler_id: Optional[str] = None


class StudentDisciplineCreate(StudentDisciplineBase):
    pass  # 创建时不需要提供 discipline_id


class StudentDisciplineUpdate(StudentDisciplineBase):
    pass  # 更新时不需要提供 discipline_id


class Discipline(StudentDisciplineBase):
    class Config:
        orm_mode = True  # 允许与 ORM 模型兼容
