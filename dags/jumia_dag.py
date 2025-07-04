# --- dags/jumia_dag.py ---

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from jumia.scraping import scrape_laptop_data
from jumia.database_tasks import load_to_bronze, run_silver_layer_procedure, run_gold_layer_procedure

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 1),
}

with DAG(
    dag_id='jumia_laptops_etl',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:

    task_scrape = PythonOperator(
        task_id='scrape_laptops',
        python_callable=scrape_laptop_data,
        dag=dag
    )

    task_load =PythonOperator(
        task_id='load_to_bronze',
        python_callable=load_to_bronze
    )

    task_silver =PythonOperator(
        task_id='run_silver_layer',
        python_callable=run_silver_layer_procedure
    )

    task_gold =PythonOperator(
        task_id='run_gold_layer',
        python_callable=run_gold_layer_procedure
    )

    task_scrape >> task_load >> task_silver >> task_gold

