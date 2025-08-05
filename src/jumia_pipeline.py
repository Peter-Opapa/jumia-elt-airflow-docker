# src/jumia_pipeline.py
"""
Jumia ELT Pipeline - Core Functions
Extracts laptop data from Jumia Kenya, loads to Bronze layer,
and triggers Silver/Gold transformations via stored procedures.
"""

from bs4 import BeautifulSoup
import requests
import time
import datetime
import pandas as pd
import os
import psycopg2

# Configuration
BASE_URL = "https://www.jumia.co.ke"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
}

def get_db_connection():
    """Create database connection to your existing jumia_db"""
    # Connect to your existing PostgreSQL database
    host = "host.docker.internal"  # Your local PostgreSQL
    database = "jumia_db"
    user = "postgres"
    port = 5432
    password = "Opapa@1292"

    print(f"🔗 Connecting to: {host}:{port}/{database} as {user}")

    return psycopg2.connect(
        host=host,
        database=database,
        user=user,
        port=port,
        password=password
    )

def scrape_laptop_data():
    """
    Scrapes laptop data from Jumia Kenya (6 pages)
    Returns: List of laptop data [name, price, old_price, discount, date]
    """
    all_data = []
    today = datetime.date.today()

    print("🚀 Starting Jumia laptop scraping...")

    for page in range(1, 2):  # Scrape 1 pages as in original
        category_url = f"https://www.jumia.co.ke/mlp-laptops/?page={page}"
        print(f"\n📄 Scraping Page {page}...")

        try:
            response = requests.get(category_url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('article', class_='c-prd')

            print(f"   Found {len(products)} products on page {page}")

            for i, product in enumerate(products):
                a_tag = product.find('a', class_='core')
                if not a_tag:
                    continue

                product_url = BASE_URL + a_tag.get('href')
                try:
                    product_response = requests.get(product_url, headers=HEADERS, timeout=10)
                    product_response.raise_for_status()
                    product_soup = BeautifulSoup(product_response.text, 'html.parser')

                    name = product_soup.find('h1').text.strip() if product_soup.find('h1') else 'N/A'
                    price = product_soup.find('span', class_='-b -ubpt -tal -fs24 -prxs')
                    old_price = product_soup.find('span', class_='-tal -gy5 -lthr -fs16 -pvxs -ubpt')
                    discount = product_soup.find('span', class_='bdg _dsct _dyn -mls')

                    all_data.append([
                        name,
                        price.text.strip() if price else 'N/A',
                        old_price.text.strip() if old_price else 'N/A',
                        discount.text.strip() if discount else 'N/A',
                        today
                    ])
                    time.sleep(1)  # Rate limiting

                except requests.exceptions.RequestException as e:
                    print(f"   ⚠️  Product error: {e}")
                    continue

        except requests.exceptions.RequestException as e:
            print(f"❌ Page {page} error: {e}")
            continue

    print(f"✅ Scraping completed! Total products: {len(all_data)}")

    # Save CSV for backup (local development)
    if not os.path.exists('/opt/airflow'):  # Not in Docker
        df = pd.DataFrame(all_data, columns=['Name', 'Current Price', 'Old Price', 'Discount', 'Date'])
        df.to_csv('JumiaLaptopScrape.csv', index=False)
        print("📁 Data saved to JumiaLaptopScrape.csv")

    return all_data

def load_to_bronze(data):
    """
    Loads scraped data into bronze.jumia_raw_laptops table
    Args: data - List of laptop records
    """
    conn = None
    try:
        print("📥 Loading data to Bronze layer...")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Create bronze schema and table if they don't exist
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS bronze;
            CREATE TABLE IF NOT EXISTS bronze.jumia_raw_laptops (
                id SERIAL PRIMARY KEY,
                product_name TEXT,
                new_price TEXT,
                old_price TEXT,
                discount TEXT,
                scraped_on DATE
            );
        """)
        conn.commit()

        # Clear existing data
        cursor.execute("TRUNCATE TABLE bronze.jumia_raw_laptops;")

        # Insert new data
        insert_query = """
            INSERT INTO bronze.jumia_raw_laptops (
                product_name, new_price, old_price, discount, scraped_on
            ) VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, data)
        conn.commit()

        print(f"✅ {len(data)} records loaded to Bronze layer successfully!")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ Bronze layer error: {e}")
        raise e
    finally:
        if conn:
            cursor.close()
            conn.close()

def run_silver_layer_procedure():
    """
    Executes silver.clean_jumia_laptops() stored procedure
    """
    conn = None
    try:
        print("🔄 Running Silver layer transformation...")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if procedure exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM pg_proc p
                JOIN pg_namespace n ON p.pronamespace = n.oid
                WHERE n.nspname = 'silver' AND p.proname = 'clean_jumia_laptops'
            );
        """)
        proc_exists = cursor.fetchone()[0]

        if proc_exists:
            cursor.execute("CALL silver.clean_jumia_laptops();")
            conn.commit()
            print("✅ Silver layer procedure executed successfully!")
        else:
            print("⚠️  Silver layer procedure not found - skipping...")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ Silver layer error: {e}")
        raise e
    finally:
        if conn:
            cursor.close()
            conn.close()

def run_gold_layer_procedure():
    """
    Executes gold.refresh_gold_layer() stored procedure
    """
    conn = None
    try:
        print("🔄 Running Gold layer aggregation...")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if procedure exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM pg_proc p
                JOIN pg_namespace n ON p.pronamespace = n.oid
                WHERE n.nspname = 'gold' AND p.proname = 'refresh_gold_layer'
            );
        """)
        proc_exists = cursor.fetchone()[0]

        if proc_exists:
            cursor.execute("CALL gold.refresh_gold_layer();")
            conn.commit()
            print("✅ Gold layer procedure executed successfully!")
        else:
            print("⚠️  Gold layer procedure not found - skipping...")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ Gold layer error: {e}")
        raise e
    finally:
        if conn:
            cursor.close()
            conn.close()

def run_full_pipeline():
    """
    Executes the complete ELT pipeline
    """
    print("🚀 Starting Jumia ELT Pipeline...")
    start_time = datetime.datetime.now()

    try:
        # Extract
        data = scrape_laptop_data()

        # Load
        load_to_bronze(data)

        # Transform - Silver
        run_silver_layer_procedure()

        # Transform - Gold
        run_gold_layer_procedure()

        end_time = datetime.datetime.now()
        duration = end_time - start_time

        print(f"🎉 Pipeline completed successfully in {duration}")
        return True

    except Exception as e:
        print(f"💥 Pipeline failed: {e}")
        return False

if __name__ == "__main__":
    run_full_pipeline()
