from fastapi import APIRouter, Request
from fastapi import Depends, HTTPException, Header
from fastapi.encoders import jsonable_encoder

from app.crud import user
from app.crud.user import get_user_username, db_create_user, get_role_name, get_info_by_username,get_user_by_id
from app.crud.student import  get_student
from app.schemas import *
from app.util.get_db import get_db
from sqlalchemy.orm import Session

from jose import JWTError, jwt
from passlib.context import CryptContext
from app.util.config import *
from app.common.jsontools import *
from app.common.logs import logger
import traceback
from datetime import datetime

usersRouter = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ROLE_TO_MENUS = {
    "student": [
        {
            "name": "个人中心",
            "index": "1",
            "icon": "user",
            "children": [
                {"href": "/", "icon": "menu", "name": "首页"},
                {"href": "/personal-info", "icon": "InfoFilled", "name": "个人信息"},
                {"href": "/academic-info", "icon": "notebook", "name": "学业信息"},
                {"href": "/security-settings", "icon": "search", "name": "个人违纪处分查询"}
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
    ],
    "departmentHead": [
        {
            "name": "学员信息查看",
            "index": "1",
            "icon": "document",
            "children": [
                {"href": "/", "icon": "menu", "name": "首页"},
                {"href": "/student-profiles", "icon": "folder-open", "name": "学生档案查看"},
                {"href": "/academic-performance", "icon": "bar-chart", "name": "学业成绩查看"},
                {"href": "/discipline-records", "icon": "warning-outline", "name": "违纪记录查看"}
            ]
        },
        {
            "name": "迎新信息与活动",
            "index": "2",
            "icon": "bell",
            "children": [
                {"href": "/new-student-info", "icon": "info", "name": "新生信息服务"},
                {"href": "/orientation-activities", "icon": "flag", "name": "迎新活动查看"}
            ]
        },
        {
            "name": "学生事务管理",
            "index": "3",
            "icon": "school",
            "children": [
                {"href": "/scholarship-audit", "icon": "medal", "name": "奖学金审核"},
                {"href": "/financial-aid-audit", "icon": "money", "name": "资助审核"}
            ]
        },
        {
            "name": "学情测评与通报",
            "index": "4",
            "icon": "edit",
            "children": [
                {"href": "/evaluation-results", "icon": "form", "name": "学情测评结果"},
                {"href": "/health-reports", "icon": "heartbeat", "name": "学员健康报告"},
                {"href": "/announcements", "icon": "bullhorn", "name": "通报发布"}
            ]
        },
        {
            "name": "数据分析与报告",
            "index": "5",
            "icon": "chart-pie",
            "children": [
                {"href": "/student-analytics", "icon": "analysis", "name": "学员数据分析"},
                {"href": "/course-attendance", "icon": "eye", "name": "上课出勤分析"},
                {"href": "/performance-analysis", "icon": "data-analysis", "name": "成绩分析"}
            ]
        }
    ],
    "counselor": [
        {
            "name": "学生档案与信息",
            "index": "1",
            "icon": "document",
            "children": [
                {"href": "/", "icon": "menu", "name": "首页"},
                {"href": "/student-management", "icon": "folder", "name": "学生信息管理"},
                {"href": "/record-lookup", "icon": "search", "name": "档案查询"}
            ]
        },
        {
            "name": "学生事务与服务",
            "index": "2",
            "icon": "school",
            "children": [
                {"href": "/id-card-issues", "icon": "credit-card", "name": "学生证办理"},
                {"href": "/campus-card-issues", "icon": "wallet", "name": "校园卡管理"},
                {"href": "/scholarship-management", "icon": "trophy", "name": "奖学金管理"},
                {"href": "/disciplinary-actions", "icon": "gavel", "name": "违纪管理"}
            ]
        },
        {
            "name": "宿舍与生活管理",
            "index": "3",
            "icon": "home",
            "children": [
                {"href": "/dormitory-management", "icon": "bed", "name": "宿舍信息管理"},
                {"href": "/repair-requests", "icon": "hammer", "name": "报修请求管理"},
                {"href": "/hygiene-inspections", "icon": "leaf", "name": "卫生检查"}
            ]
        },
        {
            "name": "离校与毕业管理",
            "index": "4",
            "icon": "exit",
            "children": [
                {"href": "/graduation-preparation", "icon": "graduation-cap", "name": "毕业生管理"},
                {"href": "/leaving-process", "icon": "list-alt", "name": "离校流程管理"}
            ]
        }
    ],
    "studentAdmin": [
        {
            "name": "学员信息管理",
            "index": "1",
            "icon": "document",
            "children": [
                {"href": "/", "icon": "menu", "name": "首页"},
                {"href": "/student-records", "icon": "folder", "name": "学生档案维护"},
                {"href": "/record-query", "icon": "search", "name": "档案查询"},
                {"href": "/student-transfer", "icon": "swap", "name": "学籍调动申请"},
                {"href": "/discipline-query", "icon": "warning", "name": "违纪处分查询"}
            ]
        },
        {
            "name": "迎新管理",
            "index": "2",
            "icon": "guide",
            "children": [
                {"href": "/pre-registration", "icon": "edit", "name": "预报到登记管理"},
                {"href": "/pickup-storage", "icon": "truck", "name": "接送与寄存管理"},
                {"href": "/information-service", "icon": "message", "name": "信息服务发布"},
                {"href": "/registration-process", "icon": "process", "name": "报到流程管理"},
                {"href": "/reception-activities", "icon": "flag", "name": "现场接待活动组织"}
            ]
        },
        {
            "name": "学生工作",
            "index": "3",
            "icon": "school",
            "children": [
                {"href": "/student-id-management", "icon": "id-card", "name": "学生证办理管理"},
                {"href": "/campus-card-recharge", "icon": "wallet", "name": "校园卡充值管理"},
                {"href": "/academic-records", "icon": "book", "name": "学籍成绩管理"},
                {"href": "/awards-penalties", "icon": "medal", "name": "奖惩管理"},
                {"href": "/financial-aid", "icon": "money", "name": "资助发放管理"},
                {"href": "/student-evaluation", "icon": "edit", "name": "学情测评发布"},
                {"href": "/student-health", "icon": "heartbeat", "name": "学员健康管理"},
                {"href": "/student-announcements", "icon": "bullhorn", "name": "学员通报"}
            ]
        },
        {
            "name": "宿舍管理",
            "index": "4",
            "icon": "home",
            "children": [
                {"href": "/dormitory-info", "icon": "info", "name": "住宿信息管理"},
                {"href": "/dormitory-hygiene", "icon": "leaf", "name": "宿舍卫生检查管理"},
                {"href": "/dormitory-discipline", "icon": "gavel", "name": "宿舍违纪管理"},
                {"href": "/dormitory-repair", "icon": "tools", "name": "宿舍报修管理"},
                {"href": "/network-service", "icon": "wifi", "name": "网络服务管理"},
                {"href": "/holiday-stay", "icon": "calendar", "name": "假期留校管理"}
            ]
        },
        {
            "name": "离校管理",
            "index": "5",
            "icon": "exit",
            "children": [
                {"href": "/graduating-students", "icon": "graduation-cap", "name": "准毕业生管理"},
                {"href": "/leaving-procedures", "icon": "list", "name": "离校事项管理"},
                {"href": "/checkout-management", "icon": "check-circle", "name": "离校办理管理"}
            ]
        },
        {
            "name": "数据分析",
            "index": "6",
            "icon": "chart-pie",
            "children": [
                {"href": "/student-portraits", "icon": "user", "name": "学员画像分析"},
                {"href": "/class-attendance", "icon": "eye-open", "name": "上课情况分析"},
                {"href": "/exam-results", "icon": "edit", "name": "考试成绩分析"},
                {"href": "/data-integration-analysis", "icon": "connection", "name": "数据集成与分析"}
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
    role_name = get_role_name(db, user.role).name
    if len(user.username) < 8 or len(user.username) > 16:
        raise HTTPException(status_code=404, detail="用户名长度应该是8-16位")
    if role_name  not in ["院系管理员", '学生', "辅导员", "学生处管理员"]:
        return reponse(code=100102, message="不存在该身份", data="")
    if role_name == "学生":
        if user.associated_id is None:
            raise HTTPException(status_code=404, detail="学生的学号不能为空")
        elif get_user_by_id(db,user.associated_id) is None:
            raise HTTPException(status_code=404, detail="该学号已被绑定")

        elif get_student(db, student_id=user.associated_id) is None:
            raise HTTPException(status_code=404, detail="学生的学号不存在")
    db_crest = get_user_username(db, user.username)
    if db_crest:
        return reponse(code=100104, message="用户名重复", data="")
    try:
        password_hash = get_password_hash(user.password_hash)
        user.password_hash = password_hash
    except Exception as e:
        logger.exception(e)
        return reponse(code=100105, data="", message="密码加密失败")
    try:
        user = db_create_user(db=db, user=user)
        logger.success("创建用户成功")
        return reponse(code=200, data={'user': user.username}, message="success")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=404, detail="注册失败")


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_cure_user_by_token(request: Request, token: Optional[str] = Header(...),
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
        userrole = get_role_name(db, get_user_username(db, username).role).name
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
    verifypassowrd = verify_password(user.password, db_crest.password_hash)
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


@usersRouter.get(path='/get_cur_user', response_model=UserBase)
async def get_current_user(user: UsernameRole = Depends(get_cure_user_by_token), db: Session = Depends(get_db)):
    user_info = jsonable_encoder(get_info_by_username(db, user.username))
    print("user_info", user_info)
    data = {}
    data['info'] = user_info

    if user.role == "学生":
        data['menu'] = ROLE_TO_MENUS.get("student")
    elif user.role == "院系管理员":
        data['menu'] = ROLE_TO_MENUS.get('departmentHead')
    elif user.role == "辅导员":
        data['menu'] = ROLE_TO_MENUS.get("counselor")
    elif user.role == '学生处管理员':
        data['menu'] = ROLE_TO_MENUS.get("studentAdmin")
    return reponse(code=200, message='成功', data=data)


@usersRouter.post(path='/change_password')
async def change_password(request: Request, user_change_pasword: UserChangepassword,
                          user: UsernameRole = Depends(get_cure_user_by_token),
                          db: Session = Depends(get_db)):
    if user_change_pasword.password == user_change_pasword.newpassword:
        return reponse(code=100304, message='新旧密码不能一样', data='')
    if len(user_change_pasword.newpassword) < 5 or len(user_change_pasword.newpassword) > 16:
        return reponse(code=100303, message='新密码长度不匹配', data='')
    username = user.username
    user_name = get_user_username(db, username)
    verify = verify_password(user_change_pasword.password, user_name.password_hash)
    if verify:
        hash_password = get_password_hash(user_change_pasword.newpassword)

        user_name.password_hash = hash_password
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
