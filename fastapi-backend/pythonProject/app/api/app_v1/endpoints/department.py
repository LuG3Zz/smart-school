from app.crud import department as crud
from app.crud.student import get_department_by_id
from .user import *
from app.schemas.department import *
from app.common.jsontools import *
import re

departmentRouter = APIRouter()


@departmentRouter.post("/departments/", response_model=DepartmentAll)
def create_department_api(department_create: DepartmentCreate, db: Session = Depends(get_db)):
    try:
        db_department = crud.create_department(db=db, department_create=department_create)
    except:
        resp_400(data="教师不存在")
    return reponse(data=jsonable_encoder(db_department))


@departmentRouter.get("/departments/{department_id}", response_model=DepartmentAll)
def read_department_api(department_id: str, db: Session = Depends(get_db)):
    db_department = crud.get_department(db=db, department_id=department_id)
    if db_department is None:
        return resp_400(message="Department not found")
    return reponse(data=jsonable_encoder(db_department))


@departmentRouter.get("/departments/", response_model=List[DepartmentAll])
def read_departments_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    departments = crud.get_departments(db=db, skip=skip, limit=limit)

    return reponse(data=jsonable_encoder(departments))


@departmentRouter.put("/departments/{department_id}", response_model=DepartmentAll)
def update_department_api(department_id: str, department_update: DepartmentUpdate, db: Session = Depends(get_db)):
    db_department = crud.update_department(db=db,  department_update=department_update)
    if db_department is None:
        return resp_400(message="Department not found")
    return reponse(data=jsonable_encoder(db_department))


@departmentRouter.delete("/departments/{department_id}")
def delete_department_api(department_id: str, db: Session = Depends(get_db)):
    try:
        success = crud.delete_department(db=db, department_id=department_id)
    except:
        return resp_400(data="删除失败,院系已和其他学生关联")
    if not success:
        return resp_400(message="Department not found")
    return reponse(code=200, data=f"Deleted department {department_id}", message="Department deleted successfully")


@departmentRouter.post(path='/department/statistics')
async def get_department_statistics(request: Request, user: UsernameRole = Depends(get_cure_user_by_token),
                                 db: Session = Depends(get_db)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if get_role_obj(db, userinfo.role).name == "院系管理员":
        department_count = crud.get_department_all(db)
        # 使用示例：
        colors = ["bg-blue-400"]
        values = [department_count]
        labels = ["共有学院"]
        if len(colors) != len(values) or len(values) != len(labels):
            raise ValueError('Input lists must all be the same size')
        panels = []
        for index in range(len(colors)):
            panels.append({
                'color': colors[index],
                'value': values[index],
                'label': labels[index]
            })
        statistics = {"panels": panels}
        print('panels', statistics)
        return reponse(data=jsonable_encoder(statistics))


@departmentRouter.get("/department/get_department")
def get_department_info(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                        user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if get_role_obj(db, userinfo.role).name in['院系管理员','学生处管理员']:
        departments = jsonable_encoder(
            crud.get_departments(db=db,  skip=skip, limit=limit))

        d = {}
        for i in departments:
            try:
                d["department_student"] = jsonable_encoder(crud.get_department_students_count(db, i.get("department_id")))
                d["teacher_info"] = jsonable_encoder(get_teacher_by_id(db, i.get("head_id")))
                i.update(d)
            except:
                pass
        total = len(departments)
        data = {"list": departments, "total": total}
        return reponse(data=data)