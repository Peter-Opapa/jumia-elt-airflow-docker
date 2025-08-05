# Simplified Jumia ELT Pipeline

This is a streamlined version of the Jumia laptop scraping ELT pipeline that connects to your existing PostgreSQL database.

## Architecture

**Extract** → **Load** → **Transform**
- **Extract**: Scrape laptop data from Jumia Kenya
- **Load**: Insert raw data into your existing bronze layer table
- **Transform**: Trigger your existing stored procedures for silver and gold layers

## Prerequisites

- Your PostgreSQL database is already running with:
  - `jumia_db` database created
  - Bronze, Silver, Gold schemas with tables
  - Stored procedures for transformations already implemented
- Docker and Docker Compose installed

## Quick Start

1. **Start the Airflow services:**
   ```bash
   cd docker
   docker-compose up -d
   ```

2. **Access Airflow UI:**
   - URL: http://localhost:8080
   - Username: `admin`
   - Password: `admin`

3. **Run the ELT Pipeline:**
   - Navigate to the `jumia_laptops_elt_pipeline` DAG
   - Click "Trigger DAG" to run manually
   - Or let it run automatically daily at midnight

## Configuration

Update the `.env` file in the `docker/` directory with your database connection details:

```env
JUMIA_DB_HOST=host.docker.internal  # Your PostgreSQL host
JUMIA_DB_PORT=5432                  # Your PostgreSQL port
JUMIA_DB_NAME=jumia_db              # Your database name
JUMIA_DB_USER=postgres              # Your database user
JUMIA_DB_PASSWORD=DB_PASSWORD       # Your database password
```

## Pipeline Tasks

1. **extract_jumia_laptops**: Scrapes data from Jumia Kenya laptops page
2. **load_to_bronze_layer**: Loads raw data into `bronze.jumia_raw_laptops` table
3. **transform_silver_layer**: Calls your stored procedure for silver layer
4. **transform_gold_layer**: Calls your stored procedure for gold layer

## Stored Procedure Names

The pipeline assumes your stored procedures are named:
- `silver.transform_bronze_to_silver()`
- `gold.transform_silver_to_gold()`

If your procedures have different names, update them in `scripts/loading_tasks.py`.

## Monitoring

- Check task logs in the Airflow UI
- View task progress in the Graph view
- Monitor database directly for transformed data

## Stopping

```bash
cd docker
docker-compose down
```
