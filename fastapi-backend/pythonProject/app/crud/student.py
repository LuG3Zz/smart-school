from app import models
from app.models.models import Student, Department, Teacher, User
from app.schemas.student import *
from sqlalchemy.orm import Session


def create_student(db: Session, student: StudentCreate):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_student(db: Session, student_id: str):
    return db.query(Student).filter(Student.student_id == student_id).first()


def get_student_by_userid(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    return db.query(Student).filter(Student.student_id == user.associated_id).first()


def get_all_student(db: Session):
    return db.query(Student).all()


def get_teacher_by_id(db: Session, teacher_id: str):
    return db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()


def get_teachers_by_department_id(db: Session, department_id: int):
    return db.query(Teacher).filter(Teacher.department_id == department_id).all()


def update_student(db: Session, student_id: str, student: StudentUpdate):
    db_student = db.query(Student).filter(Student.student_id == student_id).first()
    if db_student:
        update_data = student.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student


def get_students(db: Session, student_id: str = None, skip: int = 0, limit: int = 100):
    if student_id is None:
        return db.query(Student).offset(skip).limit(limit).all()
    else:
        return db.query(Student).filter(Student.student_id == student_id).offset(skip).limit(limit).all()


def get_department_by_id(db: Session, department_id):
    return db.query(Department).filter(Department.department_id == department_id).first()


def delete_student(db: Session, student_id: str):
    db_student = db.query(Student).filter(Student.student_id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student


def get_students_by_gender(db: Session, gender: str):
    return db.query(Student).filter(Student.gender == gender).all()
