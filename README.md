# Jumia ELT Data Pipeline

A professional Apache Airflow-based ELT (Extract, Load, Transform) pipeline for scraping laptop data from Jumia Kenya and processing it through a medallion architecture (Bronze, Silver, Gold).

## 🚀 Overview

This project implements an enterprise-grade data pipeline that:
1. **Extracts** laptop product data from Jumia Kenya website
2. **Loads** raw data into a Bronze layer (PostgreSQL)
3. **Transforms** data through Silver (cleaned) and Gold (aggregated) layers using stored procedures

## 🏗️ Architecture

- **Bronze Layer**: Raw scraped data with minimal processing
- **Silver Layer**: Cleaned and standardized data via `clean_jumia_laptops()` procedure
- **Gold Layer**: Business-ready aggregated data via `refresh_gold_layer()` procedure
- **Orchestration**: Apache Airflow with LocalExecutor
- **Storage**: PostgreSQL with dedicated schemas

## 📋 Prerequisites

- Docker and Docker Compose
- Existing PostgreSQL database with:
  - `bronze` schema for raw data storage
  - `silver` schema with `clean_jumia_laptops()` stored procedure
  - `gold` schema with `refresh_gold_layer()` stored procedure

## 🚀 Quick Start

1. **Configure Environment**
   ```bash
   # Copy template and edit with your database credentials
   cp .env.template .env
   # Update DB_PASSWORD and other values in .env file
   ```

2. **Start the Pipeline**
   ```bash
   cd docker
   docker-compose up -d
   ```

3. **Access Airflow**
   - **URL**: http://localhost:8080
   - **Username**: admin
   - **Password**: admin

4. **Trigger the DAG**
   - Navigate to "jumia_elt_pipeline" in Airflow UI
   - Toggle ON and trigger manually or wait for scheduled run

## 📁 Professional Project Structure

```
jumia-elt-airflow-docker/
├── airflow/
│   ├── dags/
│   │   └── jumia_elt_dag.py       # Main orchestration DAG
│   ├── logs/                      # Execution logs
│   └── plugins/                   # Custom Airflow plugins
├── src/
│   └── jumia_pipeline.py          # Core ELT functions
├── config/                        # Configuration files
├── docker/
│   └── docker-compose.yaml        # Clean containerization
├── .env                          # Environment variables
├── .env.template                 # Environment template
└── README.md                     # Documentation
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Airflow Settings
AIRFLOW_UID=50000
AIRFLOW_USER=admin
AIRFLOW_PASSWORD=admin

# Your Existing Database
DB_HOST=host.docker.internal  # For Docker to host communication
DB_PORT=5432
DB_NAME=jumia_db
DB_USER=postgres
DB_PASSWORD=your_actual_password

# Pipeline Settings
MAX_PAGES=6
DELAY_BETWEEN_REQUESTS=1
```

## 🔄 Pipeline Details

### Data Flow
```
Jumia Website → Bronze Layer → Silver Layer → Gold Layer
     ↓              ↓              ↓            ↓
  Scraping    Raw Storage    Data Cleaning   Business Logic
```

### Airflow DAG Tasks

1. **extract_laptops** → Scrapes laptop data (6 pages)
2. **load_bronze** → Inserts raw data into bronze.jumia_laptops
3. **transform_silver** → Executes silver.clean_jumia_laptops()
4. **transform_gold** → Executes gold.refresh_gold_layer()

### Scheduling
- **Frequency**: Daily at 6:00 AM UTC
- **Retries**: 2 attempts with 5-minute delays
- **Timeout**: 30 minutes per task

## 📊 Monitoring & Observability

### Airflow UI
- **DAG Status**: Monitor pipeline health and execution history
- **Task Logs**: Detailed logs for debugging and monitoring
- **Gantt Chart**: Execution timeline and performance metrics

### Database Monitoring
Query your existing PostgreSQL schemas to verify data flow:
```sql
-- Check Bronze layer
SELECT COUNT(*) FROM bronze.jumia_laptops;

-- Verify Silver processing
SELECT * FROM silver.processed_laptops LIMIT 5;

-- Validate Gold aggregations  
SELECT * FROM gold.laptop_summary;
```

## 🛠️ Development & Maintenance

### Adding New Features
1. **Core Logic**: Update `src/jumia_pipeline.py`
2. **Orchestration**: Modify `airflow/dags/jumia_elt_dag.py`
3. **Database**: Extend stored procedures as needed

### Local Testing
```bash
# Test core functions
cd src
python -c "from jumia_pipeline import scrape_laptop_data; print(len(scrape_laptop_data()))"

# Validate database connection
python -c "from jumia_pipeline import get_db_connection; print(get_db_connection())"
```

## 🚨 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Database connection failed | Verify `.env` credentials and host accessibility |
| DAG import errors | Check Python path and module imports |
| Scraping failures | Verify Jumia website accessibility and structure |
| Stored procedure errors | Ensure procedures exist in silver/gold schemas |

### Health Checks
```bash
# Check Docker services
docker-compose ps

# View Airflow logs
docker-compose logs airflow-scheduler

# Test database connectivity
docker-compose exec airflow-webserver python -c "from src.jumia_pipeline import get_db_connection; print('DB OK')"
```

## 📈 Performance & Scaling

- **Current Capacity**: ~6 pages, ~120 products per run
- **Resource Usage**: Optimized for LocalExecutor (single machine)
- **Scaling Options**: Upgrade to CeleryExecutor for distributed processing
- **Data Retention**: Managed via your existing database policies

## 🤝 Contributing

1. Create feature branch from `feature/improvements`
2. Follow professional coding standards
3. Update documentation for changes
4. Test thoroughly before submitting PR

## ⚖️ Compliance & Ethics

- Respects Jumia's robots.txt and rate limiting
- Implements delays between requests
- For educational and business intelligence purposes
- Ensure compliance with local data regulations

---

**Status**: ✅ Professional restructure complete - Ready for production use
