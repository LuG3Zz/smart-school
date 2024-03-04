from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.models import Notification
from app.schemas.notification import *


def create_notification(db: Session, notification_create: NotificationCreate):
    # 创建一个新的通知对象
    db_notification = Notification(**notification_create.dict())
    # 将新的通知对象添加到 Session 中
    db.add(db_notification)
    # 提交 Session，将新的通知写入数据库
    db.commit()
    # 刷新 Session，获取新的通知的 ID
    db.refresh(db_notification)
    # 返回新的通知对象
    return db_notification


def get_notification(db: Session, notification_id: int) -> Notification:
    # 查询一个指定的通知对象
    return db.query(Notification).filter(Notification.notification_id == notification_id).first()


def get_notifications_by_target_user_id(db: Session, target_user_id: int, skip: int = 0, limit: int = 10):
    # 查询一个指定用户的所有通知
    return db.query(Notification).filter(Notification.target_user_id == target_user_id).offset(skip).limit(limit).all()


def get_notifications_by_publisher_id(db: Session, publisher_id: int, skip: int = 0, limit: int = 10):
    # 查询一个指定用户的所有通知
    return db.query(Notification).filter(Notification.publisher_id == publisher_id).offset(skip).limit(limit).all()


def update_notification(db: Session, notification_id: int, notification_update: NotificationUpdate) -> Notification:
    # 查询一个指定的通知对象
    db_notification = db.query(Notification).filter(Notification.notification_id == notification_id).first()
    if db_notification:
        # 获取更新的数据
        update_data = notification_update.dict(exclude_unset=True)
        # 遍历更新的数据，修改通知对象的属性
        for key, value in update_data.items():
            setattr(db_notification, key, value)
        # 提交 Session，将更新后的通知写入数据库
        db.commit()
        # 刷新 Session，获取更新后的通知的 ID
        db.refresh(db_notification)
    # 返回更新后的通知对象
    return db_notification


def delete_notification(db: Session, notification_id: int) -> bool:
    # 查询一个指定的通知对象
    db_notification = db.query(Notification).filter(Notification.notification_id == notification_id).first()
    if db_notification:
        # 将通知对象从 Session 中删除
        db.delete(db_notification)
        # 提交 Session，将删除后的通知从数据库中删除
        db.commit()
        # 返回 True 表示删除成功
        return True
    # 返回 False 表示删除失败
    return False


def get_uncheck_notification(db: Session, target_user_id, check=False):
    uncheck_notification = db.query(Notification).filter(Notification.target_user_id == target_user_id).filter(
        Notification.is_check == check).all()
    return uncheck_notification


def get_notification_date(db: Session, target_user_id, create_at):
    notification = db.query(Notification).filter(Notification.target_user_id == target_user_id).filter(
        func.date(Notification.created_at) == create_at).all()
    return notification
