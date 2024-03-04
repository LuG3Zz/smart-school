from .user import *
from app.crud import leave_school as ls
import re

from app.schemas.leave_school import LeaveSchoolSchemasCreate, LeaveSchoolSchemasUpdate, LeaveSchoolSchemas
from .notification import send_notification

# 定义 leave_school 表对应的 crud 操作
LeaveSchoolRouter = APIRouter()  # 创建一个 APIRouter 实例


@LeaveSchoolRouter.post("/LeaveSchool/", )  # 创建一个 POST 路由，用于创建一个新的离校办理
def create_leave_school_api(leave_school_create: LeaveSchoolSchemasCreate, db: Session = Depends(get_db),
                            user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if get_role_obj(db, userinfo.role).name == "学生":
        leave_school_create.student_id = userinfo.associated_id

        leave_school = jsonable_encoder(ls.create_leave_school(db=db, leave_school_create=leave_school_create))
        return reponse(data=leave_school)


@LeaveSchoolRouter.get("/LeaveSchool/{application_id}", )  # 创建一个 GET 路由，用于读取一个指定的离校办理
def read_leave_school_api(application_id: int, db: Session = Depends(get_db)):
    db_leave_school = ls.get_leave_school_detail(db=db, application_id=application_id)
    if db_leave_school is None:
        raise HTTPException(status_code=404, detail="LeaveSchool not found")
    return reponse(data=jsonable_encoder(db_leave_school))


@LeaveSchoolRouter.get("/LeaveSchool", response_model=List[LeaveSchoolSchemas])  # 创建一个 GET 路由，用于读取所有的离校办理
def read_leave_schools_api(word:str=None,tab: str = None, leave_type: str = None, skip: int = 0, limit: int = 10,
                           db: Session = Depends(get_db),
                           user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    count = 0
    if get_role_obj(db, userinfo.role).name == "学生":
        leave_schools = jsonable_encoder(
            ls.get_leave_school_by_student_id(db=db, student_id=userinfo.associated_id, skip=skip, limit=limit))
        count = len(ls.get_leave_school_by_student_id(db=db, student_id=userinfo.associated_id, skip=skip, limit=10000))
    else:
        leave_schools = jsonable_encoder(
            ls.get_leave_school_all(db=db, skip=skip, limit=limit))
        count = len(ls.get_leave_school_all(db=db, skip=skip, limit=99999))
    d = {}
    for i in leave_schools:
        try:
            d["auditor_name"] = get_teacher_by_id(db, i.get("auditor_id")).name
            i.update(d)
        except:
            pass
    if tab != "all" and tab is not None:
        condition = lambda x: x['LeaveSchool']["application_status"] == tab
        leave_schools = list(filter(condition, leave_schools))
    if leave_type:
        condition = lambda x: x['LeaveSchool']["leave_type"] == leave_type
        leave_schools = list(filter(condition, leave_schools))
    if word:
        result_re = []
        # 遍历列表中的每个元素
        for item in leave_schools:
            # 使用 re.search 函数判断 name 值是否包含指定的字符串
            if re.search(word, item["t_name"]):
                # 如果是，就将该元素添加到结果列表中
                result_re.append(item)
        # 打印结果列表
        leave_schools = result_re

    total = count
    data = {"list": leave_schools, "total": total}
    return reponse(data=data)


@LeaveSchoolRouter.put("/{application_id}", response_model=LeaveSchoolSchemas)  # 创建一个 PUT 路由，用于更新一个指定的离校办理
def update_leave_school_api(application_id: int, leave_school_update: LeaveSchoolSchemasUpdate,
                            db: Session = Depends(get_db), user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if get_role_obj(db, userinfo.role).name != '学生':
        try:
            leave_school_update.auditor_id = userinfo.associated_id
            db_leave_school = ls.update_leave_school(db=db, application_id=application_id,
                                                     leave_school_update=leave_school_update)
            if leave_school_update.application_status in ["已通过", "已驳回"]:
                title = f"您的{db_leave_school.leave_type}{leave_school_update.application_status}"
                send_notification(title=title, student_id=leave_school_update.student_id, user=user, db=db)
        except:
            raise HTTPException(status_code=404, detail="该学生不存在")
        if db_leave_school is None:
            raise HTTPException(status_code=404, detail="LeaveSchool not found")
        return reponse(data=jsonable_encoder(db_leave_school))
    else:
        leave_school_update.application_status = '待审核'
        try:
            db_leave_school = ls.update_leave_school(db=db, application_id=application_id,
                                                     leave_school_update=leave_school_update)
        except:
            raise HTTPException(status_code=404, detail="该学生不存在")
        return reponse(data=jsonable_encoder(db_leave_school))


@LeaveSchoolRouter.delete("/{application_id}")  # 创建一个 DELETE 路由，用于删除一个指定的离校办理
def delete_leave_school_api(application_id: int, db: Session = Depends(get_db)):
    success = ls.delete_leave_school(db=db, application_id=application_id)
    if not success:
        raise HTTPException(status_code=404, detail="LeaveSchool not found")
    return reponse(data=jsonable_encoder(success))


@LeaveSchoolRouter.get("/leave_school")
def get_leaves(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), tab: Optional[str] = None,
               word: Optional[str] = None, leave_type: Optional[str] = None,
               user: UsernameRole = Depends(get_cure_user_by_token)):
    # 获取用户信息
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    # 判断用户角色
    if get_role_obj(db, userinfo.role).name == "学生":
        # 调用读取学生的离校申请的函数
        leaves = jsonable_encoder(
            ls.get_leave_school_by_student_id(db=db, student_id=userinfo.associated_id, skip=skip, limit=limit))
    elif get_role_obj(db, userinfo.role).name == "院系管理员":
        # 调用读取院系的离校申请的函数
        leaves = jsonable_encoder(
            ls.get_leave_school_by_department_id(db=db, department_id=get_teacher_by_id(db,
                                                                                        userinfo.associated_id).department_id,
                                                 skip=skip, limit=limit))
    else:
        # 调用读取所有的离校申请的函数
        leaves = jsonable_encoder(
            ls.get_leave_school_all(db=db, skip=skip, limit=limit))
    # 根据条件过滤申请
    if tab != "all" and tab is not None:
        condition = lambda x: x['LeaveSchool']["status"] == tab
        leaves = list(filter(condition, leaves))
    if word:
        result_re = []
        for item in leaves:
            if re.search(word, item["t_name"]):
                result_re.append(item)
        leaves = result_re
    if leave_type:
        result_re = []
        for item in leaves:
            if re.search(leave_type, item["LeaveSchool"]['leave_type']):
                result_re.append(item)
        leaves = result_re
    # 返回申请列表和总数
    total = len(leaves)
    data = {"list": leaves, "total": total}
    return reponse(data=data)
