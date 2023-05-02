from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from .schemas import Employee,EmployeeDesplay
from db import db_employee
from db.database import get_db
from typing import List
import csv
import codecs

router = APIRouter(
    prefix='/employee',
    tags=['post']
)



@router.get('/all', response_model=List[EmployeeDesplay])
def get_all_employees(db: Session = Depends(get_db)):
  return db_employee.get_all(db)

@router.post('/add', response_model=List[Employee])
def create(request: List[Employee], db: Session = Depends(get_db)):
    if len(request) > 1000:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="The batch of data allowed by request cannot be greater than 1000")
    return db_employee.create_from_list(db, request)


@router.post('/uploadcsv', response_model=List[Employee])
def upload_csv(csv_file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        csvReader = csv.DictReader(codecs.iterdecode(
            csv_file.file, 'utf-8'), fieldnames=['id', 'name', 'datetime', 'departmentid', 'jobid'])
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))

    list_departments = [Employee(id=employee['id'],
                                 name=employee['name'],
                                 date_time=employee['datetime'],
                                 department_id=employee['departmentid'],
                                 job_id=employee['jobid'])
                        for employee in csvReader]
    if len(list_departments) > 1000:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="The batch of data allowed by request cannot be greater than 1000")
    return db_employee.create_from_list(db, list_departments)
