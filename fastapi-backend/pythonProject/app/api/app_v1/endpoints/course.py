from fastapi.encoders import jsonable_encoder

from app.crud.student import get_department_by_id
from app.crud.teacher import get_teacher_by_id

from .user import *
from app.crud import course as c
from app import schemas

courseRouter = APIRouter()


@courseRouter.get("/courses/{course_id}", response_model=schemas.Course)
def read_course(course_id: str, db: Session = Depends(get_db)):
    db_course = c.get_course_by_id(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return reponse(data=jsonable_encoder(db_course))


@courseRouter.get("/courses/", response_model=list[schemas.Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = jsonable_encoder(c.get_courses(db, skip=skip, limit=limit))
    d = {}
    for course in courses:
        try:
            d["department_name"] = get_department_by_id(db, course.get("department_id")).name
            d['teacher_name'] = get_teacher_by_id(db, course.get("teacher_id")).name
            course.update(d)
        except:
            pass
    total = c.get_courses_count(db)
    data = {"list": courses, "total": total}
    if course is None:
        raise HTTPException(status_code=404, detail="Courses not found")
    return reponse(data=data)


@courseRouter.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = c.create_course(db, course=course)
    if db_course is None:
        raise HTTPException(status_code=404, detail="课程创建失败")
    return reponse(data=jsonable_encoder(db_course))


@courseRouter.put("/courses/{course_id}", response_model=schemas.Course)
def update_course(course_id: str, course: schemas.CourseUpdate, db: Session = Depends(get_db)):
    db_course = c.update_course(db, course_id=course_id, course=course)
    if db_course is None:
        raise HTTPException(status_code=404, detail="课程更新失败")
    return reponse(data=jsonable_encoder(db_course))


@courseRouter.delete("/courses/{course_id}", response_model=schemas.Course)
def delete_course(course_id: str, db: Session = Depends(get_db)):
    db_course = c.delete_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="课程删除失败")
    return reponse(data=jsonable_encoder(db_course))
