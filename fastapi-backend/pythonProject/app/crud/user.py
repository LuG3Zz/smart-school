from sqlalchemy.orm import Session
# from app.models.models import *
from app.models.models import *
from app.schemas import *
from fastapi.encoders import jsonable_encoder


# 通过id查询用户
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_id(db: Session, associated_id: str):
    return db.query(User).filter(User.associated_id == associated_id).first()


def get_user_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_info_by_username(db: Session, user_name: str):
    # 查询用户信息
    user_info = db.query(User).filter(User.username == user_name).first()
    print("user_info", jsonable_encoder(user_info))

    # 检查是否找到用户
    if user_info is None:
        return None  # 或者抛出异常，根据您的需求

    # 根据用户角色获取相关信息
    role_name = get_role_name(db, user_info.role).name
    print("role_name",role_name)
    if role_name == "学生":
        return db.query(Student).filter(Student.student_id == user_info.associated_id).first()
    else:
        return db.query(Teacher).filter(Teacher.teacher_id == user_info.associated_id).first()


def get_role_name(db: Session, id: id):
    return db.query(Role).filter(Role.id == id).first()


# 新建用户
def db_create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_user)  # 刷新
    return db_user
