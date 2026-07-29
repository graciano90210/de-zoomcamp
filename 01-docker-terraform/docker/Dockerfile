FROM python:3.12-slim

RUN pip install pandas sqlalchemy "psycopg[binary]"

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT ["python", "ingest_data.py"]
