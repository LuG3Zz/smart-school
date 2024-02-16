from app.crud.dormitory import *
from app.schemas.dormitory import *
from .user import *

dormitoryRouter = APIRouter()


# 创建宿舍
@dormitoryRouter.post("/dormitories/", response_model=Dormitory)
def create_dormitory_api(dormitory_create: DormitoryCreate, db: Session = Depends(get_db)):
    db_dormitory = create_dormitory(db=db, dormitory_create=dormitory_create)
    return reponse(data=db_dormitory)


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
def update_dormitory_api(dormitory_id: str, dormitory_update: DormitoryCreate, db: Session = Depends(get_db)):
    db_dormitory = update_dormitory(db=db, dormitory_id=dormitory_id, dormitory_update=dormitory_update)
    if db_dormitory is None:
        raise HTTPException(status_code=404, detail="Dormitory not found")
    return reponse(data=db_dormitory)


# 删除宿舍
@dormitoryRouter.delete("/dormitories/{dormitory_id}", response_model=Dormitory)
def delete_dormitory_api(dormitory_id: str, db: Session = Depends(get_db)):
    success = delete_dormitory(db=db, dormitory_id=dormitory_id)
    if not success:
        raise HTTPException(status_code=404, detail="Dormitory not found")
    return reponse(code=200, data=f"Deleted dormitory {dormitory_id}", message="Dormitory deleted successfully")
