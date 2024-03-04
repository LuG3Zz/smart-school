import json

from app.crud.student import *
from .user import *
from app.common.jsontools import *
from fastapi.encoders import jsonable_encoder

studentRouter = APIRouter()


@studentRouter.post("/students/", response_model=StudentInDB)
def create_student_api(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = create_student(db, student)
    return reponse(data=jsonable_encoder(db_student))


@studentRouter.get("/students/", response_model=List[StudentInDB])
def read_students_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                      user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if get_role_obj(db, userinfo.role).name == '学生处管理员':
        students = jsonable_encoder(get_students(db, skip=skip, limit=limit))
    elif get_role_obj(db, userinfo.role).name in ['院系管理员', '辅导员']:
        students = jsonable_encoder(
            get_department_students(db, get_teacher_by_id(db, userinfo.associated_id).department_id, skip=skip,
                                    limit=limit))
    else:
        students = jsonable_encoder(get_students(db, student_id=userinfo.associated_id))

    d = {}
    for i in students:
        try:
            d["department_name"] = get_department_by_id(db, i.get("department_id")).name
            i.update(d)
        except:
            pass

    total = len(students)
    data = {"list": students, "total": total}

    return reponse(data=data)


@studentRouter.put("/students/{student_id}", response_model=StudentInDB)
def update_student_api(student_id: str, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = update_student(db, student_id, student)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return reponse(data=jsonable_encoder(db_student))


@studentRouter.delete("/students/{student_id}", response_model=StudentInDB)
def delete_student_api(student_id: str, db: Session = Depends(get_db)):
    try:
        db_student = delete_student(db, student_id)
    except:
        raise HTTPException(status_code=404, detail="该学生已经选课无法删除")
    else:
        if db_student is None:
            raise HTTPException(status_code=404, detail="Student not found")
    return reponse(data=jsonable_encoder(db_student))


@studentRouter.get("/get_analytics1")
def get_major_analytics_statistics(db: Session = Depends(get_db),
                                   user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    user = get_user_username(db, user_name)
    userinfo = get_info_by_username(db, user_name)
    p = get_major_percent(db)
    d = []
    ret = dict()
    title=''
    if get_role_obj(db, user.role).name == "院系管理员":
        for i in jsonable_encoder(p):
            if i.get("department_id") == userinfo.department_id:
                d.append(i)
        title=f'{get_department(db, userinfo.department_id).name}各专业人数占比'

    if get_role_obj(db, user.role).name == "学生处管理员":
        d = jsonable_encoder(p)
        title="全校各专业人数占比"

    ret = {
        "title": {
            "text":title ,
        },
        "data": d
    }

    return reponse(data=ret)
