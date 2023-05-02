from fastapi import APIRouter, Depends, status,UploadFile, File
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from .schemas import Department, DepartmentDesplay
from db import db_department
from db.database import get_db
from typing import List
import csv
import codecs

router = APIRouter(
  prefix='/deparmet',
  tags=['post']
)

@router.get('/all', response_model=List[DepartmentDesplay])
def get_all_departmens(db: Session = Depends(get_db)):
  return db_department.get_all(db)

@router.post('/add', response_model=List[Department])
def create(request: List[Department], db: Session = Depends(get_db)):
  if len(request) > 1000:
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, 
              detail="The batch of data allowed by request cannot be greater than 1000")
  return db_department.create_from_list(db, request)

@router.post('/uploadcsv',response_model=List[Department])
def upload_csv(csv_file: UploadFile = File(...),db: Session = Depends(get_db)):
    csvReader = csv.DictReader(codecs.iterdecode(csv_file.file, 'utf-8'),fieldnames=['id','department'])
    list_departments = [Department(id=row['id'],department=row['department']) for row in csvReader]
    if len(list_departments) > 1000:
      raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                detail="The batch of data allowed by request cannot be greater than 1000")
    return db_department.create_from_list(db, list_departments)