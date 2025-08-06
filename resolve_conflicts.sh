#!/bin/bash
# Conflict Resolution Script for Jumia ELT Pipeline

echo "🔧 Resolving merge conflicts between cicd-pipeline-implementation and main..."

# Create backup of current files
echo "📋 Creating backups..."
cp src/jumia_pipeline.py src/jumia_pipeline.py.backup
cp airflow/dags/jumia_elt_dag.py airflow/dags/jumia_elt_dag.py.backup

echo "✅ Starting conflict resolution..."

# Fix the DAG file - Remove conflict markers and use proper imports
cat > airflow/dags/jumia_elt_dag.py << 'EOF'
"""
Jumia ELT Pipeline DAG
Orchestrates the extraction, loading, and transformation of Jumia laptop data
"""

from datetime import datetime, timedelta
import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator

# Add src directory to Python path for imports
sys.path.append('/opt/airflow/src')

from jumia_pipeline import (
    scrape_laptop_data,
    load_to_bronze,
    run_silver_layer_procedure,
    run_gold_layer_procedure
)

# DAG Configuration
default_args = {
    'owner': 'opapa-peter',
    'depends_on_past': False,
    'start_date': datetime(2025, 8, 5),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Create DAG
with DAG(
    'jumia_elt_pipeline',
    default_args=default_args,
    description='Jumia ELT Pipeline for laptop data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 8, 5),
    catchup=False,
    tags=['jumia', 'elt', 'laptops'],
) as dag:

    # Task 1: Scrape laptop data
    scrape_laptops = PythonOperator(
        task_id='scrape_laptops',
        python_callable=scrape_laptop_data,
        provide_context=True,
    )

    # Task 2: Load to Bronze layer
    load_bronze = PythonOperator(
        task_id='load_to_bronze',
        python_callable=load_to_bronze,
        provide_context=True,
    )

    # Task 3: Transform to Silver layer
    transform_silver = PythonOperator(
        task_id='transform_to_silver',
        python_callable=run_silver_layer_procedure,
        provide_context=True,
    )

    # Task 4: Transform to Gold layer
    transform_gold = PythonOperator(
        task_id='transform_to_gold',
        python_callable=run_gold_layer_procedure,
        provide_context=True,
    )

    # Define task dependencies
    scrape_laptops >> load_bronze >> transform_silver >> transform_gold
EOF

echo "✅ DAG file conflict resolved!"

# Now resolve the jumia_pipeline.py conflicts
# Keep the secure version with environment variables
echo "🔒 Resolving pipeline security conflicts..."

# The main conflicts are around database connection and configuration
# We want to keep the secure environment variable approach from our branch
# and reject the hardcoded passwords from main

echo "✅ Use environment variables for database connection (SECURE)"
echo "❌ Reject hardcoded passwords from main branch"

echo "📝 Manual steps required:"
echo "1. In src/jumia_pipeline.py, look for conflict markers:"
echo "   <<<<<<< HEAD"
echo "   ======="  
echo "   >>>>>>> origin/main"
echo ""
echo "2. For database connection, keep THIS version (secure):"
echo "   def get_db_connection():"
echo "       host = os.getenv('DB_HOST', 'host.docker.internal')"
echo "       database = os.getenv('DB_NAME', 'jumia_db')"
echo "       user = os.getenv('DB_USER', 'postgres')"
echo "       port = int(os.getenv('DB_PORT', 5432))"
echo "       password = os.getenv('DB_PASSWORD')"
echo ""
echo "3. For configuration, keep THIS version (configurable):"
echo "       max_pages = int(os.getenv('MAX_PAGES', 6))"
echo "       delay = float(os.getenv('DELAY_BETWEEN_REQUESTS', 1))"
echo ""
echo "4. For code style, keep consistent quote style throughout"
echo ""
echo "5. Remove ALL conflict markers: <<<<<<< HEAD, =======, >>>>>>> origin/main"

echo "🎯 After resolving conflicts:"
echo "   git add ."
echo "   git commit -m 'fix: resolve merge conflicts with security hardening'"

echo "🔥 This preserves the security improvements while merging with main!"
