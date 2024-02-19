from app.crud.student import *
from .user import *
from app.crud import student_course as sc
from app.crud import course as c
from app import schemas
import datetime
import re
from app.models import models

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
    courses = jsonable_encoder(
        sc.get_student_courses_by_student_id(db=db, student_id=student_id, skip=skip, limit=limit))
    d = {}
    for i in courses:
        try:
            d["department_name"] = get_department_by_id(db, i.get("department_id")).name
            i.update(d)
        except:
            pass
    total = sc.get_student_course_count(db, student_id)
    data = {"list": courses, "total": total}
    return reponse(data=data)


@studentCourseRouter.get("/student_courses/", response_model=List[schemas.StudentCourseModel])
def read_student_courses_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    courses = jsonable_encoder(sc.get_student_courses_by_student_id(db=db, skip=skip, limit=limit))
    d = {}
    for i in courses:
        try:
            d["department_name"] = get_department_by_id(db, i.get("department_id")).name
            i.update(d)
        except:
            pass
    total = sc.get_student_course_count(db, student_id)
    data = {"list": courses, "total": total}
    return reponse(data=data)


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


@studentCourseRouter.post(path='/student/statistics')
async def get_student_statistics(request: Request, user: UsernameRole = Depends(get_cure_user_by_token),
                                 db: Session = Depends(get_db)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if get_role_obj(db, userinfo.role).name == '学生':
        courses_count = sc.get_student_course_count(db, userinfo.associated_id)
        fail_count = sc.get_student_fail_count(db, userinfo.associated_id)
        fail_percent = f"{(1 - fail_count / courses_count) * 100}%"
        total_credits = sc.get_student_credits(db, userinfo.associated_id)

        # 使用示例：
        colors = ["bg-blue-400", "bg-red-400", "bg-red-300", "bg-green-400"]
        values = [courses_count, fail_count, fail_percent, total_credits]
        labels = ["选课门数", "不及格的门数", "课程通过率", "共选学分"]
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


@studentCourseRouter.get("/student/get_course", response_model=List[schemas.StudentCourseModel])
def get_student_courses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), semester: Optional[str] = None,
                        word: Optional[str] = None,
                        user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if get_role_obj(db, userinfo.role).name == "学生":

        courses = jsonable_encoder(
            sc.get_student_courses_by_student_id(db=db, student_id=userinfo.associated_id, skip=skip, limit=limit))
        d = {}
        for i in courses:
            try:
                d["course_info"] = jsonable_encoder(c.get_course_by_id(db, i.get("course_id")))
                teacher_id = d.get("course_info").get("teacher_id")
                course_department_id = d.get("course_info").get("department_id")
                d["teacher_info"] = jsonable_encoder(get_teacher_by_id(db, teacher_id))
                d["department_name"] = jsonable_encoder(get_department_by_id(db, course_department_id).name)
                i.update(d)
            except:
                pass
        if semester != "all" and semester is not None:
            condition = lambda x: x["course_info"]["semester"] == semester
            courses = list(filter(condition, courses))

        if word:
            # 将 JSON 字符串转换为 Python 列表
            # 定义结果列表
            result_re = []
            # 遍历列表中的每个元素
            for item in courses:
                # 使用 re.search 函数判断 name 值是否包含指定的字符串
                if re.search(word, item["course_info"]["name"]):
                    # 如果是，就将该元素添加到结果列表中
                    result_re.append(item)
            # 打印结果列表
            courses = result_re

        total = len(courses)
        data = {"list": courses, "total": total}
        return reponse(data=data)
