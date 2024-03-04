import datetime
from app.crud.dormitory import *
from app.schemas.dormitory import *
from .user import *
import re

dormitoryRouter = APIRouter()


# 创建宿舍
@dormitoryRouter.post("/dormitories/", response_model=Dormitory)
def create_dormitory_api(dormitory_create: DormitoryCreate, db: Session = Depends(get_db)):
    db_dormitory = create_dormitory(db=db, dormitory_create=dormitory_create)
    return reponse(data=jsonable_encoder(db_dormitory))


# 读取单个宿舍信息
@dormitoryRouter.get("/dormitories/{dormitory_id}", response_model=Dormitory)
def read_dormitory_api(dormitory_id: str, db: Session = Depends(get_db)):
    db_dormitory = get_dormitory(db=db, dormitory_id=dormitory_id)
    if db_dormitory is None:
        raise HTTPException(status_code=404, detail="Dormitory not found")
    return reponse(data=db_dormitory)


# 读取宿舍列表
@dormitoryRouter.get("/dormitories/", response_model=List[Dormitory])
def read_dormitories_api(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    dormitories = get_dormitories(db=db, skip=skip, limit=limit)
    return reponse(data=dormitories)


# 更新宿舍信息
@dormitoryRouter.put("/dormitories/{dormitory_id}", response_model=Dormitory)
def update_dormitory_api(dormitory_id: str, dormitory_update: DormitoryUpdate, db: Session = Depends(get_db)):
    db_dormitory = update_dormitory(db=db, dormitory_id=dormitory_id, dormitory_update=dormitory_update)
    if db_dormitory is None:
        raise HTTPException(status_code=404, detail="Dormitory not found")
    return reponse(data=jsonable_encoder(db_dormitory))


# 删除宿舍
@dormitoryRouter.delete("/dormitories/{dormitory_id}", response_model=Dormitory)
def delete_dormitory_api(dormitory_id: str, db: Session = Depends(get_db)):
    try:
        success = delete_dormitory(db=db, dormitory_id=dormitory_id)
    except:
        raise HTTPException(404, detail='该宿舍存在学生无法删除')
    if not success:
        raise HTTPException(status_code=404, detail="Dormitory not found")
    return reponse(code=200, data=f"Deleted dormitory {dormitory_id}", message="Dormitory deleted successfully")


@dormitoryRouter.get("/get_dormitories")
def get_dormitories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), tab: Optional[str] = None,
                    word: Optional[str] = None,
                    user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if get_role_obj(db, userinfo.role).name == "学生":
        # 如果角色是学生，就根据学生 ID 查询宿舍信息
        dormitories = jsonable_encoder(
            get_dormitories_by_student_id(db=db, student_id=userinfo.associated_id, skip=skip, limit=limit))

    elif get_role_obj(db, userinfo.role).name == "院系管理员":
        # 如果角色是院系管理员，就根据院系 ID 查询宿舍信息
        dormitories = jsonable_encoder(
            get_dormitories_by_department_id(db=db,
                                             department_id=get_teacher_by_id(db, userinfo.associated_id).department_id,
                                             skip=skip, limit=limit))

    else:
        # 如果角色是学生处管理员，就查询所有的宿舍信息
        dormitories = jsonable_encoder(
            get_dormitories_all(db=db, skip=skip, limit=limit))

    d = {}
    for dorm in dormitories:
        d['students'] = jsonable_encoder(get_students_by_dormitory_id(db=db, dormitory_id=dorm['dormitory_id']))
        dorm.update(d)

    if tab != "all" and tab is not None:
        # 如果有指定的标签，就根据标签筛选宿舍信息
        condition = lambda x: x['Dormitory']["status"] == tab
        dormitories = list(filter(condition, dormitories))
    if word:
        # 如果有指定的关键词，就根据关键词搜索宿舍信息
        # 将 JSON 字符串转换为 Python 列表
        # 定义结果列表
        result_re = []
        # 遍历列表中的每个元素
        for item in dormitories:
            # 使用 re.search 函数判断 dorm_number 值是否包含指定的字符串
            if re.search(word, item["dorm_number"]):
                # 如果是，就将该元素添加到结果列表中
                result_re.append(item)
        # 打印结果列表
        dormitories = result_re

    total = len(dormitories)
    data = {"list": dormitories, "total": total}
    return reponse(data=data)


student_dormitoryRouter = APIRouter()


# 创建学生宿舍分配
@student_dormitoryRouter.post("/student_dormitories/")
def create_student_dormitory_api(student_dormitory_create: StudentDormitorySchemasCreate,
                                 db: Session = Depends(get_db)):
    create_at = date.today()
    if len(get_dormitories_by_student_id(db,student_dormitory_create.student_id))!=0:
        return HTTPException(404,detail='该学生已分配了宿舍')

    student_dormitory_create.assignment_date = create_at

    try:
        db_student_dormitory = create_student_dormitory(db=db, student_dormitory_create=student_dormitory_create)
    except:
        return HTTPException(404, detail='该学生不存在')
    return reponse(data=jsonable_encoder(db_student_dormitory))


# 读取单个学生宿舍分配信息
@student_dormitoryRouter.get("/student_dormitories/{assignment_id}")
def read_student_dormitory_api(assignment_id: int, db: Session = Depends(get_db)):
    db_student_dormitory = get_student_dormitory(db=db, assignment_id=assignment_id)
    if db_student_dormitory is None:
        raise HTTPException(status_code=404, detail="Student dormitory not found")
    return reponse(data=db_student_dormitory)


# 读取学生宿舍分配列表
@student_dormitoryRouter.get("/student_dormitories/", )
def read_student_dormitories_api(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    student_dormitories = get_student_dormitories(db=db, skip=skip, limit=limit)
    return reponse(data=student_dormitories)


# 更新学生宿舍分配信息
@student_dormitoryRouter.put("/student_dormitories/{assignment_id}", )
def update_student_dormitory_api(assignment_id: int, student_dormitory_update: StudentDormitorySchemasUpdate,
                                 db: Session = Depends(get_db)):
    db_student_dormitory = update_student_dormitory(db=db, assignment_id=assignment_id,
                                                    student_dormitory_update=student_dormitory_update)
    if db_student_dormitory is None:
        raise HTTPException(status_code=404, detail="Student dormitory not found")
    return reponse(data=jsonable_encoder(db_student_dormitory))


# 删除学生宿舍分配
@student_dormitoryRouter.delete("/student_dormitories/{assignment_id}")
def delete_student_dormitory_api(assignment_id: int, db: Session = Depends(get_db)):
    try:
        success = delete_student_dormitory(db=db, assignment_id=assignment_id)
    except:
        raise HTTPException(404, detail='该学生宿舍分配已经结束无法删除')
    if not success:
        raise HTTPException(status_code=404, detail="Student dormitory not found")
    return reponse(code=200, data=f"Deleted student dormitory {assignment_id}",
                   message="Student dormitory deleted successfully")
