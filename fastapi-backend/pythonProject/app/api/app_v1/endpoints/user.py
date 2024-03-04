from fastapi import APIRouter, Request
from fastapi import Depends, HTTPException, Header
from fastapi.encoders import jsonable_encoder
from app.crud.student_course import get_student_credits, get_student_course_count, get_student_average_grade, \
    get_student_highest_grade_course
from app.crud.user import get_user_username, db_create_user, get_role_obj, get_info_by_username, get_user_by_id
from app.crud.student import get_student, get_teacher_by_id, get_all_student, get_teachers_by_department_id
from app.crud.department import *
from app.crud.studentdiscipline import *
from app.crud.record import *
from app.crud.notification import *
from app.crud.course import *
from app.schemas import *
from app.util.get_db import get_db
from sqlalchemy.orm import Session
from app.crud import  teacher

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
            "index": "0",
            "icon": "user",
            "children": [
                {"href": "/info", "icon": "InfoFilled", "name": "个人信息"},

                # {"href": "/academic-info", "icon": "notebook", "name": "学业信息"},
                {"href": "/discipline-search", "icon": "search", "name": "个人违纪处分查询"},
                {"href": "/notification", "icon": "edit", "name": "通知中心"}
            ]
        },
        {
            "name": "课程中心",
            "index": "1",
            "icon": "guide",
            "children": [
                {"href": "/courses-info", "icon": "notebook", "name": "课程信息"},
                {"href": "/course-selection", "icon": "notebook", "name": "课程选择"},
            ]
        },
        #{
        #    "name": "迎新管理",
        #    "index": "2",
        #    "icon": "guide",
        #    "children": [
        #        {"href": "/pre-registration", "icon": "edit", "name": "预报到登记"},
        #        {"href": "/pickup-storage", "icon": "van", "name": "接送与寄存申请"},
        #        {"href": "/information-service", "icon": "message", "name": "信息服务访问"}
        #    ]
        #},
        {
            "name": "学生工作",
            "index": "3",
            "icon": "school",
            "children": [
                {"href": "/affairs-record", "icon": "wallet", "name": "学工记录"},
                {"href": "/image", "icon": "edit", "name": "资料管理"}
            ]
        },
        {
            "name": "宿舍管理",
            "index": "4",
            "icon": "house",
            "children": [
                {"href": "/dormitory-info", "icon": "InfoFilled", "name": "住宿信息查询"},
            ]
        },
        {
            "name": "离校管理",
            "index": "6",
            "icon": "Van",
            "children": [
                #{"href": "/leaving-procedures-query", "icon": "list", "name": "离校事项查询"},
                {"href": "/checkout-process", "icon": "CirclePlus", "name": "离校办理"}
            ]
        }
    ],
    "departmentHead": [

        {
            "name": "院系管理",
            "index": "1",
            "icon": "document",
            "children": [
                {"href": "/info", "icon": "InfoFilled", "name": "个人信息"},
                {"href": "/departments-info-view", "icon": "monitor", "name": "院系信息查看"},
                {"href": "/students-list", "icon": "folder", "name": "院系学生列表管理"},
                {"href": "/image", "icon": "PictureFilled", "name": "资料管理"},
                {"href": "/notification", "icon": "edit", "name": "我发送的通知"}
            ]
        },
        # {
        #    "name": "迎新信息与活动",
        #    "index": "2",
        #    "icon": "bell",
        #    "children": [
        #        {"href": "/new-student-info", "icon": "info", "name": "新生信息服务"},
        #        {"href": "/orientation-activities", "icon": "flag", "name": "迎新活动查看"}
        #    ]
        # },
        {
            "name": "学生事务管理",
            "index": "3",
            "icon": "school",
            "children": [
                {"href": "/discipline-search", "icon": "DocumentDelete", "name": "违纪记录查看"},
                {"href": "/affairs-record", "icon": "wallet", "name": "学工记录审核"},
                {"href": "/dormitory-info", "icon": "InfoFilled", "name": "住宿信息查询"},
            ]
        },
        #{
        #    "name": "学情测评与通报",
        #    "index": "4",
        #    "icon": "edit",
        #    "children": [
        #        {"href": "/evaluation-results", "icon": "form", "name": "学情测评结果"},
        #        {"href": "/health-reports", "icon": "heartbeat", "name": "学员健康报告"},
        #        {"href": "/announcements", "icon": "bullhorn", "name": "通报发布"}
        #    ]
        #},
        {
            "name": "数据分析与报告",
            "index": "5",
            "icon": "TrendCharts",
            "children": [
                {"href": "/student-analytics", "icon": "data-analysis", "name": "学员数据分析"},
                # {"href": "/course-attendance", "icon": "eye", "name": "上课出勤分析"},
                # {"href": "/performance-analysis", "icon": "data-analysis", "name": "成绩分析"}
            ]
        }
    ],
    "counselor": [
        {
            "name": "学生档案与信息",
            "index": "1",
            "icon": "document",
            "children": [
                {"href": "/student-management", "icon": "folder", "name": "学生信息管理"},
                {"href": "/record-lookup", "icon": "search", "name": "档案查询"},
                {"href": "/image", "icon": "edit", "name": "资料管理"}
            ]
        },
        {
            "name": "学生事务与服务",
            "index": "2",
            "icon": "school",
            "children": [
                {"href": "/affairs-record", "icon": "wallet", "name": "学工记录审核"},
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
            "name": "信息管理",
            "index": "1",
            "icon": "document",
            "children": [
                {"href": "/info", "icon": "InfoFilled", "name": "个人信息"},
                {"href": "/students-list", "icon": "folder", "name": "学生档案及信息管理"},
                {"href": "/discipline-search", "icon": "warning", "name": "违纪处分查询及添加"},
                {"href": "/departments-info-view", "icon": "monitor", "name": "院系信息查看"},
                {"href": "/notification", "icon": "edit", "name": "我发送的通知"}
            ]
        },
        {
            "name": "课程管理",
            "index": "2",
            "icon": "document",
            "children": [
                {"href": "/course-manager", "icon": "notebook", "name": "课程管理"},
                {"href": "/my-course-info-view", "icon": "memo", "name": "我管理的课程"},
            ]
        },
        {
            "name": "学生工作",
            "index": "3",
            "icon": "school",
            "children": [
                {"href": "/affairs-record", "icon": "wallet", "name": "学工记录审核"},
                {"href": "/image", "icon": "edit", "name": "资料管理"}
            ]
        },
        {
            "name": "宿舍管理",
            "index": "4",
            "icon": "house",
            "children": [
                {"href": "/dormitory-info", "icon": "InfoFilled", "name": "住宿信息管理"},
            ]
        },
        {
            "name": "离校管理",
            "index": "5",
            "icon": "van",
            "children": [
                # {"href": "/graduating-students", "icon": "graduation-cap", "name": "准毕业生管理"},
                # {"href": "/leaving-procedures", "icon": "list", "name": "离校事项管理"},
                {"href": "/checkout-process", "icon": "List", "name": "离校办理管理"}
            ]
        },
        {
            "name": "数据分析",
            "index": "6",
            "icon": "connection",
            "children": [
                {"href": "/student-analytics", "icon": "data-analysis", "name": "学员分析"},
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
    role_name = get_role_obj(db, user.role).name
    db_crest = get_user_username(db, user.username)
    if db_crest:
        raise HTTPException(status_code=404, detail="用户名重复")
    if len(user.username) < 8 or len(user.username) > 16:
        raise HTTPException(status_code=404, detail="用户名长度应该是8-16位")
    if role_name == "学生":
        if user.associated_id is None:
            raise HTTPException(status_code=404, detail="学生的学号不能为空")
        elif get_user_by_id(db, user.associated_id):
            raise HTTPException(status_code=404, detail="该学号已被绑定")

        elif get_student(db, student_id=user.associated_id) is None:
            raise HTTPException(status_code=404, detail="学生的学号不存在")
    if role_name != "学生":
        if user.associated_id is None:


            raise HTTPException(status_code=404, detail="工号不能为空")

        elif get_user_by_id(db, user.associated_id):
            raise HTTPException(status_code=404, detail="该工号已被绑定")
        elif get_teacher_by_id(db, teacher_id=user.associated_id) is None:
            raise HTTPException(status_code=404, detail="教师的工号不存在")
        else:
            try:
                if get_teacher_by_id(db, user.associated_id).position != role_name:
                    raise HTTPException(status_code=404, detail="教师的角色不匹配")
            except:
                raise HTTPException(status_code=404, detail="角色不匹配")
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
        userrole = get_role_obj(db, get_user_username(db, username).role).name
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
    data = {}
    try:
        department_name=get_department(db,user_info.get("department_id")).name
        user_info['department_name'] = department_name
        user_info['user_info']=jsonable_encoder(get_user_username(db,user.username))

    except:
        pass

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


@usersRouter.post(path='/get_usr_statistics')
async def get_student_statistics(request: Request, user: UsernameRole = Depends(get_cure_user_by_token),
                                 db: Session = Depends(get_db)):
    user_name = user.username

    userinfo = get_user_username(db, user_name)
    info = get_info_by_username(db, user_name)

    # 使用示例：

    if get_role_obj(db, userinfo.role).name == "学生":
        title = ["用户信息", "所属学院", "已选课程学分", "课程平均分"]
        try:
            value = [info.name, get_department(db, info.department_id).name, get_student_credits(db, info.student_id),
                     f"{get_student_average_grade(db, info.student_id):.2f}"]
        except:
            value = [info.name, get_department(db, info.department_id).name, "暂无数据",
                     "暂无数据"]
        unit = [get_role_obj(db, userinfo.role).name, f"学院编号:{info.department_id}", "学分", "成绩"]
        unitColor = ["success", "info", "success", "danger"]
        subTitle = ["用户名", "专业", "累计选课门数", "最高分"]
        try:
            subValue = [user.username, info.major, get_student_course_count(db, info.student_id),
                    get_student_highest_grade_course(db, info.student_id)["grade"]]
        except:
            subValue = [user.username, info.major, "",
                        '']

    if get_role_obj(db, userinfo.role).name == "院系管理员":
        title = ["用户信息", "所属学院", "院系数量", "院系教师"]
        value = [info.name, get_department(db, info.department_id).name, get_department_all(db),
                 len(get_teachers_by_department_id(db, info.department_id))]
        unit = [get_role_obj(db, userinfo.role).name, f"学院编号:{info.department_id}", "总计", "人数"]
        unitColor = ["success", "info", "success", "info"]
        subTitle = ["用户名", "学院人数", "当前学院开设课程", "处理的违纪处分记录"]
        subValue = [user.username, get_department_students_count(db, info.department_id),
                    len(get_course_by_department_id(db, info.department_id)),
                    len(get_disciplines_by_handler_id(db, userinfo.associated_id, limit=100))]
    if get_role_obj(db, userinfo.role).name == "学生处管理员":
        title = ["用户信息", "所属学院", "院系数量", "学生数量"]
        value = [info.name, get_department(db, info.department_id).name, get_department_all(db),
                 len(get_all_student(db))]
        unit = [get_role_obj(db, userinfo.role).name, f"学院编号:{info.department_id}", "总计", "人"]
        unitColor = ["success", "info", "success", "danger"]
        subTitle = ["用户名", "学院人数", "全校🏠", "课程数量"]
        subValue = [user.username, get_department_students_count(db, info.department_id), "", get_courses_count(db)]

    panels = []
    for index in range(len(title)):
        panels.append({
            'title': title[index],
            'value': value[index],
            'unit': unit[index],
            'unitColor': unitColor[index],
            'subTitle': subTitle[index],
            'subValue': subValue[index],
        })
    statistics = {"panels": panels}
    print('panels', statistics)
    return reponse(data=jsonable_encoder(statistics))


@usersRouter.post(path='/get_usr_statistics3')
async def get_student_statistics3(user: UsernameRole = Depends(get_cure_user_by_token),
                                  db: Session = Depends(get_db)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    info = get_info_by_username(db, user_name)
    # 使用示例：
    # 创建一个 Statistics 的实例
    notification = []
    record = []
    if get_role_obj(db, userinfo.role).name == "学生":
        record_count = get_record_count(db, info.student_id)
        record_pass = get_record_status_count(db, info.student_id, "通过")
        record_approval = get_record_status_count(db, info.student_id, "待审核")
        record_rejection = get_record_status_count(db, info.student_id, "拒绝")
        record.extend([
            {
                "label": "事务数",
                "value": record_count
            },
            {
                "label": "已通过",
                "value": len(record_pass)
            },
            {
                "label": "未通过",
                "value": len(record_rejection)
            },
            {
                "label": "待审核",
                "value": len(record_approval)
            },
        ])
        notification_check = get_uncheck_notification(db, userinfo.user_id, check=True)
        notification_uncheck = get_uncheck_notification(db, userinfo.user_id)
        notification_today = get_notification_date(db, target_user_id=userinfo.user_id,
                                                   create_at=datetime.today().strftime("%Y-%m-%d"))
        notification.extend([
            {
                "label": "通知数",
                "value": len(get_notifications_by_target_user_id(db, userinfo.user_id))
            },
            {
                "label": "未读",
                "value": len(notification_uncheck)
            },
            {
                "label": "已读",
                "value": len(notification_check)
            },
            {
                "label": "今日",
                "value": len(notification_today)
            },
        ]
        )
    elif get_role_obj(db, userinfo.role).name != "学生":
        # 根据你的业务逻辑，添加相应的数据到 statistics 的 goods 和 order 列表中
        # 例如，假设你要统计院系的教师信息，你可以这样做：
        record_count = get_record_by_auditor_id(db, info.teacher_id)
        record_pass = get_record_status_count(db, student_id=None, teacher_id=info.teacher_id, status="通过")
        record_approval = get_record_status_count(db, student_id=None, teacher_id=info.teacher_id, status="待审核")
        record_rejection = get_record_status_count(db, student_id=None, teacher_id=info.teacher_id, status="拒绝")
        record.extend([
            {
                "label": "事务数",
                "value": len(record_count)
            },
            {
                "label": "已通过",
                "value": len(record_pass)
            },
            {
                "label": "未通过",
                "value": len(record_rejection)
            },
            {
                "label": "待审核",
                "value": len(record_approval)
            },
        ])
        notification_send = get_notifications_by_publisher_id(db, info.teacher_id)
        notification.extend([{
            "label": "发送的公告数",
            "value": len(notification_send)
        }, ])
    # 返回 statistics 的 JSON 序列化
    return reponse(data={"record": record, "notification": notification})
