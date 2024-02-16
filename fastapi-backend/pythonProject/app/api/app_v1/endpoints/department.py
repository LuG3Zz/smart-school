from app.crud import department as crud
from .user import *
from app.schemas.department import *
from app.common.jsontools import *

departmentRouter = APIRouter()


@departmentRouter.post("/departments/", response_model=DepartmentAll)
def create_department_api(department_create: DepartmentCreate, db: Session = Depends(get_db)):
    db_department = crud.create_department(db=db, department_create=department_create)
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
    db_department = crud.update_department(db=db, department_id=department_id, department_update=department_update)
    if db_department is None:
        return resp_400(message="Department not found")
    return reponse(data=jsonable_encoder(db_department))


@departmentRouter.delete("/departments/{department_id}", response_model=DepartmentAll)
def delete_department_api(department_id: str, db: Session = Depends(get_db)):
    success = crud.delete_department(db=db, department_id=department_id)
    if not success:
        return resp_400(message="Department not found")
    return reponse(code=200, data=f"Deleted department {department_id}", message="Department deleted successfully")
