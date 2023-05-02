FROM python:3.10-alpine3.16

WORKDIR /src

COPY requirements.txt .
RUN apk update
RUN apk add gcc libc-dev g++ libffi-dev libxml2 unixodbc-dev mariadb-dev postgresql-dev
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "8000"]
