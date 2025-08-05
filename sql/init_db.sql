-- Initialize Jumia Database Schema
-- This script creates the necessary database and tables for the Jumia ELT pipeline

-- Create the jumia_db database for data warehouse
CREATE DATABASE jumia_db;

-- Connect to jumia_db to create schemas and tables
\c jumia_db;

-- Create schemas for Bronze, Silver, and Gold layers
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;  
CREATE SCHEMA IF NOT EXISTS gold;

-- Bronze Layer Table - Raw scraped data
CREATE TABLE IF NOT EXISTS bronze.jumia_raw_laptops (
    id SERIAL PRIMARY KEY,
    product_name TEXT,
    new_price TEXT,
    old_price TEXT,
    discount TEXT,
    scraped_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Silver Layer Table - Cleaned and standardized data
CREATE TABLE IF NOT EXISTS silver.jumia_clean_laptops (
    id SERIAL PRIMARY KEY,
    product_name TEXT NOT NULL,
    new_price_numeric DECIMAL(10,2),
    old_price_numeric DECIMAL(10,2),
    discount_percentage DECIMAL(5,2),
    brand TEXT,
    scraped_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Gold Layer Table - Aggregated insights
CREATE TABLE IF NOT EXISTS gold.jumia_laptop_insights (
    id SERIAL PRIMARY KEY,
    brand TEXT,
    avg_price DECIMAL(10,2),
    min_price DECIMAL(10,2),
    max_price DECIMAL(10,2),
    avg_discount DECIMAL(5,2),
    total_products INTEGER,
    analysis_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA bronze TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA silver TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA gold TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA bronze TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA silver TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA gold TO postgres;
