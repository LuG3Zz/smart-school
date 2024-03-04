from app.crud import record as rd
from .notification import *
StudentRecordRouter = APIRouter()

@StudentRecordRouter.post("/record/")
def create_student_record_api(student_record_create: schemas.RecordSchemasCreate, db: Session = Depends(get_db),
                              user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    # 格式化时间
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if get_role_obj(db, userinfo.role).name == "学生":
        student_record_create.student_id = userinfo.associated_id
        student_record_create.created_at = created_at
    return reponse(data=jsonable_encoder(rd.create_record(db=db, record_create=student_record_create)))


@StudentRecordRouter.get("/record/{record_id}")
def read_record_detail_api(record_id: int, db: Session = Depends(get_db)):
    db_record = rd.get_record_detail(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Student record not found")
    return reponse(data=jsonable_encoder(db_record))


@StudentRecordRouter.put("/record/{record_id}", )
def update_student_record_api(record_id: int, record_update: RecordSchemasUpdate,
                              user: UsernameRole = Depends(get_cure_user_by_token),
                              db: Session = Depends(get_db)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if get_role_obj(db, userinfo.role).name != '学生':
        if record_update.status in ["通过", "拒绝"]:
            title= jsonable_encoder(rd.get_record_detail(db=db, record_id=record_id))["StudentRecord"]['details']
            new = NotificationCreate(
                target_user_id=record_update.student_id,
                title=f"您申请的{title}审核事务已{record_update.status}!",
            )
            create_notification_api(new, db, user)

        record_update.auditor = userinfo.associated_id
    elif get_role_obj(db, userinfo.role).name == '学生':
        record_update.student_id = userinfo.associated_id
        record_update.status = "待审核"
    db_record = rd.update_record(db=db, record_id=record_id, record_update=record_update)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Student record not found")
    return reponse(data=jsonable_encoder(db_record))


#
#
@StudentRecordRouter.delete("/record/")
def delete_student_record_api(record_id: List[int], db: Session = Depends(get_db)):
    for i in record_id:
        success = rd.delete_record(db=db, record_id=i)
        if not success:
            raise HTTPException(status_code=404, detail="record not found")
    return reponse(code=200, data=f"Deleted record {record_id},total:{len(record_id)}",
                   message="record deleted successfully")


@StudentRecordRouter.get("/get_records")
def get_role_record(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), tab: Optional[str] = None,
                    word: Optional[str] = None,
                    record_type: Optional[str] = None,
                    user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if get_role_obj(db, userinfo.role).name == "学生":
        records = jsonable_encoder(
            rd.get_record_by_student_id(db=db, student_id=userinfo.associated_id, skip=skip, limit=limit))

    elif get_role_obj(db, userinfo.role).name == "院系管理员":
        records = jsonable_encoder(
            rd.get_record_by_department_id(db, get_teacher_by_id(db, userinfo.associated_id).department_id))

    else:
        records = jsonable_encoder(
            rd.get_record_all(db=db, skip=skip, limit=limit))

    d = {}

    if tab != "all" and tab is not None:
        condition = lambda x: x['StudentRecord']["status"] == tab
        records = list(filter(condition, records))
    if word:
        # 将 JSON 字符串转换为 Python 列表
        # 定义结果列表
        result_re = []
        # 遍历列表中的每个元素
        for item in records:
            # 使用 re.search 函数判断 name 值是否包含指定的字符串
            if re.search(word, item["t_name"]):
                # 如果是，就将该元素添加到结果列表中
                result_re.append(item)
        # 打印结果列表
        records = result_re
    if record_type:
        result_re = []
        for item in records:
            if re.search(record_type, item["StudentRecord"]['record_type']):
                result_re.append(item)
        records = result_re

    total = len(records)
    data = {"list": records, "total": total}
    return reponse(data=data)

