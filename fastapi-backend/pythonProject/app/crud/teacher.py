from sqlalchemy.orm import Session
from app.models.models import Teacher
from app.schemas.department import *
from typing import List


def get_teacher_by_id(db: Session, teacher_id):
    return db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
