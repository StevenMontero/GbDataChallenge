from fastapi import HTTPException, status
from typing import List
from sqlalchemy.orm.session import Session
from routers.schemas import Department
from .models import DbDepartment


def get_all(db: Session):
  return db.query(DbDepartment).all()

def create(db: Session, request: Department):
    try:
        new_department = DbDepartment(
            Id=request.id,
            Department=request.department)
        db.add(new_department)
        db.commit()
        db.refresh(new_department)
        return Department
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    
def create_from_list(db: Session, request: List[Department]):
    list_department = [DbDepartment(Id=department.id,Department=department.department) for department in request]
    try:
        for department in list_department:
            db.add(department)
            db.commit()
            db.refresh(department)
        return request
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))

    