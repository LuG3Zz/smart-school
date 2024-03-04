# 定义通知表对应的 schemas 结构
from typing import Optional

from pydantic import BaseModel


class NotificationBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[str] = None
    target_user_id: Optional[int] = None
    publisher_id:Optional[int] = None


class NotificationCreate(NotificationBase):
    pass  # 创建时不需要提供 notification_id


class NotificationUpdate(NotificationBase):
    is_check:bool


