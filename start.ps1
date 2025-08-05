# Quick Start Script for Jumia ELT Pipeline (PowerShell)

Write-Host "🚀 Starting Jumia ELT Pipeline Setup..." -ForegroundColor Green

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found. Please copy .env.template to .env and update with your database credentials" -ForegroundColor Red
    exit 1
}

# Create directories if they don't exist
Write-Host "📁 Creating necessary directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "airflow\logs", "airflow\plugins" | Out-Null

# Check Docker
try {
    docker --version | Out-Null
} catch {
    Write-Host "❌ Docker not found. Please install Docker and Docker Compose" -ForegroundColor Red
    exit 1
}

Write-Host "🐳 Starting Docker services..." -ForegroundColor Cyan
Set-Location docker
docker-compose down 2>$null
docker-compose up -d

Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep 30

Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Access Airflow UI: http://localhost:8080" -ForegroundColor Cyan
Write-Host "🔑 Username: admin" -ForegroundColor White
Write-Host "🔑 Password: admin" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Next steps:" -ForegroundColor Yellow
Write-Host "1. Update .env with your actual database password"
Write-Host "2. Access Airflow UI and enable the 'jumia_elt_pipeline' DAG"
Write-Host "3. Trigger the DAG manually or wait for scheduled run"
Write-Host ""
Write-Host "📝 View logs: docker-compose logs -f"
Write-Host "🛑 Stop services: docker-compose down"
