from typing import Optional

from pydantic import  BaseModel


class StudentDormitorySchemas(BaseModel):
    assignment_id: Optional[int]
    student_id: Optional[str]
    dormitory_id: Optional[int]
    assignment_date: Optional[str]
    leave_date: Optional[str]


class StudentDormitorySchemasCreate(StudentDormitorySchemas):
    pass  # 创建时不需要提供 assignment_id


class StudentDormitorySchemasUpdate(StudentDormitorySchemas):
    pass  # 更新时不需要提供新的字段
