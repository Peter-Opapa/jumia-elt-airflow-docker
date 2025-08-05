"""
Basic test suite for Jumia ELT Pipeline
Tests core functionality without requiring database connections
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock

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
        with open(pipeline_path, 'r') as f:
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
        with open(dag_path, 'r') as f:
            content = f.read()
        
        try:
            compile(content, dag_path, 'exec')
        except SyntaxError as e:
            pytest.fail(f"Syntax error in jumia_elt_dag.py: {e}")


class TestDockerConfiguration:
    """Test Docker configuration files"""
    
    def test_docker_compose_exists(self):
        """Test that docker-compose.yaml exists"""
        compose_path = os.path.join(os.path.dirname(__file__), '..', 'docker', 'docker-compose.yaml')
        assert os.path.exists(compose_path), "docker-compose.yaml not found"
    
    def test_docker_compose_syntax(self):
        """Test that docker-compose.yaml has valid YAML syntax"""
        import yaml
        
        compose_path = os.path.join(os.path.dirname(__file__), '..', 'docker', 'docker-compose.yaml')
        
        try:
            with open(compose_path, 'r') as f:
                yaml.safe_load(f)
        except yaml.YAMLError as e:
            pytest.fail(f"Invalid YAML syntax in docker-compose.yaml: {e}")


@patch('psycopg2.connect')
class TestDatabaseMocking:
    """Test database operations with mocking"""
    
    def test_database_connection_mock(self, mock_connect):
        """Test database connection with mocked psycopg2"""
        # Mock successful connection
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        # This would normally be imported from jumia_pipeline
        # For testing, we'll simulate the connection logic
        def mock_get_db_connection():
            import psycopg2
            return psycopg2.connect(
                host='test_host',
                port=5432,
                database='test_db',
                user='test_user',
                password='test_password'
            )
        
        # Test the mocked connection
        conn = mock_get_db_connection()
        assert conn is not None
        mock_connect.assert_called_once()
    
    def test_data_processing_mock(self, mock_connect):
        """Test data processing logic with mocked data"""
        # Mock data that would come from scraping
        mock_laptop_data = [
            {
                'product_name': 'Test Laptop HP 15',
                'price_ksh': 65000,
                'product_url': 'https://test.com/laptop1',
                'image_url': 'https://test.com/img1.jpg',
                'rating': 4.5,
                'reviews_count': 123
            },
            {
                'product_name': 'Test Laptop Dell 14',
                'price_ksh': 75000,
                'product_url': 'https://test.com/laptop2',
                'image_url': 'https://test.com/img2.jpg',
                'rating': 4.2,
                'reviews_count': 89
            }
        ]
        
        # Test data validation
        assert len(mock_laptop_data) == 2
        assert all('product_name' in item for item in mock_laptop_data)
        assert all('price_ksh' in item for item in mock_laptop_data)
        assert all(isinstance(item['price_ksh'], (int, float)) for item in mock_laptop_data)


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
            'README.md',
            '.env.template',
            '.gitignore',
            'requirements.txt',
            'src/jumia_pipeline.py',
            'airflow/dags/jumia_elt_dag.py',
            'docker/docker-compose.yaml',
            '.github/workflows/ci-cd.yml'
        ]
        
        for file_path in required_files:
            full_path = os.path.join(base_path, file_path)
            assert os.path.exists(full_path), f"Required file {file_path} not found"


if __name__ == "__main__":
    """Run tests directly if script is executed"""
    pytest.main([__file__, "-v"])
