from app.crud.student import *
from app.crud.student_course import get_student_course_rank
from .user import *
from app.crud import student_course as sc
from app.crud import course as c
from app import schemas
import datetime
import re
from app.models import models
from .notification import send_notification

studentCourseRouter = APIRouter()


@studentCourseRouter.post("/student_courses/", response_model=schemas.StudentCourseModel)
def create_student_course_api(student_course_create: schemas.StudentCourseCreate, db: Session = Depends(get_db),
                              user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)

    if get_role_obj(db, userinfo.role).name == "学生":
        student_course_create.student_id = userinfo.associated_id
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
def read_student_courses_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                             user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    courses = jsonable_encoder(sc.get_student_courses_by_student_id(db=db, skip=skip, limit=limit))
    d = {}
    for i in courses:
        try:
            d["department_name"] = get_department_by_id(db, i.get("department_id")).name
            i.update(d)
        except:
            pass
    total = sc.get_student_course_count(db, userinfo.associated_id)
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


@studentCourseRouter.put("/update_grade/{student_id}/{course_id}", response_model=schemas.StudentCourseModel)
def update_student_grade_api(student_id: str, course_id: str, student_course_update: schemas.StudentCourseUpdate,
                             db: Session = Depends(get_db), user: UsernameRole = Depends(get_cure_user_by_token), ):
    db_student_course = sc.update_student_grade(db=db, student_id=student_id, course_id=course_id,
                                                student_course_update=student_course_update)

    send_notification(db=db,
                      title=f'您的课程:{get_course_by_id(db,db_student_course.course_id).name}  成绩已更新! 成绩为：{db_student_course.grade}'
                      , student_id=student_id, user=user)

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
    colors = []
    values = []
    labels = []
    if get_role_obj(db, userinfo.role).name == '学生':
        courses_count = sc.get_student_course_count(db, userinfo.associated_id)
        fail_count = sc.get_student_fail_count(db, userinfo.associated_id)
        grade_course = sc.get_student_course_have_grade_count(db, userinfo.associated_id)
        if grade_course != 0:
            fail_percent = f"{(1 - (fail_count / grade_course)) * 100:.2f}%"
        else:
            fail_percent = f"0%"
        total_credits = sc.get_student_credits(db, userinfo.associated_id)
        # 使用示例：
        colors = ["bg-blue-400", "bg-red-400", "bg-red-300", "bg-green-400"]
        values = [courses_count, fail_count, fail_percent, total_credits]
        labels = ["选课门数", "不及格的门数", "课程通过率", "共选学分"]
    else:
        courses_count = len(c.get_course_by_teacher_id(db, userinfo.associated_id))
        colors = ["bg-gree-400"]
        values = [courses_count]
        labels = ["我管理的课程数量"]

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
def get_role_courses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), semester: Optional[str] = None,
                     word: Optional[str] = None,
                     user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if get_role_obj(db, userinfo.role).name == "学生":
        courses = jsonable_encoder(
            sc.get_student_courses_by_student_id(db=db, student_id=userinfo.associated_id, skip=skip, limit=limit))

    else:
        courses = jsonable_encoder(
            sc.get_teacher_courses_by_teacher_id(db=db, teacher_id=userinfo.associated_id, skip=skip, limit=limit))

    d = {}
    for i in courses:
        try:
            d["course_info"] = jsonable_encoder(c.get_course_by_id(db, i.get("course_id")))
            teacher_id = d.get("course_info").get("teacher_id")
            course_department_id = d.get("course_info").get("department_id")
            d["teacher_info"] = jsonable_encoder(get_teacher_by_id(db, teacher_id))
            d["department_name"] = jsonable_encoder(get_department_by_id(db, course_department_id).name)
            d["rank"] = jsonable_encoder(
                get_student_course_rank(db, student_id=i.get("student_id"), course_id=i.get("course_id")))
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


