from sqlalchemy.orm import Session
from app.models.models import Teacher
from app.schemas.department import *
from typing import List
from typing import Optional

from pydantic import Field, BaseModel


class TeacherSchemas(BaseModel):
    teacher_id: Optional[int]
    name: Optional[str] = None
    gender: Optional[str] = None
    contact_info: Optional[str] = None
    department_id: Optional[int]
    position: Optional[str] = None
    specialization: Optional[str] = None


class TeacherSchemasCreate(TeacherSchemas):
    pass  # 创建时不需要提供 teacher_id


def get_teacher_by_id(db: Session, teacher_id):
    return db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()


def create_teacher(db: Session, teacher_create: TeacherSchemasCreate):
    db_teacher = Teacher(**teacher_create.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher
