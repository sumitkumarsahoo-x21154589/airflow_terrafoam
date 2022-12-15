FROM apache/airflow:2.2.4-python3.7
COPY requirements.txt .
RUN pip install -r requirements.txt