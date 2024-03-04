from sqlalchemy import func
from sqlalchemy.orm import Session, aliased
from app.models.models import Department, Student
from app.schemas.department import *
from typing import List


def create_department(db: Session, department_create: DepartmentCreate) -> DepartmentAll:
    db_department = Department(**department_create.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


def get_department(db: Session, department_id: str) -> DepartmentAll:
    return db.query(Department).filter(Department.department_id == department_id).first()


def get_department_all(db: Session):
    return db.query(Department).count()


def get_department_students_count(db: Session, department_id: int):
    return db.query(Student).filter(Student.department_id == department_id).count()


def get_department_students(db: Session, department_id: int, skip: int = 0, limit: int = 100):
    return db.query(Student).filter(Student.department_id == department_id).offset(skip).limit(limit).all()


def get_departments(db: Session, skip: int = 0, limit: int = 10) -> List[DepartmentAll]:
    return db.query(Department).offset(skip).limit(limit).all()


def update_department(db: Session, department_update: DepartmentUpdate) -> DepartmentAll:
    db_department = db.query(Department).filter(Department.department_id == department_update.department_id).first()
    if db_department:
        update_data = department_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_department, key, value)
        db.commit()
        db.refresh(db_department)
    return db_department


def delete_department(db: Session, department_id: str) -> bool:
    db_department = db.query(Department).filter(Department.department_id == department_id).first()
    if db_department:
        db.delete(db_department)
        db.commit()
        return True
    return False


# 统计某个学院男女学生数量的 crud 函数
def get_department_student_gender(db: Session, department_id: int, gender: str = "男"):
    # 查询某个学院的所有学生
    db_students = db.query(Student).join(Department, Student.department_id == Department.department_id).filter(
        Department.department_id == department_id)
    # 根据性别过滤学生
    db_students = db_students.filter(Student.gender == gender).all()
    return db_students


def get_department_student_major(db: Session, department_id: int, major):
    # 查询某个专业的所有学生
    db_students = db.query(Student).join(Department, Student.department_id == Department.department_id).filter(
        Department.department_id == department_id)
    # 根据性别过滤学生
    db_students = db_students.filter(Student.major == major).all()
    return db_students


def get_major_percent(db: Session):
    # 创建别名，方便后续查询
    d = aliased(Department)
    s = aliased(Student)

    # 查询每个学院的总人数
    total_students = db.query(d.department_id, d.name.label('department_name'),
                              func.count(s.student_id).label('total_students')).join(s,
                                                                                     d.department_id == s.department_id).group_by(
        d.department_id, d.name).subquery()

    # 查询每个学院的每个专业的人数
    major_students = db.query(d.department_id, d.name.label('department_name'), s.major,
                              func.count(s.student_id).label('major_students')).join(s,
                                                                                     d.department_id == s.department_id).group_by(
        d.department_id, d.name, s.major).subquery()

    # 将两个查询结果连接起来，计算每个专业在学院中的占比
    percentage = db.query(major_students.c.department_id, major_students.c.department_name, major_students.c.major.label("name"),
                          major_students.c.major_students.label("value"), total_students.c.total_students,
                          func.round(major_students.c.major_students * 100.0 / total_students.c.total_students,
                                     2).label('percentage')).join(total_students,
                                                                  major_students.c.department_id == total_students.c.department_id).order_by(
        major_students.c.department_id, major_students.c.major)
    return percentage.all()
