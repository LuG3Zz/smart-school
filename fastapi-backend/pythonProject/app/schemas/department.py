from pydantic import BaseModel


class DepartmentBase(BaseModel):
    department_id:int
    name: str
    head_id: str
    contact_info: str


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(DepartmentBase):
    pass


class DepartmentAll(DepartmentBase):
    department_id: str

    class Config:
        orm_mode = True
