from sqlalchemy.orm import Session
from app.models.models import Student, StudentDormitory, Dormitory, Department  # 假设这是我们的SQLAlchemy宿舍模型
from app.schemas.dormitory import DormitoryCreate, DormitoryUpdate
from app.schemas.student_dorm import *


def create_dormitory(db: Session, dormitory_create: DormitoryCreate) -> Dormitory:
    db_dormitory = Dormitory(**dormitory_create.dict())
    db.add(db_dormitory)
    db.commit()
    db.refresh(db_dormitory)
    return db_dormitory


def get_dormitory(db: Session, dormitory_id: str) -> Dormitory:
    return db.query(Dormitory).filter(Dormitory.dormitory_id == dormitory_id).first()


def get_dormitories(db: Session, skip: int = 0, limit: int = 10) -> list[Dormitory]:
    return db.query(Dormitory).offset(skip).limit(limit).all()


def update_dormitory(db: Session, dormitory_id: str, dormitory_update: DormitoryUpdate) -> Dormitory:
    db_dormitory = db.query(Dormitory).filter(Dormitory.dormitory_id == dormitory_id).first()
    if db_dormitory:
        update_data = dormitory_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_dormitory, key, value)
        db.add(db_dormitory)
        db.commit()
        db.refresh(db_dormitory)
    return db_dormitory


def delete_dormitory(db: Session, dormitory_id: str) -> bool:
    db_dormitory = db.query(Dormitory).filter(Dormitory.dormitory_id == dormitory_id).first()
    if db_dormitory:
        db.delete(db_dormitory)
        db.commit()
        return True
    return False


def get_dormitories_by_student_id(db: Session, student_id: str, skip: int = 0, limit: int = 10):
    # 使用 query 方法来查询 Dorm 表和 StDorm 表
    # 使用 join 方法来连接两个表，根据宿舍 ID 匹配
    # 使用 filter 方法来筛选符合学生学号的记录
    # 使用 offset 和 limit 方法来分页查询
    # 使用 first 方法来返回查询结果的第一个元素，如果没有结果则返回 None
    return db.query(Dormitory).join(StudentDormitory, StudentDormitory.dormitory_id == Dormitory.dormitory_id).filter(
        StudentDormitory.student_id == student_id).offset(skip).limit(limit).all()


# 定义一个函数，接受数据库会话和学院 ID 参数
def get_dormitories_by_department_id(db: Session, department_id: int, skip: int = 0, limit: int = 10):
    # 使用 query 方法来查询 Student, StudentDormitory, Dormitory, 和 Department 表
    # 使用 join 方法来连接四个表，根据外键匹配
    # 使用 filter 方法来筛选符合学院 ID 的记录
    # 使用 all 方法来返回查询结果的所有元素，如果没有结果则返回空列表
    return (db.query(Dormitory).join(StudentDormitory, Dormitory.dormitory_id == StudentDormitory.dormitory_id)
            .join(Student, Student.student_id == StudentDormitory.student_id).filter(
        Student.department_id == department_id).offset(skip).limit(limit).all())


def get_students_by_dormitory_id(db: Session, dormitory_id: int):
    # 使用 query 方法来查询 Student, StudentDormitory, 和 Dormitory 表
    # 使用 join 方法来连接三个表，根据外键匹配
    # 使用 filter 方法来筛选符合宿舍号的记录
    # 使用 all 方法来返回查询结果的所有元素，如果没有结果则返回空列表
    return db.query(Student, Department.name.label('department'), StudentDormitory).join(StudentDormitory,
                                                                                         Student.student_id == StudentDormitory.student_id).join(
        Dormitory, StudentDormitory.dormitory_id == Dormitory.dormitory_id).join(Department,
                                                                                 Department.department_id == Student.department_id).filter(
        Dormitory.dormitory_id == dormitory_id).all()


def get_dormitories_all(db: Session, skip: int = 0, limit: int = 10):
    # 使用 query 方法来查询需要的字段
    # 使用 join 方法来连接四个表，并使用 on 关键字来指定连接条件
    # 使用 filter 方法来添加过滤条件，根据需求进行筛选
    # 使用 all 方法来返回查询结果的所有元素，如果没有结果则返回空列表
    return db.query(Dormitory).offset(skip).limit(limit).all()


def create_student_dormitory(db: Session, student_dormitory_create: StudentDormitorySchemasCreate) -> StudentDormitory:
    db_student_dormitory = StudentDormitory(**student_dormitory_create.dict())
    db.add(db_student_dormitory)
    db.commit()
    db.refresh(db_student_dormitory)
    return db_student_dormitory


def get_student_dormitory(db: Session, assignment_id: int) -> StudentDormitory:
    return db.query(StudentDormitory).filter(StudentDormitory.assignment_id == assignment_id).first()


def get_student_dormitories(db: Session, skip: int = 0, limit: int = 10) -> list[StudentDormitory]:
    return db.query(StudentDormitory).offset(skip).limit(limit).all()


def update_student_dormitory(db: Session, assignment_id: int,
                             student_dormitory_update: StudentDormitorySchemasUpdate) -> StudentDormitory:
    db_student_dormitory = db.query(StudentDormitory).filter(StudentDormitory.assignment_id == assignment_id).first()
    if db_student_dormitory:
        update_data = student_dormitory_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_student_dormitory, key, value)
        db.commit()
        db.refresh(db_student_dormitory)
    return db_student_dormitory


def delete_student_dormitory(db: Session, assignment_id: int) -> bool:
    db_student_dormitory = db.query(StudentDormitory).filter(StudentDormitory.assignment_id == assignment_id).first()
    if db_student_dormitory:
        db.delete(db_student_dormitory)
        db.commit()
        return True
    return False
