from datetime import date, datetime
from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional, List


class StudentBase(BaseModel):
    student_id: str
    name: str
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    department_id: Optional[str] = None
    major: Optional[str] = None
    class_: Optional[str] = None
    enrollment_date: Optional[date] = None
    contact_info: Optional[str] = None
    status: Optional[str] = None
class StudentCreate(StudentBase):
    pass


class StudentCreate(StudentBase):
    student_id: constr(max_length=20)


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    department_id: Optional[int] = None
    major: Optional[str] = None
    class_: Optional[str] = None
    enrollment_date: Optional[date] = None
    contact_info: Optional[str] = None
    status: Optional[str] = None
    photo:Optional[str]


class StudentInDB(StudentBase):
    pass


class TransferRequestBase(BaseModel):
    reason: str
    submit_date: datetime
    status: constr(max_length=20)


class TransferRequestUpdate(BaseModel):
    reason: Optional[str] = Field(None, description="调动原因")
    status: Optional[str] = Field(None, description="审核状态", max_length=20)

    # 假设更新操作不允许修改提交日期和学生ID，所以这里不包括它们

    class Config:
        schema_extra = {
            "example": {
                "reason": "更换专业",
                "status": "待审核"
            }
        }


class TransferRequestCreate(TransferRequestBase):
    student_id: constr(max_length=20)


class TransferRequestOut(TransferRequestBase):
    request_id: int
    student_id: constr(max_length=20)

    class Config:
        orm_mode = True


class DisciplineRecordBase(BaseModel):
    violation_date: date
    description: str
    penalty_level: constr(max_length=50)


class DisciplineRecordUpdate(BaseModel):
    violation_date: Optional[date] = None
    description: Optional[str] = None
    penalty_level: Optional[str] = Field(None, max_length=50)

    class Config:
        orm_mode = True


class DisciplineRecordCreate(DisciplineRecordBase):
    student_id: constr(max_length=20)


class DisciplineRecordOut(DisciplineRecordBase):
    record_id: int
    student_id: constr(max_length=20)

    class Config:
        orm_mode = True
