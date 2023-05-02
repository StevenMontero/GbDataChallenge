from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm.session import Session
from routers.schemas import HiredbyJobDeparmentDesplay, HiringDepartmentDisplay

query = text('''
            WITH all_employee_data_from_2021 AS (
    SELECT
    dp."Department",
    jp."Job",
    EXTRACT(QUARTER FROM CAST(em."DateTime" AS TIMESTAMP)) AS "Quarter",
	COUNT(*) AS "Count"
    FROM
    public."Employee" AS em
    INNER JOIN public."Department" AS dp ON dp."Id" = em."DepartmentId"
    INNER JOIN public."Job" AS jp ON jp."Id" = em."JobId"
    WHERE
    EXTRACT(YEAR FROM CAST(em."DateTime" AS TIMESTAMP)) = :year
	GROUP BY
	"dp"."Department",
    "jp"."Job",
    "Quarter"
)

SELECT 
  ed."Department",
  ed."Job",
  COALESCE(SUM(CASE WHEN ed."Quarter" = 1 THEN ed."Count" END), 0) AS Q1,
  COALESCE(SUM(CASE WHEN ed."Quarter" = 2 THEN ed."Count" END), 0) AS Q2,
  COALESCE(SUM(CASE WHEN ed."Quarter" = 3 THEN ed."Count" END), 0) AS Q3,
  COALESCE(SUM(CASE WHEN ed."Quarter" = 4 THEN ed."Count" END), 0) AS Q4
FROM 
  all_employee_data_from_2021 ed
GROUP BY 
  ed."Department", 
  ed."Job"
ORDER BY 
  ed."Department", 
  ed."Job"
        ''')

query_hiring_department = text('''
      WITH employees_by_department AS (
        SELECT 
          "DepartmentId", 
          COUNT(*) AS "num_employees_hired"
        FROM 
          public."Employee" 
        WHERE 
          EXTRACT(YEAR FROM CAST("DateTime" AS TIMESTAMP)) = :year 
        GROUP BY 
          "DepartmentId"
      ), 
      mean_employees_hired AS (
        SELECT 
          AVG("num_employees_hired") AS "mean_num_employees_hired"
        FROM 
          employees_by_department
      )
      SELECT 
        d."Id", 
        d."Department", 
        e."num_employees_hired"
      FROM 
        public."Department" d 
        INNER JOIN employees_by_department e ON d."Id" = e."DepartmentId" 
        CROSS JOIN mean_employees_hired m
      WHERE 
        e."num_employees_hired" > m."mean_num_employees_hired"
      ORDER BY 
        e."num_employees_hired" DESC;WITH employees_by_department AS (
        SELECT 
          "DepartmentId", 
          COUNT(*) AS "num_employees_hired"
        FROM 
          public."Employee" 
        WHERE 
          EXTRACT(YEAR FROM CAST("DateTime" AS TIMESTAMP)) = :year 
        GROUP BY 
          "DepartmentId"
      ), 
      mean_employees_hired AS (
        SELECT 
          AVG("num_employees_hired") AS "mean_num_employees_hired"
        FROM 
          employees_by_department
      )
      SELECT 
        d."Id", 
        d."Department", 
        e."num_employees_hired"
      FROM 
        public."Department" d 
        INNER JOIN employees_by_department e ON d."Id" = e."DepartmentId" 
        CROSS JOIN mean_employees_hired m
      WHERE 
        e."num_employees_hired" > m."mean_num_employees_hired"
      ORDER BY 
        e."num_employees_hired" DESC;
''')


def get_hiring_department(db: Session):
    result = db.connection().execute(query_hiring_department, {"year": 2021})
    hiring_departments = [HiringDepartmentDisplay(
        id=row[0], department=row[1], num_employees_hired=row[2]) for row in result]
    return hiring_departments


def get_all_hired_by_department_job(db: Session):

    try:
        result = db.connection().execute(query, {"year": 2021})
        result_kpi_list = [HiredbyJobDeparmentDesplay(
            Department=row[0], Job=row[1], q1=int(row[2]), q2=int(row[3]), q3=row[4], q4=row[5])
            for row in result.fetchall()]
        return result_kpi_list
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
