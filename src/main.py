from fastapi import FastAPI
from db import models
from db.database import engine
from routers import job, department, employee, kpis
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(job.router)
app.include_router(employee.router)
app.include_router(department.router)
app.include_router(kpis.router)

@app.get("/")
def root():
  return "Data Engeneering Challenge API!"

app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)

models.Base.metadata.create_all(engine)