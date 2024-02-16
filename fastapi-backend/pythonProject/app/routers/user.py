from fastapi import APIRouter, Request
from fastapi import Depends, HTTPException, Header
from app.util.get_db import get_db
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.util.config import *
from app.common import logger
import traceback
from datetime import datetime
from fastapi.encoders import jsonable_encoder

usersRouter = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ROLE_TO_MENUS ={
  "student": [
    {
      "name": "个人中心",
      "index": "1",
      "icon": "user",
      "children": [
        {"href": "/", "icon": "menu", "name": "首页"},
        {"href": "/personal-info", "icon": "InfoFilled", "name": "个人信息"},
        {"href": "/academic-info", "icon": "notebook", "name": "学业信息"},
        {"href": "/security-settings", "icon": "lock", "name": "安全设置"}
      ]
    },
    {
      "name": "迎新管理",
      "index": "2",
      "icon": "guide",
      "children": [
        {"href": "/pre-registration", "icon": "edit", "name": "预报到登记"},
        {"href": "/pickup-storage", "icon": "van", "name": "接送与寄存申请"},
        {"href": "/information-service", "icon": "message", "name": "信息服务访问"}
      ]
    },
    {
      "name": "学生工作",
      "index": "3",
      "icon": "school",
      "children": [
        {"href": "/campus-card-recharge", "icon": "wallet", "name": "校园卡充值"},
        {"href": "/academic-records", "icon": "book", "name": "学籍成绩查询"},
        {"href": "/awards-penalties", "icon": "medal", "name": "奖惩查询"},
        {"href": "/financial-aid-application", "icon": "money", "name": "资助申请"},
        {"href": "/student-evaluation-participation", "icon": "edit", "name": "学情测评参与"},
        {"href": "/student-health-update", "icon": "heartbeat", "name": "健康信息更新"}
      ]
    },
    {
      "name": "宿舍管理",
      "index": "4",
      "icon": "house",
      "children": [
        {"href": "/dormitory-info-query", "icon": "infofilled", "name": "住宿信息查询"},
        {"href": "/dormitory-hygiene-feedback", "icon": "leaf", "name": "宿舍卫生反馈"},
        {"href": "/dormitory-discipline-report", "icon": "gavel", "name": "宿舍违纪报告"},
        {"href": "/dormitory-repair-request", "icon": "tools", "name": "宿舍报修申请"},
        {"href": "/network-service-request", "icon": "wifi", "name": "网络服务申请"},
        {"href": "/holiday-stay-application", "icon": "calendar", "name": "假期留校申请"}
      ]
    },
    {
      "name": "离校管理",
      "index": "5",
      "icon": "Van",
      "children": [
        {"href": "/leaving-procedures-query", "icon": "list", "name": "离校事项查询"},
        {"href": "/checkout-process", "icon": "check-circle", "name": "离校办理"}
      ]
    }
  ]
}


    # 其他菜单配置...

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# 新建用户
@usersRouter.post("/create", tags=["users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info("创建用户")
    if len(user.username) < 8 or len(user.username) > 16:
        return reponse(code=100106, message="用户名长度应该是8-16位", data="")
    if user.age < 18:
        return reponse(code=100103, message="年纪大小不符合", data="")
    if (user.role == "学生" and user.student_id is None) or (user.role == "教师" and user.jobnum is None) or (
            user.role not in ["教师", '学生']):
        return reponse(code=100102, message="身份和对应号不匹配", data="")
    db_crest = get_user_username(db, user.username)
    if db_crest:
        return reponse(code=100104, message="用户名重复", data="")
    try:
        password = get_password_hash(user.password)
        user.password=password
    except Exception as e:
        logger.exception(e)
        return reponse(code=100105, data="", message="密码加密失败")
    try:
        user = db_create_user(db=db, user=user)
        logger.success("创建用户成功")
        return reponse(code=200, data={'user': user.username}, message="success")
    except Exception as e:
        logger.exception(e)
        return reponse(code=100101, data="", message="注册失败")


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_cure_user(request: Request, token: Optional[str] = Header(...),
                        db: Session = Depends(get_db)) -> UsernameRole:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="验证失败"
    )
    credentials_FOR_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="用户未登录或者登陆token已经失效"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        useris = await request.app.state.redis.get(username)
        if not useris and useris != token:
            raise credentials_FOR_exception
        userrole = get_role_name(db,get_user_username(db, username).role).name
        user = UsernameRole(username=username, role=userrole)
        return user
    except JWTError:
        logger.error(traceback.format_exc())
        raise credentials_exception


@usersRouter.post("/login")
async def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):
    db_crest = get_user_username(db, user.username)
    if not db_crest:
        logger.info("login：" + user.username + "不存在")
        return reponse(code=100205, message='用户不存在', data="")
    verifypassowrd = verify_password(user.password, db_crest.password)
    if verifypassowrd:
        useris = await request.app.state.redis.get(user.username)
        if not useris:
            try:
                token = create_access_token(data={"sub": user.username})
            except Exception as e:
                logger.exception(e)
                return reponse(code=100203, message='产生token失败', data='')
            await request.app.state.redis.set(user.username, token, expire=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
            return reponse(code=200, message='成功', data={"token": token})
        return reponse(code=200, message='成功', data={"token": useris})
    else:
        result = await  request.app.state.redis.hgetall(user.username + "_password", encoding='utf8')
        if not result:
            times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            request.app.state.redis.hmset_dict(user.username + "_password", num=0, time=times)
            return reponse(code=100206, data='', message='密码错误')
        else:
            errornum = int(result['num'])
            numtime = (datetime.now() - datetime.strptime(result['time'], '%Y-%m-%d %H:%M:%S')).seconds / 60
            if errornum < 10 and numtime < 30:
                # 更新错误次数
                errornum += 1
                request.app.state.redis.hmset_dict(user.username + "_password", num=errornum)
                return reponse(code=100206, data='', message='密码错误')
            elif errornum < 10 and numtime > 30:
                # 次数置于1，时间设置现在时间
                errornum = 1
                times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                request.app.state.redis.hmset_dict(user.username + "_password", num=errornum, time=times)
                return reponse(code=100206, data='', message='密码错误')
            elif errornum > 10 and numtime < 30:
                # 次数设置成最大，返回
                errornum += 1
                request.app.state.redis.hmset_dict(user.username + "_password", num=errornum)
                return reponse(code=100204, message='输入密码错误次数过多，账号暂时锁定，请30min再来登录', data='')
            else:
                errornum = 1
                times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                request.app.state.redis.hmset_dict(user.username + "_password", num=errornum, time=times)
                return reponse(code=100206, data='', message='密码错误')


@usersRouter.get(path='/getcuruser', response_model=UserBase)
async def getcuruser(user: UsernameRole = Depends(get_cure_user), db: Session = Depends(get_db)):
    user_name = get_user_username(db, username=user.username)
    data = {}
    data['username'] = user_name.username
    data['sex'] = user_name.sex
    data['age'] = user_name.age
    data['role'] = user.role

    if user.role == "学生":
        data['studentnum'] = user_name.student_id
        data['menu']=ROLE_TO_MENUS.get("student")

    else:
        data['jobnum'] = user_name.jobnum
    return reponse(code=200, message='成功', data=data)


@usersRouter.post(path='/changepassword')
async def changepassword(request: Request, userchangepasword: UserChangepassword,
                         user: UsernameRole = Depends(get_cure_user),
                         db: Session = Depends(get_db)):
    if userchangepasword.password == userchangepasword.newpassword:
        return reponse(code=100304, message='新旧密码不能一样', data='')
    if len(userchangepasword.newpassword) < 5 or len(userchangepasword.newpassword) > 16:
        return reponse(code=100303, message='新密码长度不匹配', data='')
    username = user.username
    user_name = get_user_username(db, username)
    verify = verify_password(userchangepasword.password, user_name.password)
    if verify:
        hashpassword = get_password_hash(userchangepasword.newpassword)

        user_name.password=hashpassword
        try:
            db.commit()
            db.refresh(user_name)
        except Exception as e:
            logger.exception(e)
            return reponse(code=100302, message='密码保存失败', data='')
        request.app.state.redis.delete(user.username)
        request.app.state.redis.delete(user.username + "_password")
        return reponse(code=200, message="成功", data=user.username)
    return reponse(code=100301, message='原密码校验失败', data='')


@usersRouter.post(path='/addmessage')
async def addmessage(messageconent: MessageConent,
                     user: UsernameRole = Depends(get_cure_user),
                     db: Session = Depends(get_db)):
    if len(messageconent.connect) > 500 or len(messageconent.connect) < 5:
        return reponse(code=100502, message='留言长度在5-500个字符长度', data='')
    user_name = get_user_username(db, user.username)
    rev_user = get_user(db, messageconent.id)
    if not rev_user:
        return reponse(code=100503, message='留言用户不存在', data='')
    if rev_user.id == user_name.id:
        return reponse(code=100501, message='自己不能给自己留言', data='')
    times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    message = Message(senduser=user_name.id,
                      acceptusers=rev_user.id,
                      context=messageconent.connect,
                      sendtime=times,addtime=times,read=False)
    db.add(message)
    db.commit()
    db.refresh(message)
    return reponse(code=200, message="成功", data='')


@usersRouter.get(path="/viewmessage")
async def viewmessage(id: int,
                      user: UsernameRole = Depends(get_cure_user),
                      db: Session = Depends(get_db)):
    useris=get_user_username(db,user.username)
    message = get_message(db, id)
    if not message:
        return reponse(code=100601, message='留言不存在', data='')
    if message.acceptusers != useris.id and message.senduser != useris.id:
        return reponse(code=100602, message='权限不足', data='')
    message.read = True
    db.commit()
    db.refresh(message)
    all_pid = get_pid_message(db, message.id)
    messageone = MessageOne(id=message.id,
                            senduser=get_user(db,message.senduser).username,
                            acceptusers=get_user(db, message.acceptusers).username,
                            read=message.read,
                            sendtime=message.sendtime,
                            addtime=str(message.addtime),
                            context=message.context)
    if len(all_pid) > 0:
        allpidlist = []
        for item in all_pid:
            message = MessagePid(id=message.id,
                                 senduser=get_user(db,item.senduser).username,
                                 acceptusers=get_user(db,item.acceptusers).username,
                                 read=item.read,
                                 sendtime=item.sendtime,
                                 addtime=str(item.addtime),
                                 context=item.context, pid=item.pid)
            allpidlist.append(message)
        messageone.pid = allpidlist
    return reponse(code=200, message='成功', data=jsonable_encoder(messageone))


@usersRouter.get(path="/messagelist")
async def messagelist(user: UsernameRole = Depends(get_cure_user),
                      db: Session = Depends(get_db)):
    users = get_user_username(db, user.username)
    messagelist = get_message_list(db=db, userid=users.id)
    message_list = []
    mainmessage = []
    if len(messagelist) > 0:
        for item in messagelist:
            if item.pid == "":
                messageone = MessageOne(id=item.id,
                                        senduser=get_user(db,item.senduser).username,
                                        acceptusers=get_user(db,item.acceptusers).username,
                                        read=item.read,
                                        sendtime=item.sendtime,
                                        addtime=str(item.addtime),
                                        context=item.context)
                mainmessage.append(messageone.id)
                all_pid = get_pid_message(db, item.id)
                if len(all_pid) > 0:
                    allpidlist = []
                    for items in all_pid:
                        message = MessagePid(id=item.id,
                                             senduser=get_user(db,items.senduser).username,
                                             acceptusers=get_user(db,items.acceptusers).username,
                                             read=items.read,
                                             sendtime=items.sendtime,
                                             addtime=str(items.addtime),
                                             context=items.context,
                                             pid=items.pid)
                        allpidlist.append(message)
                    messageone.pid = allpidlist
                message_list.append(messageone)
            else:
                if item.pid not in mainmessage:
                    message = get_message(db, item.pid)
                    if  message:
                        all_pid = get_pid_message(db, message.id)
                        messageone = MessageOne(id=message.id,
                                                senduser=get_user(db,message.senduser).username,
                                                acceptusers=get_user(db,message.acceptusers).username,
                                                read=message.read,
                                                sendtime=message.sendtime,
                                                addtime=str(message.addtime),
                                                context=message.context)
                        if len(all_pid) > 0:
                            allpidlist = []
                            for item in all_pid:
                                messagepid = MessagePid(id=message.id,
                                                        senduser=get_user(db,item.senduser).username,
                                                        acceptusers=get_user(db,item.acceptusers).username,
                                                        read=item.read,
                                                        sendtime=item.sendtime,
                                                        addtime=str(item.addtime),
                                                        context=item.context, pid=item.pid)
                                allpidlist.append(messagepid)
                            messageone.pid = allpidlist
                        message_list.append(messageone)
    return reponse(code=200, message='成功', data=jsonable_encoder(message_list))


@usersRouter.post(path='/rebackmessage')
async def rebackmessage(rebackmessage: RebackMessConnet, user: UsernameRole = Depends(get_cure_user),
                        db: Session = Depends(get_db)):
    if rebackmessage.connect == "":
        return reponse(code=100802, message='回复留言内容不能为空', data='回复留言内容不能为空')
    if len(rebackmessage.connect) > 500 or len(rebackmessage.connect) < 5:
        return reponse(code=100803, message='回复内容应该在5-500字', data='回复内容应该在5-500字')
    users = get_user_username(db, user.username)
    message = get_message(db, rebackmessage.rebackid)
    if not message:
        return reponse(code=100804, message='回复留言id不存在', data='回复留言id不存在')
    db_creat_rebackmessage(db, rebackmessage, users.id)
    return reponse(code=200, message='成功', data='成功')


@usersRouter.get(path='/deletemessage')
async def deletemessage(id: int, db: Session = Depends(get_db),
                        user: UsernameRole = Depends(get_cure_user)):
    messagse = get_message(db, id)
    useris=get_user_username(db,user.username)
    if not messagse:
        return reponse(code=100901, message='删除留言不存在', data='')
    if useris.id != messagse.acceptusers and useris.id != messagse.senduser:
        return reponse(code=100902, message='权限不足', data='')
    messagse.status = 1
    db.commit()
    db.refresh(messagse)
    return reponse(code=200, message='成功', data='成功')
