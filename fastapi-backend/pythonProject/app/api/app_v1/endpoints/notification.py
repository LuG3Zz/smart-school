from app.crud.student import get_student_by_userid
from .user import *
from app.crud import notification as nc
import re
import datetime
from app.schemas.notification import NotificationCreate, NotificationUpdate
from app.models.models import Notification

# 定义 notifications 表对应的 crud 操作
NotificationRouter = APIRouter()  # 创建一个 APIRouter 实例


def send_notification(db:Session,title:str, student_id:str, user: UsernameRole = Depends(get_cure_user_by_token)):
    new = NotificationCreate(
        target_user_id=student_id,
        title=title,
    )
    create_notification_api(new, db, user)


@NotificationRouter.post("/notification/", )  # 创建一个 POST 路由，用于创建一个新的通知
def create_notification_api(notification_create: NotificationCreate, db: Session = Depends(get_db),
                            user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    now = datetime.datetime.now()
    # 格式化时间
    created_at = now.strftime("%Y-%m-%d %H:%M:%S")
    target_user = get_user_by_id(db, str(notification_create.target_user_id))
    if target_user is not None:
        notification_create.target_user_id = target_user.user_id

    if get_role_obj(db, userinfo.role).name != "学生":
        notification_create.publisher_id = userinfo.associated_id
        notification_create.created_at = created_at
        try:
            notifications = jsonable_encoder(nc.create_notification(db=db, notification_create=notification_create))
        except:
            raise HTTPException(404, detail="用户不存在")
        return reponse(data=notifications)


@NotificationRouter.get("/Notification/{notification_id}", )  # 创建一个 GET 路由，用于读取一个指定的通知
def read_notification_api(notification_id: int, db: Session = Depends(get_db)):
    db_notification = nc.get_notification(db=db, notification_id=notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return reponse(data=jsonable_encoder(db_notification))


@NotificationRouter.get("/", )  # 创建一个 GET 路由，用于读取一个指定用户的所有通知
def read_notifications_api(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                           user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    notifications = jsonable_encoder(
        nc.get_notifications_by_target_user_id(db=db, target_user_id=userinfo.user_id, skip=skip, limit=limit))
    total = len(notifications)
    data = {"list": notifications, "total": total}
    return reponse(data=data)


@NotificationRouter.put("/{notification_id}", )  # 创建一个 PUT 路由，用于更新一个指定的通知
def update_notification_api(notification_id: int, notification_update: NotificationUpdate,
                            db: Session = Depends(get_db),
                            user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if get_role_obj(db, userinfo.role).name != '学生':
        if notification_update.is_check is True:
            notification_update.is_check = False
    try:
        db_notification = nc.update_notification(db=db, notification_id=notification_id,
                                                 notification_update=notification_update)
    except:
        raise HTTPException(status_code=404, detail="该用户不存在")
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return reponse(data=jsonable_encoder(db_notification))


@NotificationRouter.delete("/{notification_id}", )  # 创建一个 DELETE 路由，用于删除一个指定的通知
def delete_notification_api(notification_id: int, db: Session = Depends(get_db)):
    result = nc.delete_notification(db=db, notification_id=notification_id)
    if result:
        return reponse(data="Notification deleted successfully")
    else:
        raise HTTPException(status_code=404, detail="Notification not found")


@NotificationRouter.get("/notification_count")
def get_uncheck_notification_count(db: Session = Depends(get_db),
                                   user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    uncheck_notification_count = len(nc.get_uncheck_notification(db=db, target_user_id=userinfo.user_id))
    if uncheck_notification_count:
        return reponse(data={"total": uncheck_notification_count})
    else:
        pass


@NotificationRouter.get("/notification")
def get_role_notification(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                          tab: Optional[str] = None,
                          word: Optional[str] = None,
                          is_check: Optional[bool] = None,
                          user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if get_role_obj(db, userinfo.role).name != '学生':
        notifications = jsonable_encoder(nc.get_notifications_by_publisher_id(db, userinfo.associated_id))
    # 查询一个指定用户的所有通知
    else:
        notifications = jsonable_encoder(
            nc.get_notifications_by_target_user_id(db=db, target_user_id=userinfo.user_id, skip=skip, limit=limit))
    d = {}

    if tab != "all" and tab is not None:
        if tab == 'uncheck':
            condition = lambda x: x["is_check"] == False
            notifications = list(filter(condition, notifications))
        else:
            condition = lambda x: x["is_check"] == True
            notifications = list(filter(condition, notifications))
    for i in notifications:
        try:
            d["publisher"] = get_teacher_by_id(db, i.get("publisher_id")).name
            d["target_user"] = get_student_by_userid(db, i.get('target_user_id')).name
            i.update(d)
        except:
            pass
    # 如果有指定通知日期，过滤出符合条件的通知
    # 如果有指定关键词，过滤出标题或内容中包含关键词的通知
    if is_check:
        result_re = []
        for item in notifications:
            if item['is_check']:
                result_re.append(item)
        # 打印结果列表
        notifications = result_re

    if word:
        result_re = []
        for item in notifications:
            if re.search(word, item["title"]) or re.search(word, item["content"]):
                result_re.append(item)
        # 打印结果列表
        notifications = result_re
    # 计算通知的总数
    total = len(notifications)
    # 返回响应数据
    data = {"list": notifications, "total": total}
    return reponse(data=data)
