from sqlalchemy.orm import Session
from app import models
from app import schemas

from sqlalchemy.orm import Session

from app.models import models
from app.models.models import StudentCourse
from app.schemas import StudentCourseUpdate, StudentCourseCreate


def get_course(db: Session, course_id: str):
    return db.query(models.Course).filter(models.Course.course_id == course_id).first()


def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()


def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def update_course(db: Session, course_id: str, course: schemas.CourseUpdate):
    db_course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if db_course:
        update_data = course.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_course, key, value)
        db.commit()
        db.refresh(db_course)
    return db_course


def delete_course(db: Session, course_id: str):
    db_course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if db_course:
        db.delete(db_course)
        db.commit()
        return True
    return False


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
