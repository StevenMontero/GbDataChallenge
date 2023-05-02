from pydantic import BaseModel

class Job(BaseModel):
    id : int
    job : str

class Department(BaseModel):
    id : int
    department : str

class Employee(BaseModel):
    id : int 
    name : str 
    date_time : str
    department_id : int 
    job_id : int

class EmployeeDesplay(BaseModel):
    Id : int 
    Name : str 
    DateTime : str
    DepartmentId : int 
    JobId : int
    class Config():
        orm_mode = True

class JobDesplay(BaseModel):
    Id : int
    Job : str
    class Config():
        orm_mode = True

class DepartmentDesplay(BaseModel):
    Id : int
    Department : str
    class Config():
        orm_mode = True


class HiredbyJobDeparmentDesplay (BaseModel):
    Department : str
    Job : str
    q1 : str
    q2 : str
    q3 : str
    q4 : str
    class Config():
        orm_mode = True

class HiringDepartmentDisplay(BaseModel):
    id: str
    department: str
    num_employees_hired: str
    class Config():
        orm_mode = True
