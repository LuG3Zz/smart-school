from sqlalchemy.orm import Session
from app.models.models import Dormitory as DBDormitory  # 假设这是我们的SQLAlchemy宿舍模型
from app.schemas.dormitory import DormitoryCreate


def create_dormitory(db: Session, dormitory_create: DormitoryCreate) -> DBDormitory:
    db_dormitory = DBDormitory(**dormitory_create.dict())
    db.add(db_dormitory)
    db.commit()
    db.refresh(db_dormitory)
    return db_dormitory


def get_dormitory(db: Session, dormitory_id: str) -> DBDormitory:
    return db.query(DBDormitory).filter(DBDormitory.dormitory_id == dormitory_id).first()


def get_dormitories(db: Session, skip: int = 0, limit: int = 10) -> list[DBDormitory]:
    return db.query(DBDormitory).offset(skip).limit(limit).all()


def update_dormitory(db: Session, dormitory_id: str, dormitory_update: DormitoryCreate) -> DBDormitory:
    db_dormitory = db.query(DBDormitory).filter(DBDormitory.dormitory_id == dormitory_id).first()
    if db_dormitory:
        update_data = dormitory_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_dormitory, key, value)
        db.commit()
        db.refresh(db_dormitory)
    return db_dormitory


def delete_dormitory(db: Session, dormitory_id: str) -> bool:
    db_dormitory = db.query(DBDormitory).filter(DBDormitory.dormitory_id == dormitory_id).first()
    if db_dormitory:
        db.delete(db_dormitory)
        db.commit()
        return True
    return False
