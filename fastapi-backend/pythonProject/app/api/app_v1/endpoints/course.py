from fastapi.encoders import jsonable_encoder

from .user import *
from app.crud import course as c
from app import schemas

courseRouter = APIRouter()


@courseRouter.get("/courses/{course_id}", response_model=schemas.Course)
def read_course(course_id: str, db: Session = Depends(get_db)):
    db_course = c.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return reponse(data=jsonable_encoder(db_course))


@courseRouter.get("/courses/", response_model=list[schemas.Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = c.get_courses(db, skip=skip, limit=limit)
    if course is None:
        raise HTTPException(status_code=404, detail="Courses not found")
    return reponse(data=courses)


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


@courseRouter.post("/student_courses/", response_model=schemas.StudentCourseModel)
def create_student_course_api(student_course_create: schemas.StudentCourseCreate, db: Session = Depends(get_db)):
    return reponse(data=jsonable_encoder(c.create_student_course(db=db, student_course_create=student_course_create)))


@courseRouter.get("/student_courses/{enrollment_id}", response_model=schemas.StudentCourseModel)
def read_student_course_api(enrollment_id: str, db: Session = Depends(get_db)):
    db_student_course = c.get_student_course(db=db, enrollment_id=enrollment_id)
    if db_student_course is None:
        raise HTTPException(status_code=404, detail="StudentCourse not found")
    return reponse(data=jsonable_encoder(db_student_course))


@courseRouter.get("/student_courses/", response_model=List[schemas.StudentCourseModel])
def read_student_courses_api(student_id: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    courses = c.get_student_courses(db=db, student_id=student_id, skip=skip, limit=limit)
    return reponse(data=jsonable_encoder(courses))


@courseRouter.put("/student_courses/{enrollment_id}", response_model=schemas.StudentCourseModel)
def update_student_course_api(enrollment_id: str, student_course_update: schemas.StudentCourseUpdate,
                              db: Session = Depends(get_db)):
    db_student_course = c.update_student_course(db=db, enrollment_id=enrollment_id,
                                                student_course_update=student_course_update)
    if db_student_course is None:
        raise HTTPException(status_code=404, detail="StudentCourse not found")
    return reponse(data=jsonable_encoder(db_student_course))


@courseRouter.delete("/student_courses/{enrollment_id}")
def delete_student_course_api(enrollment_id: str, db: Session = Depends(get_db)):
    success = c.delete_student_course(db=db, enrollment_id=enrollment_id)
    if not success:
        raise HTTPException(status_code=404, detail="StudentCourse not found")
    return reponse(code=200, data=f"Deleted StudentCourse {enrollment_id}",
                   message="StudentCourse deleted successfully")
