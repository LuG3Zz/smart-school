from sqlalchemy.orm import Session
from app.schemas import *
from sqlalchemy import or_, and_


def get_message(db: Session, message: int):
    return db.query(Message).filter(Message.id == message, Message.status == False).first()


def get_pid_message(db: Session, message: int):
    return db.query(Message).filter(and_(Message.id != message, Message.pid == message, Message.status == False)).all()


def get_message_list(db: Session, userid: int):
    return db.query(Message).filter(
        or_(Message.senduser == userid, Message.acceptusers == userid,
            Message.status == 0)).all()


def db_creat_rebackmessage(db: Session, reback: RebackMessConnet, senduser: int):
    times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

    reabck = Message(pid=reback.id, context=reback.connect)
    reabck.sendtime = times
    reabck.senduser = senduser
    db.add(reabck)
    db.commit()  # 提交保存到数据库中
    db.refresh(reabck)  # 刷新
    return reabck
