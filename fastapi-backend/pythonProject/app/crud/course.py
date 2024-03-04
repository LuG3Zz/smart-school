from sqlalchemy.orm import Session
from app import models
from app import schemas

from sqlalchemy.orm import Session

from app.models import models


def get_course_by_id(db: Session, course_id: str):
    return db.query(models.Course).filter(models.Course.course_id == course_id).first()


def get_course_by_teacher_id(db: Session, teacher_id: str):
    return db.query(models.Course).filter(models.Course.teacher_id == teacher_id).all()


def get_course_by_department_id(db: Session, department_id: int):
    return db.query(models.Course).join(models.Department,
                                        models.Department.department_id == models.Course.department_id).filter(
        models.Course.department_id == department_id).all()


def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()


def get_courses_count(db: Session):
    return db.query(models.Course).count()


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


def get_student_selection_course(db, student_id: str, semester: str, skip: int = 0, limit: int = 10):
    # 查询该学生已经选过的课程的 ID 列表
    enrolled_course_ids = db.query(models.StudentCourse.course_id).filter(models.StudentCourse.student_id == student_id)
    # 查询符合学生学期的课程
    available_courses = db.query(models.Course).filter(models.Course.semester == semester)
    # 筛选出学生未选的课程
    elective_courses = available_courses.filter(models.Course.course_id.notin_(enrolled_course_ids))
    # 返回可选课程的列表
    return elective_courses.limit(limit).offset(skip).all()
