from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, DateTime, Text, BLOB, Boolean, Enum
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


# 学工事务记录表
class StudentRecord(Base):
    __tablename__ = 'student_records'
    record_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(20), ForeignKey('students.student_id'))
    record_type = Column(String(50))
    details = Column(Text)
    created_at = Column(DateTime)
    auditor = Column(Integer, ForeignKey('teachers.teacher_id'))
    status = Column(String(10), nullable=False, default='待审核')  # 状态，字符串类型，非空，默认值为'待审核'
    # 添加一个相关材料字段，类型为 html 值
    content = Column(Text)


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
    position = Column(String(50), ForeignKey('roles.name'))
    specialization = Column(String(100))


# 课程信息表
class Course(Base):
    __tablename__ = 'courses'
    course_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    credits = Column(Integer)
    semester = Column(String(20))  # 添加学期字段
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    teacher_id = Column(Integer, ForeignKey('teachers.teacher_id'))


# 学生课程表
class StudentCourse(Base):
    __tablename__ = 'student_courses'
    enrollment_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(20), ForeignKey('students.student_id'))
    course_id = Column(Integer, ForeignKey('courses.course_id'))
    grade = Column(Integer)


# 宿舍信息表
class Dormitory(Base):
    __tablename__ = 'dormitories'
    dormitory_id = Column(Integer, primary_key=True, index=True)
    dorm_number = Column(String(20))
    floor = Column(Integer)
    capacity = Column(Integer)
    current_occupancy = Column(Integer)
    contact_phone = Column(String(20))
    grade = Column(Integer, default=0)


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
    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    content = Column(Text)
    created_at = Column(DateTime)
    target_user_id = Column(Integer, ForeignKey('users.user_id'))
    publisher_id = Column(Integer, ForeignKey('teachers.teacher_id'))
    is_check = Column(Boolean, default=False)


class Role(Base):
    '''角色表'''
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=8), unique=True, index=True)  # 角色名称


class StudentDiscipline(Base):
    __tablename__ = 'student_disciplines'
    discipline_id = Column(Integer, primary_key=True, autoincrement=True)  # 添加自增属性
    student_id = Column(String(20), ForeignKey('students.student_id'))  # 添加外键属性
    discipline_type = Column(String(50))  # 添加非空属性
    discipline_date = Column(Date)  # 添加日期属性
    discipline_detail = Column(Text)  # 添加文本属性
    discipline_result = Column(String(50))  # 添加非空属性
    handler_id = Column(Integer, ForeignKey('teachers.teacher_id'))


# 定义一个映射类
class Image(Base):
    # 指定表名为 images
    __tablename__ = 'images'
    # 定义一个 id 字段，整数类型，主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.user_id'))
    # 定义一个 url 字段，字符串类型，非空，长度为 255，用来存储图像的网址
    url = Column(String(255), nullable=False)
    # 定义一个 name 字段，字符串类型，非空，长度为 255，用来存储图像的名称
    name = Column(String(255), nullable=False)
    # 定义一个 path 字段，字符串类型，非空，长度为 255，用来存储图像的路径
    path = Column(String(255), nullable=False)
    # 定义一个 create_time 字段，日期时间类型，非空，用来存储图像的创建时间
    create_time = Column(DateTime, nullable=False)
    # 定义一个 update_time 字段，日期时间类型，非空，用来存储图像的更新时间
    update_time = Column(DateTime, nullable=False)
    # 定义一个 image_class_id 字段，整数类型，非空，用来存储图像的分类编号
    image_class_id = Column(String(50), nullable=False)


class LeaveSchool(Base):
    # 表名
    __tablename__ = "leave_school"
    # 申请编号，主键，自增
    application_id = Column(Integer, primary_key=True, autoincrement=True)
    # 学生学号，外键，关联学生表
    student_id = Column(String(20), ForeignKey("students.student_id"))
    # 个人信息，JSON格式，包括姓名、性别、身份证号等
    leave_type = Column(Enum("毕业离校", "退学离校", "休学离校","放假离校"))
    # 离校原因，文本格式
    leave_reason = Column(Text)
    # 离校时间，日期格式
    leave_date = Column(Date)
    # 申请状态，枚举类型，可取值为'待审核'，'已通过'，'已驳回'
    application_status = Column(Enum("待审核", "已通过", "已驳回"), nullable=False, default='待审核')
    # 审核人员，外键，关联院系负责人表
    auditor_id = Column(Integer, ForeignKey("departments.head_id"))


Base.metadata.create_all(bind=engine)
