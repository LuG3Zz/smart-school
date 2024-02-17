from app import models
from app import schemas

from sqlalchemy.orm import Session
from app.models.models import StudentCourse
from app.schemas import StudentCourseUpdate, StudentCourseCreate
from app.models import models


def create_student_course(db: Session, student_course_create: StudentCourseCreate) -> StudentCourse:
    db_student_course = StudentCourse(**student_course_create.dict())
    db.add(db_student_course)
    db.commit()
    db.refresh(db_student_course)
    return db_student_course


def get_student_course(db: Session, enrollment_id: str) -> StudentCourse:
    return db.query(StudentCourse).filter(StudentCourse.enrollment_id == enrollment_id).first()


def get_student_courses(db: Session, student_id: str, skip: int = 0, limit: int = 10) -> list[StudentCourse]:
    return db.query(StudentCourse).filter(StudentCourse.student_id == student_id).offset(skip).limit(limit).all()


def update_student_course(db: Session, enrollment_id: str, student_course_update: StudentCourseUpdate) -> StudentCourse:
    db_student_course = db.query(StudentCourse).filter(StudentCourse.enrollment_id == enrollment_id).first()
    if db_student_course:
        update_data = student_course_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_student_course, key, value)
        db.commit()
        db.refresh(db_student_course)
    return db_student_course


def delete_student_course(db: Session, enrollment_id: str) -> bool:
    db_student_course = db.query(StudentCourse).filter(StudentCourse.enrollment_id == enrollment_id).first()
    if db_student_course:
        db.delete(db_student_course)
        db.commit()
        return True
    return False