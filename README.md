
# 🛒 Jumia Laptop ELT Pipeline (Airflow + Docker + PostgreSQL)

A production-grade ELT pipeline that **scrapes laptop data** from the [Jumia Kenya](https://www.jumia.co.ke/) website, loads it into a **PostgreSQL-based data warehouse**, transforms it using **stored procedures**, and orchestrates the process using **Apache Airflow** in a **Dockerized environment**. The pipeline runs **daily** and can also be triggered manually via the Airflow web UI.

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

This project automates the extraction, transformation, and loading of real-time laptop listings from Jumia. The scraped data is simultaneously saved into a CSV file and streamed directly into a PostgreSQL data warehouse where it undergoes multiple transformation layers:

- **Bronze Layer**: Raw scraped data
- **Silver Layer**: Cleaned and standardized data via SQL procedures
- **Gold Layer**: Analytical summary tables for reporting

Everything is **Dockerized** and managed using **Apache Airflow**, making it robust, reproducible, and production-ready.

---

## 🧱 Architecture

![ETL Architecture Diagram](https://example.com/your-etl-architecture.png)

```text
               ┌────────────┐
               │ Web Scraper│
               └─────┬──────┘
                     │
          ┌──────────▼──────────┐
          │  Extract (Python)   │
          └─────┬──────┬────────┘
                │      │
        ┌───────▼──┐ ┌─▼────────┐
        │  CSV File │ │ Bronze DB │
        └──────────┘ └─────┬────┘
                           │
                   ┌──────▼─────┐
                   │ Silver Layer│
                   └──────┬─────┘
                          │
                   ┌──────▼─────┐
                   │ Gold Layer │
                   └────────────┘
                           │
             [Analytics, Dashboards, Exports]

  (All steps orchestrated via Docker + Airflow)
```

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
│   └── jumia_etl_dag.py                # Airflow DAG definition
│
├── scripts/
│   ├── extract.py                      # Scrapes Jumia laptops
│   ├── transform.py                    # (Optional) Data cleanup
│   └── load.py                         # Loads data into bronze table
│
├── sql/
│   ├── create_bronze_table.sql
│   ├── silver_layer_proc.sql
│   └── gold_layer_proc.sql
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── data/
│   └── sample_laptops.csv              # Sample data
│
├── notebooks/
│   └── analyze_gold_layer.ipynb        # Optional analytics preview
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🖼️ Screenshots

### 📌 Airflow DAG  
![Airflow DAG Screenshot](https://example.com/airflow-dag.png)

### 📌 Airflow Task Logs  
![Airflow Logs Screenshot](https://example.com/airflow-logs.png)

### 📌 PostgreSQL Layers  
![DB Tables Screenshot](https://example.com/db-tables.png)

---

## 🧪 How to Run

### 📦 Prerequisites
- Docker & Docker Compose installed
- Git

### ▶️ Run the Pipeline

```bash
# Clone the repository
git clone https://github.com/your-username/jumia-laptop-etl-pipeline.git
cd jumia-laptop-etl-pipeline

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
| new_price     | NUMERIC   |
| old_price     | NUMERIC   |
| discount      | TEXT      |
| scraped_on    | TIMESTAMP |

### Silver Layer
> Cleaned using `silver_layer_proc.sql`: removes nulls, standardizes fields

### Gold Layer
> Aggregated insights created using `gold_layer_proc.sql`: average prices, discounts per brand/category

---

## 📌 To Do

- [ ] Add email or Slack alerts on DAG failure
- [ ] Expand scraper to other Jumia product categories
- [ ] Connect to BI tools (Power BI, Metabase)
- [ ] Add unit/integration tests

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](https://github.com/your-username/jumia-laptop-etl-pipeline/blob/main/LICENSE) for details.

---

## 📬 Contact

Created with ❤️ by [Your Name](https://github.com/your-username)  
Feel free to reach out or open an issue for questions and improvements!
