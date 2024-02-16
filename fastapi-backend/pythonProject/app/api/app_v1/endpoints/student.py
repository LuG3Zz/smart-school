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
def read_students_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = jsonable_encoder(get_students(db, skip=skip, limit=limit))
    d = {}
    for i in students:
        try:
            d["department_name"] = get_department_by_id(db,i.get("department_id")).name
            i.update(d)
        except:
            pass
        
    total = db.query(Student).count()
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
