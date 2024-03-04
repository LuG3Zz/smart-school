from sqlalchemy.orm import Session
from app.models.models import StudentRecord, Student, Teacher
from app.schemas.record import *


def create_record(db: Session, record_create: RecordSchemasCreate):
    db_record = StudentRecord(**record_create.dict())
    db.add(db_record)
    # 提交 Session，将新的违纪处分写入数据库
    db.commit()
    # 刷新 Session，获取新的违纪处分的 ID
    db.refresh(db_record)
    # 返回新的违纪处分对象
    return db_record


def get_user_by_record(db: Session, reord_id: int):
    pass


def get_record_detail(db: Session, record_id: int):
    # 查询一个指定的违纪处分对象
    # 对 record 表和 student 表、teacher 表进行多表查询
    return db.query(StudentRecord, Student).join(Student,
                                                 StudentRecord.student_id == Student.student_id).filter(
        StudentRecord.record_id == record_id).first()


def get_record_count(db: Session, student_id: int) -> int:
    # 查询一个指定学生的违纪处分的数量
    return db.query(StudentRecord).filter(StudentRecord.student_id == student_id).count()


def get_record_status_count(db: Session, student_id, status: str, teacher_id=None, ) -> list:
    if teacher_id:
        return db.query(StudentRecord).filter(StudentRecord.auditor == teacher_id).filter(
            StudentRecord.status == status).all()
    else:
        return db.query(StudentRecord).filter(StudentRecord.student_id == student_id).filter(
            StudentRecord.status == status).all()


#
#
# def get_discipline_results(db: Session) -> list:
#    # 查询所有的违纪处分
#    return db.query(StudentDiscipline.discipline_result).distinct().all()
#
#
def get_record_by_student_id(db: Session, student_id: int, skip: int = 0, limit: int = 10):
    return db.query(StudentRecord, Student.name.label('s_name'), Teacher.name.label('t_name')).join(Student,
                                                                                                    StudentRecord.student_id == Student.student_id).filter(
        StudentRecord.student_id == student_id).outerjoin(Teacher, Teacher.teacher_id == StudentRecord.auditor).offset(
        skip).limit(limit).all()


def get_record_by_auditor_id(db: Session, auditor: int, skip: int = 0, limit: int = 10):
    # 查询一个指定处理人的所有违纪处分
    return db.query(StudentRecord, Teacher.name).join(Teacher, Teacher.teacher_id == auditor).filter(
        StudentRecord.auditor == auditor).offset(skip).limit(limit).all()


def get_record_all(db: Session, skip: int = 0, limit: int = 10):
    return db.query(StudentRecord, Student.name.label('s_name'), Teacher.name.label('t_name')).join(Student,
                                                                                                    StudentRecord.student_id == Student.student_id).outerjoin(
        Teacher, Teacher.teacher_id == StudentRecord.auditor).offset(
        skip).limit(limit).all()


def get_record_by_department_id(db: Session, department_id: int, skip: int = 0, limit: int = 10):
    # 通过 department_id 筛选出该院系的学生
    students = db.query(Student).filter(Student.department_id == department_id).subquery()
    # 通过学生表和成绩表进行连接查询，获取学生的姓名和成绩
    records = db.query(StudentRecord, students.c.name.label('s_name'), Teacher.name.label('t_name')).join(students,
                                                                                                          StudentRecord.student_id == students.c.student_id).outerjoin(
        Teacher, Teacher.teacher_id == StudentRecord.auditor).offset(
        skip).limit(limit).all()
    return records


#
#
def update_record(db: Session, record_id: int, record_update: RecordSchemasUpdate):
    # 查询一个指定的违纪处分对象
    db_record = db.query(StudentRecord).filter(StudentRecord.record_id == record_id).first()
    if db_record:
        # 获取更新的数据
        update_data = record_update.dict(exclude_unset=True)
        # 遍历更新的数据，修改违纪处分对象的属性
        for key, value in update_data.items():
            setattr(db_record, key, value)
        # 提交 Session，将更新后的违纪处分写入数据库
        db.add(db_record)
        db.commit()
        # 刷新 Session，获取更新后的违纪处分的 ID
        db.refresh(db_record)
    # 返回更新后的违纪处分对象
    return db_record


#
#
def delete_record(db: Session, record_id: int) -> bool:
    # 查询一个指定的违纪处分对象
    db_record = db.query(StudentRecord).filter(StudentRecord.record_id == record_id).first()
    if db_record:
        # 将违纪处分对象从 Session 中删除
        db.delete(db_record)
        # 提交 Session，将删除后的违纪处分从数据库中删除
        db.commit()
        # 返回 True 表示删除成功
        return True
    # 返回 False 表示删除失败
    return False
