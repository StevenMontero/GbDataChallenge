from fastapi import HTTPException, status
from typing import List
from sqlalchemy.orm.session import Session
from routers.schemas import Employee
from .models import DbEmployee



def get_all(db: Session):
  return db.query(DbEmployee).all()

def create(db: Session, request: Employee):
    try:
        new_employee = DbEmployee(
            Id=Employee.id,
            Name=Employee.name,
            DateTime=Employee.date_time,
            DepartmentId=Employee.department_id,
            JobId=Employee.job_id
        )
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
        return Employee
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


def create_from_list(db: Session, request: List[Employee]):
    list_employee = [DbEmployee(Id=employee.id,
                           Name=employee.name,
                           DateTime=employee.date_time,
                           DepartmentId=employee.department_id,
                           JobId=employee.job_id)
                for employee in request]
    try:
        for job in list_employee:
            db.add(job)
            db.commit()
            db.refresh(job)
        return request
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
