"""
Health Check Script for Jumia ELT Pipeline
Run this to validate your setup before starting the pipeline
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        return False
    
    required_vars = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
    with open('.env', 'r') as f:
        content = f.read()
    
    missing_vars = []
    for var in required_vars:
        if f"{var}=" not in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    if "your_password_here" in content or "your_actual_password" in content:
        print("⚠️  Please update DB_PASSWORD in .env with your actual database password")
        return False
    
    print("✅ Environment configuration valid")
    return True

def check_project_structure():
    """Verify professional project structure"""
    required_paths = [
        'airflow/dags/jumia_elt_dag.py',
        'src/jumia_pipeline.py',
        'docker/docker-compose.yaml',
        '.env'
    ]
    
    missing_paths = []
    for path in required_paths:
        if not os.path.exists(path):
            missing_paths.append(path)
    
    if missing_paths:
        print(f"❌ Missing files: {', '.join(missing_paths)}")
        return False
    
    print("✅ Project structure valid")
    return True

def check_python_modules():
    """Check if required Python modules can be imported"""
    required_modules = ['requests', 'beautifulsoup4', 'pandas', 'psycopg2']
    
    missing_modules = []
    for module in required_modules:
        try:
            if module == 'beautifulsoup4':
                import bs4
            elif module == 'psycopg2':
                import psycopg2
            else:
                __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"⚠️  Python modules will be installed in Docker: {', '.join(missing_modules)}")
    else:
        print("✅ All Python dependencies available")
    
    return True

def main():
    print("🔍 Jumia ELT Pipeline Health Check")
    print("=" * 40)
    
    checks = [
        check_env_file(),
        check_project_structure(),
        check_python_modules()
    ]
    
    print("=" * 40)
    
    if all(checks):
        print("🎉 All checks passed! Ready to start the pipeline.")
        print("\nNext steps:")
        print("1. Run: docker-compose up -d (from docker/ directory)")
        print("2. Access: http://localhost:8080")
        print("3. Enable and trigger the 'jumia_elt_pipeline' DAG")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
