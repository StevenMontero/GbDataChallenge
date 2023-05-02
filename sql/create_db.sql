

CREATE TABLE Department (
    Id int NOT NULL,
    Department varchar(255),
    CONSTRAINT PK_DepartmentId PRIMARY KEY (Id),
);

CREATE TABLE Job (
    Id int NOT NULL,
    Job varchar(255),
    CONSTRAINT PK_JobId PRIMARY KEY (Id),
);

CREATE TABLE Employee (
    Id int NOT NULL,
    Name VARCHAR(200) NOT NULL,
    DateTime VARCHAR(200) NOT NULL,
    DepartmentId int NOT NULL,
    JobId int,
    CONSTRAINT PK_Employee PRIMARY KEY (Id),
    CONSTRAINT FK_DepartmentId FOREIGN KEY (DepartmentId) REFERENCES Department(Id),
    CONSTRAINT FK_JobId FOREIGN KEY (JobId) REFERENCES Job(Id)
);

CREATE INDEX idx_id_deparment ON Employee (DepartmentId);
CREATE INDEX idx_id_job ON Employee (JobId);