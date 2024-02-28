FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /app/modules
COPY modules/*.py .
WORKDIR /app
COPY clockify2imput.py .

ENTRYPOINT [ "python", "clockify2imput.py" ]