from sqlalchemy.orm import Session
from app.models.models import LeaveSchool, Student, Teacher
from app.schemas.leave_school import *


def create_leave_school(db: Session, leave_school_create: LeaveSchoolSchemasCreate):
    # 创建一个离校办理对象
    db_leave_school = LeaveSchool(**leave_school_create.dict())
    # 将离校办理对象添加到 Session 中
    db.add(db_leave_school)
    # 提交 Session，将新的离校办理写入数据库
    db.commit()
    # 刷新 Session，获取新的离校办理的 ID
    db.refresh(db_leave_school)
    # 返回新的离校办理对象
    return db_leave_school


def get_user_by_leave_school(db: Session, application_id: int):
    # 查询一个指定的离校办理对象
    return db.query(LeaveSchool, Student).join(Student, LeaveSchool.student_id == Student.student_id).filter(
        LeaveSchool.application_id == application_id).first()


def get_leave_school_detail(db: Session, application_id: int):
    # 查询一个指定的离校办理对象
    # 对 leave_school 表和 student 表、teacher 表进行多表查询
    return db.query(LeaveSchool, Student, Teacher).join(Student, LeaveSchool.student_id == Student.student_id).outerjoin(
        Teacher, Teacher.teacher_id == LeaveSchool.auditor_id).filter(
        LeaveSchool.application_id == application_id).first()


def get_leave_school_count(db: Session, student_id: int) -> int:
    # 查询一个指定学生的离校办理的数量
    return db.query(LeaveSchool).filter(LeaveSchool.student_id == student_id).count()


def get_leave_school_status_count(db: Session, student_id, status: str, auditor_id=None) -> list:
    # 查询一个指定学生的指定状态的离校办理
    if auditor_id:
        # 如果指定了审核人员，那么只查询该审核人员处理的离校办理
        return db.query(LeaveSchool).filter(LeaveSchool.auditor_id == auditor_id).filter(
            LeaveSchool.application_status == status).all()
    else:
        # 否则查询所有的离校办理
        return db.query(LeaveSchool).filter(LeaveSchool.student_id == student_id).filter(
            LeaveSchool.application_status == status).all()


def get_leave_school_by_student_id(db: Session, student_id: int, skip: int = 0, limit: int = 10):
    # 查询一个指定学生的所有离校办理
    return db.query(LeaveSchool, Student.name.label('s_name'), Teacher.name.label('t_name')).join(Student,
                                                                                                  LeaveSchool.student_id == Student.student_id).filter(
        LeaveSchool.student_id == student_id).outerjoin(Teacher, Teacher.teacher_id == LeaveSchool.auditor_id).offset(
        skip).limit(limit).all()


def get_leave_school_by_auditor_id(db: Session, auditor_id: int, skip: int = 0, limit: int = 10):
    # 查询一个指定审核人员的所有离校办理
    return db.query(LeaveSchool, Teacher.name).join(Teacher, Teacher.teacher_id == auditor_id).filter(
        LeaveSchool.auditor_id == auditor_id).offset(skip).limit(limit).all()


def get_leave_school_by_department_id(db: Session, department_id: int, skip: int = 0, limit: int = 10):
    # 通过 department_id 筛选出该院系的学生
    students = db.query(Student).filter(Student.department_id == department_id).subquery()
    # 通过学生表和离校办理表进行连接查询，获取学生的姓名和离校办理
    leave_schools = db.query(LeaveSchool, students.c.name.label('s_name'), Teacher.name.label('t_name')).join(students,
                                                                                                             LeaveSchool.student_id == students.c.student_id).outerjoin(
        Teacher, Teacher.teacher_id == LeaveSchool.auditor_id).offset(
        skip).limit(limit).all()
    return leave_schools

def get_leave_school_all(db: Session,  skip: int = 0, limit: int = 10):
    return (db.query(LeaveSchool, Student.name.label('s_name'), Teacher.name.label('t_name')).join(Student,
                                                                                                  LeaveSchool.student_id == Student.student_id)
            .outerjoin(Teacher, Teacher.teacher_id == LeaveSchool.auditor_id).offset(
        skip).limit(limit).all())


def update_leave_school(db: Session, application_id: int, leave_school_update: LeaveSchoolSchemasUpdate):
    # 查询一个指定的离校办理对象
    db_leave_school = db.query(LeaveSchool).filter(LeaveSchool.application_id == application_id).first()
    if db_leave_school:
        # 获取更新的数据
        update_data = leave_school_update.dict(exclude_unset=True)
        # 遍历更新的数据，修改离校办理对象的属性
        for key, value in update_data.items():
            setattr(db_leave_school, key, value)
        # 提交 Session，将更新后的离校办理写入数据库
        db.add(db_leave_school)
        db.commit()
        # 刷新 Session，获取更新后的离校办理的 ID
        db.refresh(db_leave_school)
    # 返回更新后的离校办理对象
    return db_leave_school


def delete_leave_school(db: Session, application_id: int) -> bool:
    # 查询一个指定的离校办理对象
    db_leave_school = db.query(LeaveSchool).filter(LeaveSchool.application_id == application_id).first()
    if db_leave_school:
        # 将离校办理对象从 Session 中删除
        db.delete(db_leave_school)
        # 提交 Session，将删除后的离校办理从数据库中删除
        db.commit()
        # 返回 True 表示删除成功
        return True
    # 返回 False 表示删除失败
    return False
