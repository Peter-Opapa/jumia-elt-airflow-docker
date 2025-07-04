# --- etl_jobs/jumia/database_tasks.py ---

import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def load_to_bronze():
    conn= None
    try:
        df = pd.read_csv('/opt/airflow/dags/jumia/JumiaLaptopScrape.csv')
        data = df.values.tolist()

        conn = psycopg2.connect(
            host="postgres",
            database="jumia_db",
            user="postgres",
            password=os.getenv("DB_PASSWORD"),
            port=5432
        )
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE bronze.jumia_raw_laptops;")
        insert_query = """
            INSERT INTO bronze.jumia_raw_laptops (
                product_name, new_price, old_price, discount, scraped_on
            ) VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, data)
        conn.commit()
        print("Data loaded to bronze layer.")
    except Exception as e:
        print(f"Bronze insert error: {e}")
    finally:
        if conn:
            conn.close()


def run_silver_layer_procedure():
    try:
        conn = psycopg2.connect(
            host="postgres",
            database="jumia_db",
            user="postgres",
            password=os.getenv("DB_PASSWORD"),
            port=5432
        )
        cursor = conn.cursor()
        cursor.execute("CALL silver.clean_jumia_laptops();")
        conn.commit()
        print("Silver layer procedure executed.")
    except Exception as e:
        print(f"Silver procedure error: {e}")
    finally:
        if conn:
            conn.close()

def run_gold_layer_procedure():
    try:
        conn = psycopg2.connect(
            host="postgres",
            database="jumia_db",
            user="postgres",
            password=os.getenv("DB_PASSWORD"),
            port=5432
            )
        cursor = conn.cursor()
        cursor.execute("CALL gold.refresh_gold_layer();")
        conn.commit()
        print("Gold layer procedure executed.")
    except Exception as e:
        print(f"Gold procedure error: {e}")
    finally:
        if conn:
            conn.close()
