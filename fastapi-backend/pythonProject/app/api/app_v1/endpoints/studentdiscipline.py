from .user import *
from app.crud import studentdiscipline as dc
import re
from .notification import send_notification

from app.schemas.studentdiscipline import StudentDisciplineCreate, Discipline
from app.schemas.studentdiscipline import StudentDisciplineUpdate

# 定义 disciplines 表对应的 crud 操作
DisciplineRouter = APIRouter()  # 创建一个 APIRouter 实例


@DisciplineRouter.post("/Discipline/", )  # 创建一个 POST 路由，用于创建一个新的违纪处分
def create_discipline_api(discipline_create: StudentDisciplineCreate, db: Session = Depends(get_db),
                          user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if get_role_obj(db, userinfo.role).name != "学生":
        discipline_create.handler_id = userinfo.associated_id

    try:
        discipline = jsonable_encoder(dc.create_discipline(db=db, discipline_create=discipline_create))
        send_notification(title=f"新增一条类型为{discipline_create.discipline_detail}的违纪记录",
                          student_id=discipline_create.student_id, user=user, db=db)
        return reponse(data=discipline)
    except:
        raise HTTPException(404, detail='添加失败')


@DisciplineRouter.get("/Discipline/{discipline_id}", )  # 创建一个 GET 路由，用于读取一个指定的违纪处分
def read_discipline_api(discipline_id: int, db: Session = Depends(get_db)):
    db_discipline = dc.get_discipline(db=db, discipline_id=discipline_id)
    if db_discipline is None:
        raise HTTPException(status_code=404, detail="Discipline not found")
    return reponse(data=jsonable_encoder(db_discipline))


@DisciplineRouter.get("/", response_model=List[Discipline])  # 创建一个 GET 路由，用于读取所有的违纪处分
def read_disciplines_api(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                         user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if get_role_obj(db, userinfo.role).name == "学生":
        disciplines = jsonable_encoder(
            dc.get_disciplines_by_student_id(db=db, student_id=userinfo.associated_id, skip=skip, limit=limit))
    else:
        disciplines = jsonable_encoder(
            dc.get_disciplines_by_handler_id(db=db, handler_id=userinfo.associated_id, skip=skip, limit=limit))

    d = {}
    for i in disciplines:
        try:
            d["handler_name"] = get_teacher_by_id(db, i.get("handler_id")).name
            i.update(d)
        except:
            pass
    total = len(get_discipline_results(db))
    data = {"list": disciplines, "total": total}
    return reponse(data=data)


@DisciplineRouter.put("/{discipline_id}", response_model=Discipline)  # 创建一个 PUT 路由，用于更新一个指定的违纪处分
def update_discipline_api(discipline_id: int, discipline_update: Discipline, db: Session = Depends(get_db)):
    try:
        db_discipline = dc.update_discipline(db=db, discipline_id=discipline_id, discipline_update=discipline_update)
    except:
        raise HTTPException(status_code=404, detail="该学生不存在")
    if db_discipline is None:
        raise HTTPException(status_code=404, detail="Discipline not found")
    return reponse(data=jsonable_encoder(db_discipline))


@DisciplineRouter.delete("/{discipline_id}")  # 创建一个 DELETE 路由，用于删除一个指定的违纪处分
def delete_discipline_api(discipline_id: int, db: Session = Depends(get_db)):
    success = dc.delete_discipline(db=db, discipline_id=discipline_id)
    if not success:
        raise HTTPException(status_code=404, detail="Discipline not found")
    return reponse(data=jsonable_encoder(success))


@DisciplineRouter.get("/discipline")
def get_role_discipline(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                        discipline_date: Optional[str] = None,
                        word: Optional[str] = None,
                        user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    count = 0
    if get_role_obj(db, userinfo.role).name == "学生":
        disciplines = jsonable_encoder(
            dc.get_disciplines_by_student_id(db=db, student_id=userinfo.associated_id, skip=skip, limit=limit))
        count = len(jsonable_encoder(
            dc.get_disciplines_by_student_id(db=db, student_id=userinfo.associated_id, skip=skip, limit=1000)))


    else:
        disciplines = jsonable_encoder(
            dc.get_disciplines_by_handler_id(db=db, handler_id=userinfo.associated_id, skip=skip, limit=limit))
        count = len(jsonable_encoder(
            dc.get_disciplines_by_handler_id(db=db, handler_id=userinfo.associated_id, skip=skip, limit=1000)))


    d = {}
    for i in disciplines:
        try:
            d["handler_name"] = get_teacher_by_id(db, i.get("handler_id")).name
            d["student_name"] = get_student(db, i.get("student_id")).name
            i.update(d)
        except:
            pass
    if discipline_date != "all" and discipline_date is not None:
        condition = lambda x: x["discipline_date"] == discipline_date
        disciplines = list(filter(condition, disciplines))
    if word:
        result_re = []
        if word.startswith("s:"):
            for item in disciplines:
                if re.search(word[2:], item["student_name"]):
                    result_re.append(item)
        else:
            for item in disciplines:
                if re.search(word, item["handler_name"]):
                    result_re.append(item)
        # 打印结果列表
        disciplines = result_re

    total = count
    data = {"list": disciplines, "total": total}
    return reponse(data=data)
