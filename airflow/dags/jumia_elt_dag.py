# airflow/dags/jumia_elt_dag.py
"""
Jumia ELT Pipeline DAG
Orchestrates the extraction, loading, and transformation of Jumia laptop data
"""

import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

# Add src directory to Python path for imports
sys.path.append("/opt/airflow/src")

from jumia_pipeline import (  # noqa: E402
    scrape_laptop_data,
    load_to_bronze,
    run_silver_layer_procedure,
    run_gold_layer_procedure,
)

# DAG Configuration
default_args = {
    "owner": "opapa-peter",
    "depends_on_past": False,
    "start_date": datetime(2025, 8, 5),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "catchup": False,
}

# Create DAG
dag = DAG(
    "jumia_elt_pipeline",
    default_args=default_args,
    description="Jumia Laptop ELT Pipeline - Extract, Load, Transform",
    schedule_interval="0 0 * * *",  # Daily at midnight UTC
    max_active_runs=1,
    tags=["jumia", "elt", "laptops", "data-pipeline"],
)


# Task 1: Extract laptop data from Jumia
def extract_task():
    """Extract laptop data and return for next task."""
    print("🚀 Starting data extraction...")
    data = scrape_laptop_data()
    print(f"📊 Extracted {len(data)} laptop records")
    return data


extract_laptops = PythonOperator(
    task_id="extract_laptops",
    python_callable=extract_task,
    dag=dag,
    doc_md="""
    ### Extract Laptops
    Scrapes laptop data from 6 pages of Jumia Kenya laptops category.
    Extracts: product name, current price, old price, discount, date
    """,
)


# Task 2: Load data to Bronze layer
def load_task(**context):
    """Load extracted data to bronze layer."""
    print("📥 Starting data loading...")
    # Get data from previous task
    data = context["task_instance"].xcom_pull(task_ids="extract_laptops")
    load_to_bronze(data)
    print("✅ Data loaded to Bronze layer")


load_bronze = PythonOperator(
    task_id="load_bronze",
    python_callable=load_task,
    dag=dag,
    doc_md="""
    ### Load to Bronze Layer
    Loads raw scraped data into bronze.jumia_raw_laptops table.
    Truncates existing data and inserts fresh records.
    """,
)

# Task 3: Transform to Silver layer
transform_silver = PythonOperator(
    task_id="transform_silver",
    python_callable=run_silver_layer_procedure,
    dag=dag,
    doc_md="""
    ### Silver Layer Transformation
    Executes silver.clean_jumia_laptops() stored procedure.
    Cleans and standardizes the bronze layer data.
    """,
)

# Task 4: Transform to Gold layer
transform_gold = PythonOperator(
    task_id="transform_gold",
    python_callable=run_gold_layer_procedure,
    dag=dag,
    doc_md="""
    ### Gold Layer Aggregation
    Executes gold.refresh_gold_layer() stored procedure.
    Creates business-ready aggregated insights.
    """,
)

# Define task dependencies
extract_laptops >> load_bronze >> transform_silver >> transform_gold
