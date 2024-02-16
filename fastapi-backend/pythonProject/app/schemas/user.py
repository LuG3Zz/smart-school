from pydantic import BaseModel, Field
from typing import Optional, List


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password_hash: str
    role: str
    associated_id: Optional[str] = None


class UserLogin(UserBase):
    password: str


class UsersToken(UserBase):
    token: str


class UsernameRole(UserBase):
    role: str


class UserId(UserBase):
    user_id: str


class UserChangepassword(BaseModel):
    password: str
    newpassword: str


