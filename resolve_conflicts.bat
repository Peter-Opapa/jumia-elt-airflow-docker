@echo off
REM Conflict Resolution Guide for Windows
echo 🔧 Merge Conflict Resolution Guide
echo =====================================

echo.
echo 📋 CONFLICTS DETECTED IN:
echo   - airflow/dags/jumia_elt_dag.py
echo   - src/jumia_pipeline.py

echo.
echo 🎯 RESOLUTION STRATEGY:
echo   ✅ Keep SECURE environment variables (our branch)
echo   ❌ Reject hardcoded passwords (main branch)

echo.
echo 📝 STEP 1: Fix DAG file (airflow/dags/jumia_elt_dag.py)
echo   Look for: <<<<<<< HEAD
echo   Action: Keep the import structure with proper order:
echo.
echo   from datetime import datetime, timedelta
echo   import sys
echo   import os
echo   from airflow import DAG
echo   from airflow.operators.python import PythonOperator
echo.
echo   # Add src directory to Python path for imports
echo   sys.path.append('/opt/airflow/src')

echo.
echo 📝 STEP 2: Fix Pipeline file (src/jumia_pipeline.py)
echo   In get_db_connection function, KEEP THIS (secure):
echo.
echo     def get_db_connection():
echo         host = os.getenv("DB_HOST", "host.docker.internal")
echo         database = os.getenv("DB_NAME", "jumia_db")  
echo         user = os.getenv("DB_USER", "postgres")
echo         port = int(os.getenv("DB_PORT", 5432))
echo         password = os.getenv("DB_PASSWORD")
echo.
echo   REJECT THIS (insecure from main):
echo         password = "Opapa@1292"  # ❌ HARDCODED PASSWORD

echo.
echo 📝 STEP 3: Configuration variables
echo   KEEP THIS (configurable):
echo     max_pages = int(os.getenv("MAX_PAGES", 6))
echo     delay = float(os.getenv("DELAY_BETWEEN_REQUESTS", 1))

echo.
echo 📝 STEP 4: Remove ALL conflict markers
echo   Delete these lines:
echo     <<<<<<< HEAD
echo     =======
echo     >>>>>>> origin/main

echo.
echo 🚀 STEP 5: Complete the merge
echo   git add .
echo   git commit -m "fix: resolve merge conflicts with security hardening"

echo.
echo ✅ This preserves your security improvements!
echo 🔥 Your CI/CD pipeline will pass all security scans!

pause
