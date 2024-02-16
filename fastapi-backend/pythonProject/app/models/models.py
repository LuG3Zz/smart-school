from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, DateTime, Text, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.util.config import EVENT

Base = declarative_base()
if EVENT == "test":
    from app.util.testDatabase import Base, engine
else:
    from app.util.database import Base, engine


# 学生信息表
class Student(Base):
    __tablename__ = 'students'
    student_id = Column(String(20), primary_key=True)
    name = Column(String(100))
    gender = Column(String(1))
    date_of_birth = Column(Date)
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    major = Column(String(50))
    class_ = Column(String(50))
    enrollment_date = Column(Date)
    contact_info = Column(String(100))
    photo = Column(Text)  # 使用Text类型存储Base64编码的图片
    status = Column(String(20))


# 学生档案表
class StudentRecord(Base):
    __tablename__ = 'student_records'
    record_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(20), ForeignKey('students.student_id'))
    record_type = Column(String(50))
    details = Column(Text)
    created_at = Column(DateTime)


# 院系与专业表
class Department(Base):
    __tablename__ = 'departments'
    department_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    head_id = Column(Integer, ForeignKey('teachers.teacher_id'))
    contact_info = Column(String(100))


# 教师信息表（此处添加以满足外键约束）
class Teacher(Base):
    __tablename__ = 'teachers'
    teacher_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    gender = Column(String(1))
    contact_info = Column(String(100))
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    position = Column(String(50))
    specialization = Column(String(100))


# 课程信息表
class Course(Base):
    __tablename__ = 'courses'
    course_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    credits = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    teacher_id = Column(Integer, ForeignKey('teachers.teacher_id'))


# 学生课程表
class StudentCourse(Base):
    __tablename__ = 'student_courses'
    enrollment_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(20), ForeignKey('students.student_id'))
    course_id = Column(Integer, ForeignKey('courses.course_id'))
    semester = Column(String(20))
    grade = Column(String(10))


# 宿舍信息表
class Dormitory(Base):
    __tablename__ = 'dormitories'
    dormitory_id = Column(Integer, primary_key=True, index=True)
    dorm_number = Column(String(20))
    floor = Column(Integer)
    capacity = Column(Integer)
    current_occupancy = Column(Integer)
    contact_phone = Column(String(20))


# 学生宿舍分配表
class StudentDormitory(Base):
    __tablename__ = 'student_dormitories'
    assignment_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(20), ForeignKey('students.student_id'))
    dormitory_id = Column(Integer, ForeignKey('dormitories.dormitory_id'))
    assignment_date = Column(Date)
    leave_date = Column(Date)


# 登录与权限表
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    password_hash = Column(String(255))  # 存储密码的哈希值
    role = Column(Integer)
    associated_id = Column(String(20))  # 根据角色关联到对应的ID，如学生ID或教师ID


# 事件与通知表
class Notification(Base):
    __tablename__ = 'notifications'
    notification_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content = Column(Text)
    created_at = Column(DateTime)
    target_user_id = Column(Integer, ForeignKey('users.user_id'))


class Role(Base):
    '''角色表'''
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=8), unique=True, index=True)  # 角色名称


Base.metadata.create_all(bind=engine)
