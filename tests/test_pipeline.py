"""
Test suite for Jumia ELT Pipeline
Essential tests for CI/CD pipeline validation
"""

import sys
import os
import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestEnvironmentConfiguration:
    """Test environment and configuration handling"""
    
    def test_env_template_exists(self):
        """Test that environment template file exists"""
        env_template_path = os.path.join(os.path.dirname(__file__), '..', '.env.template')
        assert os.path.exists(env_template_path), ".env.template file not found"
    
    def test_env_template_content(self):
        """Test that environment template has required variables"""
        env_template_path = os.path.join(os.path.dirname(__file__), '..', '.env.template')
        
        with open(env_template_path, 'r') as f:
            content = f.read()
            
        required_vars = [
            'DB_HOST=',
            'DB_PASSWORD=',
            'DB_NAME=',
            'DB_USER=',
            'AIRFLOW_USER=',
            'AIRFLOW_PASSWORD=',
            'MAX_PAGES=',
            'DELAY_BETWEEN_REQUESTS='
        ]
        
        for var in required_vars:
            assert var in content, f"Required variable {var} not found in .env.template"
    
    def test_gitignore_protects_env(self):
        """Test that .gitignore properly excludes .env files"""
        gitignore_path = os.path.join(os.path.dirname(__file__), '..', '.gitignore')
        
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r') as f:
                content = f.read()
            assert '.env' in content, ".env files should be gitignored for security"


class TestPipelineImports:
    """Test that pipeline modules can be imported safely"""
    
    def test_jumia_pipeline_import(self):
        """Test that jumia_pipeline module structure is valid"""
        pipeline_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'jumia_pipeline.py')
        assert os.path.exists(pipeline_path), "jumia_pipeline.py not found"
        
        # Test that the file is valid Python syntax
        with open(pipeline_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            compile(content, pipeline_path, 'exec')
        except SyntaxError as e:
            pytest.fail(f"Syntax error in jumia_pipeline.py: {e}")
    
    def test_dag_file_exists(self):
        """Test that DAG file exists and is valid"""
        dag_path = os.path.join(os.path.dirname(__file__), '..', 'airflow', 'dags', 'jumia_elt_dag.py')
        assert os.path.exists(dag_path), "jumia_elt_dag.py not found"
        
        # Test that the file is valid Python syntax
        with open(dag_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            compile(content, dag_path, 'exec')
        except SyntaxError as e:
            pytest.fail(f"Syntax error in jumia_elt_dag.py: {e}")


class TestProjectStructure:
    """Test project structure and organization"""
    
    def test_required_directories_exist(self):
        """Test that required project directories exist"""
        base_path = os.path.join(os.path.dirname(__file__), '..')
        
        required_dirs = [
            'src',
            'airflow/dags',
            'docker',
            '.github/workflows'
        ]
        
        for dir_path in required_dirs:
            full_path = os.path.join(base_path, dir_path)
            assert os.path.exists(full_path), f"Required directory {dir_path} not found"
    
    def test_required_files_exist(self):
        """Test that required project files exist"""
        base_path = os.path.join(os.path.dirname(__file__), '..')
        
        required_files = [
            '.env.template',
            '.gitignore',
            'requirements.txt',
            'src/jumia_pipeline.py',
            'airflow/dags/jumia_elt_dag.py',
            'docker/docker-compose.yaml',
            'docker/Dockerfile',
            '.github/workflows/ci-cd.yml'
        ]
        
        for file_path in required_files:
            full_path = os.path.join(base_path, file_path)
            assert os.path.exists(full_path), f"Required file {file_path} not found"
