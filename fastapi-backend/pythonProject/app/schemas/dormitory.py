from typing import Optional

from pydantic import BaseModel


# 宿舍基本信息模型，用于读取操作
class DormitoryBase(BaseModel):
    dorm_number: str
    floor: int
    capacity: int
    current_occupancy: Optional[int] = 0
    contact_phone: str


# 创建宿舍时的请求模型，不包含自动生成的ID
class DormitoryCreate(DormitoryBase):
    pass


class DormitoryUpdate(BaseModel):
    floor: Optional[int]
    capacity: Optional[int]
    grade:Optional[int]
    current_occupancy: Optional[int] = 0
    contact_phone: Optional[str]


# 宿舍的完整模型，包括自动生成的ID
class Dormitory(DormitoryBase):
    dormitory_id: int

    class Config:
        orm_mode = True
