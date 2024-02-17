from sqlalchemy.orm import Session
from app import models
from app import schemas

from sqlalchemy.orm import Session

from app.models import models



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



