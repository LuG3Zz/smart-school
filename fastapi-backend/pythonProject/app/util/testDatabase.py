from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.util.config import *
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://"+testusername+":"+testpassword+"@"+(testhost)+":"+str(testport)+"/"+testdb

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, encoding='utf8', echo=True
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
