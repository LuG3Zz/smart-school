from .user import *
from app.crud import student_course as sc
from app import schemas

studentCourseRouter = APIRouter()


@studentCourseRouter.post("/student_courses/", response_model=schemas.StudentCourseModel)
def create_student_course_api(student_course_create: schemas.StudentCourseCreate, db: Session = Depends(get_db)):
    return reponse(data=jsonable_encoder(sc.create_student_course(db=db, student_course_create=student_course_create)))


@studentCourseRouter.get("/student_courses/{enrollment_id}", response_model=schemas.StudentCourseModel)
def read_student_course_api(enrollment_id: str, db: Session = Depends(get_db)):
    db_student_course = sc.get_student_course(db=db, enrollment_id=enrollment_id)
    if db_student_course is None:
        raise HTTPException(status_code=404, detail="StudentCourse not found")
    return reponse(data=jsonable_encoder(db_student_course))


@studentCourseRouter.get("/student_courses/", response_model=List[schemas.StudentCourseModel])
def read_student_courses_api(student_id: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    courses = sc.get_student_courses(db=db, student_id=student_id, skip=skip, limit=limit)
    return reponse(data=jsonable_encoder(courses))


@studentCourseRouter.put("/student_courses/{enrollment_id}", response_model=schemas.StudentCourseModel)
def update_student_course_api(enrollment_id: str, student_course_update: schemas.StudentCourseUpdate,
                              db: Session = Depends(get_db)):
    db_student_course = sc.update_student_course(db=db, enrollment_id=enrollment_id,
                                                 student_course_update=student_course_update)
    if db_student_course is None:
        raise HTTPException(status_code=404, detail="StudentCourse not found")
    return reponse(data=jsonable_encoder(db_student_course))


@studentCourseRouter.delete("/student_courses/{enrollment_id}")
def delete_student_course_api(enrollment_id: str, db: Session = Depends(get_db)):
    success = sc.delete_student_course(db=db, enrollment_id=enrollment_id)
    if not success:
        raise HTTPException(status_code=404, detail="StudentCourse not found")
    return reponse(code=200, data=f"Deleted StudentCourse {enrollment_id}",
                   message="StudentCourse deleted successfully")
