from .database import Base
from sqlalchemy import Column,String,Integer,ForeignKey

class DbJob(Base):
    __tablename__ = "Job"
    Id = Column(Integer, primary_key = True)
    Job = Column(String)

class DbDepartment(Base):
    __tablename__ = "Department"
    Id = Column(Integer, primary_key = True)
    Department = Column(String)

class DbEmployee(Base):
    __tablename__ = "Employee"
    Id = Column(Integer, primary_key = True)
    Name = Column(String)
    DateTime = Column(String)
    DepartmentId = Column(Integer, ForeignKey("Department.Id"))
    JobId = Column(Integer, ForeignKey("Job.Id"))