@studentCourseRouter.get("/student_course/get_students", response_model=List[schemas.StudentCourseModel])
def get_student_by_courses(
        course_id: str,
        skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
        word: Optional[str] = None,
):
    students = jsonable_encoder(
        sc.get_student_by_course_id(db=db, course_id=course_id, skip=skip, limit=limit))

    d = {}
    for i in students:
        try:
            department_id = i.get("department_id")
            student_id = i.get("student_id")

            d["department_name"] = jsonable_encoder(get_department_by_id(db, department_id).name)
            d["student_grade"] = jsonable_encoder(sc.get_student_courses_by_id(db, student_id, course_id).grade)
            i.update(d)
        except:
            pass
    if word:
        # 将 JSON 字符串转换为 Python 列表
        # 定义结果列表
        result_re = []
        # 遍历列表中的每个元素
        for item in students:
            # 使用 re.search 函数判断 name 值是否包含指定的字符串
            if re.search(word, item["name"]):
                # 如果是，就将该元素添加到结果列表中
                result_re.append(item)
        # 打印结果列表
        students = result_re

    total = len(students)
    data = {"list": students, "total": total}
    return reponse(data=data)


@studentCourseRouter.get("/student/get_course_statistics")
def get_student_courses_statistics(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                                   semester: Optional[str] = 'all',
                                   user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if get_role_obj(db, userinfo.role).name == "学生":
        courses = jsonable_encoder(
            sc.get_student_courses_by_student_id(db=db, student_id=userinfo.associated_id, skip=skip, limit=limit))
        # 创建两个空列表，用于存储课程名称和学生成绩
        course_names = []
        student_grades = []
        for i in courses:
            try:
                # 获取课程名称和学生成绩，并添加到对应的列表中
                course = c.get_course_by_id(db, i.get("course_id"))
                course_semester = course.semester
                if course_semester == semester or semester == 'all':
                    student_grade = sc.get_student_courses_by_id(db, userinfo.associated_id, i.get("course_id")).grade
                    if student_grade is None:
                        continue
                    course_names.append(course.name)
                    student_grades.append(student_grade)
            except:
                continue
        # 将 data 字典中的 x 键的值改为 course_names 列表，y 键的值改为 student_grades 列表
        data = {"x": course_names, "y": student_grades}
        sorted_data = sorted(zip(data["x"], data["y"]), key=lambda x: x[1], reverse=True)
        # 将排序后的元组列表拆分成两个列表，分别赋值给 data 字典中的 x 和 y 键
        try:
            data["x"], data["y"] = zip(*sorted_data)
            return reponse(data=data)
        except:
            return reponse(data='no data')
    elif get_role_obj(db, userinfo.role).name == "院系管理员":
        department_id = get_teacher_by_id(db, userinfo.associated_id).department_id
        department_name = get_department(db, department_id).name
        men_count = get_department_student_gender(db, department_id,
                                                  gender='男')
        women_count = get_department_student_gender(db, department_id,
                                                    gender='女')
        data = [{"value": len(men_count), "name": "男生数量"}, {"value": len(women_count), "name": "女生数量"}]
        title = f'{jsonable_encoder(department_name)}男女比例图'

    else:
        title = '全体学生男女比例'
        men_count = get_students_by_gender(db, '男')
        women_count = get_students_by_gender(db, '女')
        data = [{"value": len(men_count), "name": "男生数量"}, {"value": len(women_count), "name": "女生数量"}]

    ret = {
        "title": {
            "text": title,
            "name": title,
        },
        "data": data
    }

    return reponse(data=ret)


@studentCourseRouter.get("/student/get_selection_course", response_model=List[schemas.StudentCourseModel])
def get_selection(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), semester: Optional[str] = None,
                  word: Optional[str] = None,
                  user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if get_role_obj(db, userinfo.role).name == "学生":
        courses = jsonable_encoder(
            c.get_student_selection_course(db=db, student_id=userinfo.associated_id, semester=semester, skip=skip,
                                           limit=limit))
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
