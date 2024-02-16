from pydantic import BaseModel


# 宿舍基本信息模型，用于读取操作
class DormitoryBase(BaseModel):
    dorm_number: str
    floor: int
    capacity: int
    current_occupancy: int
    contact_phone: str


# 创建宿舍时的请求模型，不包含自动生成的ID
class DormitoryCreate(DormitoryBase):
    pass


# 宿舍的完整模型，包括自动生成的ID
class Dormitory(DormitoryBase):
    dormitory_id: int

    class Config:
        orm_mode = True
