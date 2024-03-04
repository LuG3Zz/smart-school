from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.models import StudentCourse, Course, Student
from app.schemas import StudentCourseUpdate, StudentCourseCreate


def create_student_course(db: Session, student_course_create: StudentCourseCreate) -> StudentCourse:
    db_student_course = StudentCourse(**student_course_create.dict())
    db.add(db_student_course)
    db.commit()
    db.refresh(db_student_course)
    return db_student_course


def get_student_course(db: Session, enrollment_id: str) -> StudentCourse:
    return db.query(StudentCourse).filter(StudentCourse.enrollment_id == enrollment_id).first()


def get_student_course_count(db: Session, student_id: str) -> int:
    return db.query(StudentCourse).filter(StudentCourse.student_id == student_id).count()


def get_student_course_have_grade_count(db: Session, student_id: str) -> int:
    return db.query(StudentCourse).filter(StudentCourse.student_id == student_id).filter(
        StudentCourse.grade.isnot(None)).count()


def get_student_fail_count(db: Session, student_id: str) -> int:
    return db.query(StudentCourse).filter(StudentCourse.student_id == student_id).filter(
        StudentCourse.grade < '60').count()


def get_student_average_grade(db: Session, student_id: str) -> float:
    # 查询学生课程表中成绩为非空的课程的成绩的平均值
    return db.query(func.avg(StudentCourse.grade)).filter(StudentCourse.student_id == student_id).filter(
        StudentCourse.grade.isnot(None)).scalar()


def get_student_highest_grade_course(db: Session, student_id: str):
    # 查询学生课程表中成绩最高的课程
    return db.query(StudentCourse.grade).filter(StudentCourse.student_id == student_id).group_by(
        StudentCourse.enrollment_id, StudentCourse.student_id, StudentCourse.course_id, StudentCourse.grade).order_by(
        func.max(StudentCourse.grade).desc()).first()


# def get_student_course_rank(db: Session, student_id: str):
#    # 查询学生课程表中该学生在课程中的排名
#    return db.query(StudentCourse, func.rank().over(order_by=StudentCourse.grade.desc()).label('rank')).filter(StudentCourse.student_id == student_id).order_by(
#        StudentCourse.grade.desc()).all()


def get_student_credits(db: Session, student_id: str) -> int:
    total_credits = db.query(func.sum(Course.credits)).join(
        StudentCourse, Course.course_id == StudentCourse.course_id
    ).filter(
        StudentCourse.student_id == student_id
    ).scalar()
    return total_credits


def get_student_courses_by_student_id(db: Session, student_id: str, skip: int = 0, limit: int = 10):
    return db.query(StudentCourse).filter(StudentCourse.student_id == student_id).offset(skip).limit(limit).all()


def get_student_courses_by_id(db: Session, student_id: str, course_id: str):
    from sqlalchemy import and_
    # 返回符合条件的第一条记录
    return db.query(StudentCourse).filter(
        and_(StudentCourse.student_id == student_id, StudentCourse.course_id == course_id)).first()


def get_teacher_courses_by_teacher_id(db: Session, teacher_id: str, skip: int = 0, limit: int = 10):
    return db.query(Course).filter(Course.teacher_id == teacher_id).offset(skip).limit(limit).all()


def get_student_by_course_id(db: Session, course_id: str, skip: int = 0, limit: int = 10):
    student_id = [sc.student_id for sc in
                  db.query(StudentCourse.student_id).filter(StudentCourse.course_id == course_id).all()]
    return db.query(Student).filter(Student.student_id.in_(student_id)).offset(skip).limit(limit).all()


def update_student_course(db: Session, enrollment_id: str, student_course_update: StudentCourseUpdate) -> StudentCourse:
    db_student_course = db.query(StudentCourse).filter(StudentCourse.enrollment_id == enrollment_id).first()
    if db_student_course:
        update_data = student_course_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_student_course, key, value)
        db.commit()
        db.refresh(db_student_course)
    return db_student_course


def update_student_grade(db: Session, student_id: str, course_id: str, student_course_update: StudentCourseUpdate):
    db_student_course = db.query(StudentCourse).filter(StudentCourse.student_id == student_id).filter(
        StudentCourse.course_id == course_id).first()
    if db_student_course:
        setattr(db_student_course, 'grade', student_course_update.grade)
        db.commit()
        db.refresh(db_student_course)
    return db_student_course


def delete_student_course(db: Session, enrollment_id: str) -> bool:
    db_student_course = db.query(StudentCourse).filter(StudentCourse.enrollment_id == enrollment_id).first()
    if db_student_course:
        db.delete(db_student_course)
        db.commit()
        return True
    return False


def get_student_course_rank(db: Session, student_id: str, course_id: str):
    # 查询学生课程表中成绩不为空的课程
    query = db.query(StudentCourse).filter(StudentCourse.grade.isnot(None))

    # 查询学生在课程中的排名
    # 使用窗口函数 over() 和 rank() 来计算每个课程中的排名
    # 使用子查询来过滤出指定的学生和课程
    subquery = query.with_entities(StudentCourse.student_id, StudentCourse.course_id, StudentCourse.grade,
                                   func.rank().over(order_by=StudentCourse.grade.desc(),
                                                    partition_by=StudentCourse.course_id).label('rank')).subquery()
    result = db.query(subquery).filter(subquery.c.student_id == student_id, subquery.c.course_id == course_id).first()

    # 返回结果
    return result
