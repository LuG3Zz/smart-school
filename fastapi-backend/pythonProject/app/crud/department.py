from sqlalchemy.orm import Session
from app.models.models import Department
from app.schemas.department import *
from typing import  List


def create_department(db: Session, department_create: DepartmentCreate) -> DepartmentAll:
    db_department = Department(**department_create.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


def get_department(db: Session, department_id: str) -> DepartmentAll:
    return db.query(Department).filter(Department.department_id == department_id).first()


def get_departments(db: Session, skip: int = 0, limit: int = 10) -> List[DepartmentAll]:
    return db.query(Department).offset(skip).limit(limit).all()


def update_department(db: Session, department_id: str, department_update: DepartmentUpdate) -> DepartmentAll:
    db_department = db.query(Department).filter(Department.department_id == department_id).first()
    if db_department:
        update_data = department_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_department, key, value)
        db.commit()
        db.refresh(db_department)
    return db_department


def delete_department(db: Session, department_id: str) -> bool:
    db_department = db.query(Department).filter(Department.department_id == department_id).first()
    if db_department:
        db.delete(db_department)
        db.commit()
        return True
    return False
