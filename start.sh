#!/bin/bash
# Quick Start Script for Jumia ELT Pipeline

echo "🚀 Starting Jumia ELT Pipeline Setup..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please copy .env.template to .env and update with your database credentials"
    exit 1
fi

# Create directories if they don't exist
echo "📁 Creating necessary directories..."
mkdir -p airflow/logs airflow/plugins

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker and Docker Compose"
    exit 1
fi

echo "🐳 Starting Docker services..."
cd docker
docker-compose down 2>/dev/null
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 30

echo "✅ Setup complete!"
echo ""
echo "📊 Access Airflow UI: http://localhost:8080"
echo "🔑 Username: admin"
echo "🔑 Password: admin"
echo ""
echo "🎯 Next steps:"
echo "1. Update .env with your actual database password"
echo "2. Access Airflow UI and enable the 'jumia_elt_pipeline' DAG"
echo "3. Trigger the DAG manually or wait for scheduled run"
echo ""
echo "📝 View logs: docker-compose logs -f"
echo "🛑 Stop services: docker-compose down"
