# 🚀 CI/CD Setup Guide for Jumia ELT Pipeline

## 📋 Overview

This guide provides comprehensive instructions for setting up Continuous Integration and Continuous Deployment (CI/CD) for the Jumia ELT Pipeline. The setup ensures automated testing, security scanning, and deployment while maintaining credential security.

## 🔐 GitHub Secrets Configuration

### Required Secrets

Configure these secrets in your GitHub repository (`Settings > Secrets and variables > Actions`):
   ```
   DB_PASSWORD=your_actual_database_password
   AIRFLOW_PASSWORD=your_airflow_password
   ```

### Example GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Jumia ELT Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        pip install beautifulsoup4 requests pandas psycopg2-binary
    
    - name: Run tests
      env:
        DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        AIRFLOW_PASSWORD: ${{ secrets.AIRFLOW_PASSWORD }}
      run: |
        # Add your test commands here
        python -c "from src.jumia_pipeline import scrape_laptop_data; print('Pipeline import successful')"

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      env:
        DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        AIRFLOW_PASSWORD: ${{ secrets.AIRFLOW_PASSWORD }}
      run: |
        # Add your deployment commands here
        echo "Deploying with secure environment variables"
```

### Docker Secrets (Production)

For production deployments, use Docker secrets:

```bash
# Create secrets
echo "your_db_password" | docker secret create db_password -
echo "your_airflow_password" | docker secret create airflow_password -
```

### Environment-Specific Configuration

1. **Development**: Use `.env` file (not committed)
2. **Staging**: Use CI/CD secrets
3. **Production**: Use orchestration secrets (Docker Swarm, Kubernetes, etc.)

### Security Best Practices

✅ **Never commit `.env` files**
✅ **Use repository secrets for CI/CD**
✅ **Rotate passwords regularly**
✅ **Use least-privilege database users**
✅ **Monitor access logs**
✅ **Use HTTPS for all connections**

## Quick Setup for New Environments

1. Copy `.env.template` to `.env`
2. Update with your actual credentials
3. Run `docker compose up -d`
4. Access Airflow at http://localhost:8080
