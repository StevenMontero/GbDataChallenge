from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import HiredbyJobDeparmentDesplay,HiringDepartmentDisplay
from db import db_kpis
from db.database import get_db
from typing import List

router = APIRouter(
  prefix='/kpis',
  tags=['post']
)

@router.get('/hiredkpiperquater', response_model=List[HiredbyJobDeparmentDesplay])
def get_all_hired_by_department_job(db: Session = Depends(get_db)):
  return db_kpis.get_all_hired_by_department_job(db)

@router.get('/hiringkpibydepartment', response_model=List[HiringDepartmentDisplay])
def get_all_hired_by_department_job(db: Session = Depends(get_db)):
  return db_kpis.get_hiring_department(db)