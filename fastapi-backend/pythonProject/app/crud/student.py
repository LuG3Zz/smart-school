from app import models
from app.models.models import Student, Department, Teacher
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


def get_teacher_by_id(db: Session, teacher_id: str):
    return db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()


def update_student(db: Session, student_id: str, student: StudentUpdate):
    db_student = db.query(Student).filter(Student.student_id == student_id).first()
    if db_student:
        update_data = student.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Student).offset(skip).limit(limit).all()


def get_department_by_id(db: Session, department_id):
    return db.query(Department).filter(Department.department_id == department_id).first()


def delete_student(db: Session, student_id: str):
    db_student = db.query(Student).filter(Student.student_id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student
