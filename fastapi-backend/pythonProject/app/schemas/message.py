from pydantic import BaseModel, Field
from typing import Optional, List


class MessageConent(BaseModel):
    id: int
    connect: str


class RebackMessConnet(MessageConent):
    rebackid: int


class Messages(BaseModel):
    id: int
    senduser: str
    acceptusers: str
    read: bool
    sendtime: str
    addtime: str
    context: str


class MessagePid(Messages):
    pid: int


class MessageOne(Messages):
    pid: List[MessagePid] = []
