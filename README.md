
# 🛒 Jumia Laptop ELT Pipeline (Airflow + Docker + PostgreSQL)

A production-grade ELT pipeline built using Python for scraping real-time laptop product data from [Jumia Kenya Laptops](https://www.jumia.co.ke/mlp-laptops/) category. The extracted data is simultaneously stored in a CSV file and loaded into a PostgreSQL-based data warehouse structured into Bronze, Silver, and Gold layers.

Transformations are handled using SQL stored procedures in the Database, and the entire workflow is fully containerized using Docker and orchestrated with Apache Airflow. The pipeline is designed to run automatically on a daily schedule or can be manually triggered via the Airflow web interface.

This robust and modular setup is ideal for automating data collection, transformation, and storage processes in a scalable and maintainable way.

---

## 🧭 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [How to Run](#how-to-run)
- [Database Schema](#database-schema)
- [To Do](#to-do)
- [License](#license)

---

## 🚀 Project Overview

This project automates the extraction, loading and transformation of real-time laptop listings from Jumia. The scraped data is simultaneously saved into a CSV file and streamed directly into a PostgreSQL data warehouse where it undergoes multiple transformation layers:

- **Bronze Layer**: Raw scraped data
- **Silver Layer**: Cleaned and standardized data via SQL procedures
- **Gold Layer**: Analytical summary tables for reporting

Everything is **Dockerized** and managed using **Apache Airflow**, making it robust, reproducible, and production-ready.

---

## 🧱 Architecture

![ETL Architecture Diagram](https://github.com/Peter-Opapa/jumia-elt-airflow-docker/blob/main/images/data-architecture.png)

---

## ⚙️ Tech Stack

- **Python** – Web scraping, ETL logic
- **BeautifulSoup & Requests** – For HTML parsing
- **Pandas** – Data manipulation
- **PostgreSQL** – Data warehouse with multi-layer architecture
- **Stored Procedures** – For transformations (Silver & Gold layers)
- **Apache Airflow** – Workflow orchestration
- **Docker** – Containerization
- **Docker Compose** – Multi-service orchestration

---

## ✨ Features

- ✅ Real-time scraping of Jumia laptops
- ✅ Dual-loading to CSV and PostgreSQL
- ✅ Layered warehouse: Bronze, Silver, Gold
- ✅ SQL transformations via stored procedures
- ✅ Fully containerized using Docker
- ✅ Scheduled or manual runs via Airflow UI
- ✅ Scalable and modular design

---

## 📁 Project Structure

```bash
jumia-laptop-etl-pipeline/
│
├── dags/
│   └── jumia_etl_dag.py                   # Airflow DAG definition
│
├── scripts/
│   ├── scraping.py                        # Scrapes Jumia laptops data                  
│   └── loading_tasks.py                   # Loads data into bronze layer and executes stored procedures
│
├── sql/
│   ├── create_bronze_table.sql            # SQL query for creating the bronze layer table
│   ├── silver_layer_proc.sql              # Stored procedure for Silver layer transformation
│   └── gold_layer_proc.sql                # Stored procedure for Gold layer (business-ready data)
│
├── Images/                                # Captured screenshots and proof images
│
├── Logs/
│   ├── scrape_laptops.log                 # Airflow log showing successful data scraping                  
│   └── load_to_bronze.log                 # Airflow log showing successful loading into bronze layer
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml                 # Manages multi-container Docker environment
│
├── data/
│   └── sample_laptops.csv                 # Sample scraped data saved to CSV
│
├── notebooks/
│   ├── jumia_full_pipeline.ipynb          # Jupyter version of the full pipeline (for testing)
│   └── jumia_full_pipeline.py             # Python script version of the notebook
│
├── requirements.txt                       # Python dependencies
├── README.md                              # Project documentation
└── .gitignore                             # Excludes files from Git tracking

```

---

##  Proof of Working

### 📌 Airflow Web UI 
![Airflow Web UI Screenshot](https://github.com/Peter-Opapa/jumia-elt-airflow-docker/blob/main/images/airflow_success.png)

### 📌 PostgreSQL Layers
#### Bronze layer Output
![Bronze Layer table](https://github.com/Peter-Opapa/jumia-elt-airflow-docker/blob/main/images/bronze_layer_output.png)
#### Silver layer Output
![Silver Layer Table](https://github.com/Peter-Opapa/jumia-elt-airflow-docker/blob/main/images/Silver_layer_output.png)
#### Gold layer Output
![Gold Layer Sample](https://github.com/Peter-Opapa/jumia-elt-airflow-docker/blob/main/images/sample_gold_layer_output.png)

### 📌 Manual Testing Output
![Manual Test Result](https://github.com/Peter-Opapa/jumia-elt-airflow-docker/blob/main/images/manual_testing_success.png)

### 📌 Airflow Task Logs  
[Airflow Logs](https://github.com/Peter-Opapa/jumia-elt-airflow-docker/tree/main/logs)


---

## 🧪 How to Run

### 📦 Prerequisites
- Docker & Docker Compose installed
- Git

### ▶️ Run the Pipeline

```bash
# Clone the repository
git clone https://github.com/Peter-Opapa/jumia-elt-airflow-docker.git
cd jumia-elt-airflow-docker

# Start all services (Airflow, Postgres)
docker-compose up --build

# Open Airflow UI
# Visit http://localhost:8080
# Login: admin / admin (default)

# Trigger the DAG manually or wait for the daily schedule
```

---

## 🗃️ Database Schema

### Bronze Table
| Column        | Type      |
|---------------|-----------|
| product_name  | TEXT      |
| new_price     | TEXT  |
| old_price     | TEXT  |
| discount      | TEXT      |
| scraped_on    | TIMESTAMP |

### Silver Layer
Cleaned using [`silver_layer_proc.sql`](https://github.com/Peter-Opapa/jumia-elt-airflow-docker/blob/main/sql/silver_schema_stored_procedure.sql): removes nulls, standardizes fields

### Gold Layer
Aggregated insights created using [`gold_layer_proc.sql`](https://github.com/Peter-Opapa/jumia-elt-airflow-docker/blob/main/sql/gold_schema_stored_procedure.sql): average prices, discounts per brand/category

---

## 📌 To Do

- [ ] Expand scraper to other Jumia product categories
- [ ] Connect to BI tools (Power BI, Metabase)
- [ ] Add unit/integration tests

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](https://github.com/Peter-Opapa/jumia-elt-airflow-docker/blob/main/LICENSE) for details.

---

## 📬 Contact

Created with ❤️ by [Peter](https://github.com/peter-opapa)  
Feel free to reach out or open an issue for questions and improvements!
