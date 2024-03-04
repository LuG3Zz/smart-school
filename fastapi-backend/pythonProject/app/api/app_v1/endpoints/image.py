import datetime

from .user import *
from fastapi import Depends, HTTPException, Query, Form
from sqlalchemy.orm import Session
from app.models.models import Image
from app.schemas.image import *
from app.common.jsontools import *
import os

ImageRouter = APIRouter()


# 定义一个 GET 路由，用来获取所有的图像数据
@ImageRouter.get("/images/", response_model=List[ImageSchema])
def get_images(name: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
               user: UsernameRole = Depends(get_cure_user_by_token)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    # 从数据库中查询所有的图像记录
    images = db.query(Image).filter(Image.owner_id == userinfo.user_id).filter(Image.image_class_id == name).offset(
        skip).limit(limit).all()
    total = len(images)
    data = {'list': jsonable_encoder(images), 'total': total}

    # 返回图像列表
    return reponse(data=data)


# 定义一个 POST 路由，用来创建一个新的图像数据
@ImageRouter.post("/images/")
def create_image(image: ImageSchema, db: Session = Depends(get_db)):
    # 将新的图像对象添加到数据库会话中
    db.add(image)
    # 提交数据库会话，保存数据
    db.commit()
    # 刷新数据库会话，获取新的图像对象的 id
    db.refresh(image)
    # 返回新的图像对象
    return reponse(data=jsonable_encoder(image))


# 定义一个 GET 路由，用来获取指定 id 的图像数据
@ImageRouter.get("/images/{image_id}")
def get_image(image_id: int, db: Session = Depends(get_db)):
    # 从数据库中查询指定 id 的图像记录，如果不存在，抛出 404 异常
    image = db.query(Image).get(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    # 返回图像对象
    return reponse(data=jsonable_encoder(image))


# 定义一个 PUT 路由，用来更新指定 id 的图像数据
# @ImageRouter.put("/images/{image_id}", response_model=ImageSchema)
# def update_image(image_id: int, image: ImageSchema, db: Session = Depends(get_db)):
#    # 从数据库中查询指定 id 的图像记录，如果不存在，抛出 404 异常
#    image_in_db = db.query(Image).get(image_id)
#    if not image_in_db:
#        raise HTTPException(status_code=404, detail="Image not found")
#    # 根据输入的数据模型，更新图像对象的属性
#    image_in_db.url = image.url
#    image_in_db.name = image.name
#    image_in_db.path = image.path
#    image_in_db.create_time = image.create_time
#    image_in_db.update_time = image.update_time
#    image_in_db.image


@ImageRouter.post("/upload_file/")
async def upload_file(image_class_id: str = Form(...), img: UploadFile = File(...), db: Session = Depends(get_db),
                      user: UsernameRole = Depends(get_cure_user_by_token),
                      ):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    # 读取文件内容
    file_content = await img.read()
    path = f"../public/{userinfo.username}/{image_class_id}/"
    if not os.path.exists(path):
        # 如果不存在，创建 images 文件夹
        os.makedirs(path)
        # 保存文件到本地，文件名为上传文件的文件名
    with open(path + img.filename, "wb") as f:
        f.write(file_content)
    # 返回文件名和内容类型
    new_image = Image(
        owner_id=userinfo.user_id,
        url='http://127.0.0.1:8000' + path[2:] + img.filename,
        name=img.filename,
        path=path,
        create_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        update_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        image_class_id=image_class_id
    )
    create_image(db=db, image=new_image)
    return reponse(data={"filename": img.filename, "content_type": img.content_type})

    # do something with root, dirs, files


@ImageRouter.post("/create_image_class/")
async def create_image_class(image_class: ImageClassSchemaCreate, user: UsernameRole = Depends(get_cure_user_by_token),
                             db: Session = Depends(get_db)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    if not os.path.exists(f"../public/{userinfo.username}/{image_class.name}/"):
        # 如果不存在，创建 images 文件夹
        os.makedirs(f"../public/{userinfo.username}/{image_class.name}/")
    # 保存文件到本地，文件名为上传文件的文件名
    # 返回文件名和内容类型
    return reponse(data="ok")


@ImageRouter.get("/get_image_class/")
async def get_image_class(user: UsernameRole = Depends(get_cure_user_by_token),
                          db: Session = Depends(get_db),
                          page: int = Query(1, ge=1),  # 添加分页参数
                          size: int = Query(10, ge=1)):
    user_name = user.username
    userinfo = get_user_username(db, user_name)
    DIR = []  # 使用列表而不是字典
    if not os.path.exists(f"../public/{userinfo.username}/"):
        # 如果不存在，创建 images 文件夹
        os.makedirs(f"../public/{userinfo.username}/")
    # 遍历文件夹中的子目录
    for root, dirs, files in os.walk(f"../public/{userinfo.username}/"):
        for i, d in enumerate(dirs):
            # 为每个子目录创建一个字典，包含所需的字段和值
            sub_dir = {}
            sub_dir["id"] = i + 1  # id 可以从 1 开始递增
            sub_dir["name"] = d  # name 就是子目录的名称
            sub_dir["order"] = 50  # order 可以根据您的逻辑设置，这里假设都是 50
            sub_dir["images_count"] = len(os.listdir(os.path.join(root, d)))  # images_count 就是子目录中的文件数量
            # 将子目录的信息添加到列表中
            DIR.append(sub_dir)
    # 根据页码和每页数据量计算切片的起始和结束位置
    start = (page - 1) * size
    end = page * size
    # 从数据源中获取切片的数据
    items = DIR[start:end]
    # 返回文件名和内容类型
    return reponse(data={"list": items, "totalCount": len(DIR)})


@ImageRouter.delete("/delete_image/{id_}")
def delete_image_api(id_: int, db: Session = Depends(get_db)):
    success = delete_image(db=db, id=id_)
    if not success:
        raise HTTPException(status_code=404, detail="image not found")
    os.remove(success.path + success.name)

    return reponse(data=f"Deleted image success")


def delete_image(db: Session, id):
    # 查询一个指定的违纪处分对象
    db_image = db.query(Image).filter(Image.id == id).first()
    if db_image:
        # 将违纪处分对象从 Session 中删除
        db.delete(db_image)
        # 提交 Session，将删除后的违纪处分从数据库中删除
        db.commit()
        # 返回  表示删除成功
        return db_image
    # 返回 False 表示删除失败
    return None
