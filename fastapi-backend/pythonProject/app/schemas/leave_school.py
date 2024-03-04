from typing import Optional

from pydantic import Field, BaseModel


class LeaveSchoolSchemas(BaseModel):
    application_id: Optional[int]
    student_id: Optional[str]
    leave_type: Optional[str] = None
    leave_reason: Optional[str] = '无'
    leave_date: Optional[str] = None
    application_status: Optional[str] = None
    auditor_id: Optional[int]


class LeaveSchoolSchemasCreate(LeaveSchoolSchemas):
    pass  # 创建时不需要提供 application_id


class LeaveSchoolSchemasUpdate(LeaveSchoolSchemas):
    pass  # 更新时不需要提供新的字段
