from app.util.database import *
from app.util.testDatabase import TestingSessionLocal
from app.util.config import EVENT


def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_pro():
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接
    :return:
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


if EVENT == "test":
    get_db = get_test_db
else:
    get_db = get_db_pro
