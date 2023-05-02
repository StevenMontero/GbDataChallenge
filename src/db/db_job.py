from fastapi import HTTPException, status
from typing import List
from sqlalchemy.orm.session import Session
from routers.schemas import Job
from .models import DbJob

def get_all(db: Session):
  return db.query(DbJob).all()

def create(db: Session, request: Job):
    try:
        new_job = DbJob(
            Id=request.id,
            Job=request.job)
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        return new_job
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))

def create_from_list(db: Session, request: List[Job]):
    list_job = [DbJob(Id=job.id,Job=job.job) for job in request]
    try:
        for job in list_job:
            db.add(job)
            db.commit()
            db.refresh(job)
        return request
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))

    