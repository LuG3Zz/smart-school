from typing import Optional

from pydantic import Field, BaseModel


class RecordSchemas(BaseModel):
    student_id: Optional[str]
    record_type: Optional[str] = None
    details: Optional[str] = None
    created_at: Optional[str] = None
    auditor: Optional[int]
    status: Optional[str] = None
    record_id: Optional[int]


class RecordSchemasCreate(RecordSchemas):
    pass  # 创建时不需要提供 discipline_id


class RecordSchemasUpdate(RecordSchemas):
    content: Optional[str] = None
