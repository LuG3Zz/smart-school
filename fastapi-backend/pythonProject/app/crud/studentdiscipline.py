# 导入 SQLAlchemy 相关的模块

from sqlalchemy.orm import Session
from app.models.models import StudentDiscipline
from app.schemas.studentdiscipline import *


def create_discipline(db: Session, discipline_create: StudentDisciplineCreate):
    # 创建一个新的违纪处分对象
    db_discipline = StudentDiscipline(**discipline_create.dict())
    # 将新的违纪处分对象添加到 Session 中
    db.add(db_discipline)
    # 提交 Session，将新的违纪处分写入数据库
    db.commit()
    # 刷新 Session，获取新的违纪处分的 ID
    db.refresh(db_discipline)
    # 返回新的违纪处分对象
    return db_discipline


def get_discipline(db: Session, discipline_id: int) -> StudentDiscipline:
    # 查询一个指定的违纪处分对象
    return db.query(StudentDiscipline).filter(StudentDiscipline.discipline_id == discipline_id).first()


def get_discipline_count(db: Session, student_id: int) -> int:
    # 查询一个指定学生的违纪处分的数量
    return db.query(StudentDiscipline).filter(StudentDiscipline.student_id == student_id).count()


def get_discipline_types(db: Session) -> list:
    # 查询所有的违纪类型
    return db.query(StudentDiscipline.discipline_type).distinct().all()


def get_discipline_results(db: Session) -> list:
    # 查询所有的违纪处分
    return db.query(StudentDiscipline).all()


def get_disciplines_by_student_id(db: Session, student_id: int, skip: int = 0, limit: int = 10):
    # 查询一个指定学生的所有违纪处分
    return db.query(StudentDiscipline).filter(StudentDiscipline.student_id == student_id).offset(skip).limit(limit).all()


def get_disciplines_by_handler_id(db: Session, handler_id: int, skip: int = 0, limit: int = 10):
    # 查询一个指定处理人的所有违纪处分
    return db.query(StudentDiscipline).filter(StudentDiscipline.handler_id == handler_id).offset(skip).limit(limit).all()


def update_discipline(db: Session, discipline_id: int, discipline_update: Discipline) -> Discipline:
    # 查询一个指定的违纪处分对象
    db_discipline = db.query(StudentDiscipline).filter(StudentDiscipline.discipline_id == discipline_id).first()
    if db_discipline:
        # 获取更新的数据
        update_data = discipline_update.dict(exclude_unset=True)
        # 遍历更新的数据，修改违纪处分对象的属性
        for key, value in update_data.items():
            setattr(db_discipline, key, value)
        # 提交 Session，将更新后的违纪处分写入数据库
        db.commit()
        # 刷新 Session，获取更新后的违纪处分的 ID
        db.refresh(db_discipline)
    # 返回更新后的违纪处分对象
    return db_discipline


def delete_discipline(db: Session, discipline_id: int) -> bool:
    # 查询一个指定的违纪处分对象
    db_discipline = db.query(StudentDiscipline).filter(StudentDiscipline.discipline_id == discipline_id).first()
    if db_discipline:
        # 将违纪处分对象从 Session 中删除
        db.delete(db_discipline)
        # 提交 Session，将删除后的违纪处分从数据库中删除
        db.commit()
        # 返回 True 表示删除成功
        return True
    # 返回 False 表示删除失败
    return False
