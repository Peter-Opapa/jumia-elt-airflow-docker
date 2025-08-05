# 🔐 GitHub Secrets Setup Guide

## Required Secrets for CI/CD

To enable the full CI/CD pipeline, you need to configure these secrets in your GitHub repository:

### 🚀 How to Add Secrets

1. Go to your GitHub repository
2. Click on **Settings** tab
3. Navigate to **Secrets and variables** > **Actions**
4. Click **"New repository secret"**
5. Add each secret below:

### 📋 Required Secrets List

#### Production Environment
```bash
# Database Configuration
DB_HOST=your-production-db-host.com
DB_PASSWORD=YourSecureProductionPassword123!

# Airflow Configuration  
AIRFLOW_PASSWORD=SecureAirflowAdminPassword456!

# Container Registry (if using private registry)
DOCKER_REGISTRY_USER=your-docker-username
DOCKER_REGISTRY_TOKEN=your-docker-access-token
```

#### Staging Environment (Optional)
```bash
# Staging Database
STAGING_DB_HOST=staging-db-host.com
STAGING_DB_PASSWORD=StagingPassword789!
STAGING_AIRFLOW_PASSWORD=StagingAirflowPass012!
```

### 🔒 Security Best Practices

1. **Use Strong Passwords**: Minimum 12 characters with mixed case, numbers, symbols
2. **Rotate Regularly**: Change passwords quarterly
3. **Least Privilege**: Use dedicated service accounts with minimal permissions
4. **Monitor Usage**: Review GitHub Actions logs for any issues

### 🧪 Testing the Setup

After adding secrets, test the pipeline:

```bash
# Push to trigger CI/CD
git add .
git commit -m "feat: add GitHub Actions CI/CD pipeline"
git push origin feature/improvements

# Monitor the workflow
# Go to Actions tab in GitHub to see the pipeline running
```

### 🎯 Workflow Triggers

The pipeline runs on:
- **Push** to main, develop, or feature branches
- **Pull requests** to main or develop
- **Weekly schedule** (security scans)

### 📊 What the Pipeline Does

1. **🧪 Testing**: Code quality, linting, unit tests across Python versions
2. **🔒 Security**: Vulnerability scanning, secret detection, container security
3. **🐳 Building**: Docker image creation and multi-platform builds
4. **🧪 Integration**: Database connectivity and data flow testing
5. **📊 Performance**: Benchmark testing and performance monitoring
6. **🚀 Deployment**: Automated staging and production deployment

### ⚠️ Important Notes

- The `.env` file is automatically ignored by git (secure by default)
- All database operations in CI use mock data (no real data exposure)
- Container images are built and scanned for vulnerabilities
- Failed security scans won't block the pipeline but will alert you

### 🆘 Troubleshooting

If the pipeline fails:

1. **Check Secrets**: Ensure all required secrets are added correctly
2. **Review Logs**: Go to Actions tab > Click on failed run > Check logs
3. **Test Locally**: Run tests locally before pushing
4. **Validate Configuration**: Ensure .env.template is up to date

The pipeline is designed to be robust and will continue even if some optional steps fail, ensuring your code can still be deployed safely.
