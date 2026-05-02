from datetime import datetime

import requests
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


API_BASE_URL = "http://host.docker.internal:8000"


def ingest_products():
    payload = [
        {"name": "Orange", "price": 120, "category": "fruits"},
        {"name": "Milk", "price": 80, "category": "dairy"},
    ]

    response = requests.post(
        f"{API_BASE_URL}/products/ingest",
        json=payload,
        headers={"source-system": "airflow"},
        timeout=30,
    )

    response.raise_for_status()
    print(response.json())


def load_products():
    response = requests.post(
        f"{API_BASE_URL}/products/load",
        timeout=30,
    )

    response.raise_for_status()
    print(response.json())


with DAG(
    dag_id="product_ingestion_dag",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["fastapi", "sqlserver", "ingestion"],
) as dag:

    ingest_task = PythonOperator(
        task_id="ingest_products_to_staging",
        python_callable=ingest_products,
    )

    load_task = PythonOperator(
        task_id="run_stored_procedure_load",
        python_callable=load_products,
    )

    ingest_task >> load_task