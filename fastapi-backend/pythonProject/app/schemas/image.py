from datetime import datetime

from fastapi import File, UploadFile
from pydantic import BaseModel


class ImageSchema(BaseModel):
    # 定义一个 id 字段，整数类型，主键
    id: int
    # 定义一个 url 字段，字符串类型，非空，长度为 255，用来存储图像的网址
    url: str
    # 定义一个 name 字段，字符串类型，非空，长度为 255，用来存储图像的名称
    name: str
    # 定义一个 path 字段，字符串类型，非空，长度为 255，用来存储图像的路径
    path: str
    # 定义一个 create_time 字段，日期时间类型，非空，用来存储图像的创建时间
    create_time: datetime
    # 定义一个 image_class_id 字段，整数类型，非空，用来存储图像的分类编号
    image_class_id: int


class ImageUpload(BaseModel):
    img: UploadFile(...) = File(...)
    image_class_id: str


class ImageSchemaUpdate(BaseModel):
    # 定义一个 id 字段，整数类型，主键
    id: int
    # 定义一个 url 字段，字符串类型，非空，长度为 255，用来存储图像的网址
    url: str
    # 定义一个 name 字段，字符串类型，非空，长度为 255，用来存储图像的名称
    name: str
    # 定义一个 path 字段，字符串类型，非空，长度为 255，用来存储图像的路径
    path: str
    # 定义一个 create_time 字段，日期时间类型，非空，用来存储图像的创建时间
    # 定义一个 update_time 字段，日期时间类型，非空，用来存储图像的更新时间
    update_time: datetime
    # 定义一个 image_class_id 字段，整数类型，非空，用来存储图像的分类编号
    image_class_id: int
    update_time: datetime


class ImageClassSchemaCreate(BaseModel):
    name: str
