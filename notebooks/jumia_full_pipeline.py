# etl_jobs/jumia_pipeline.py
#Importing necessary libraries
from bs4 import BeautifulSoup
import requests
import time
import datetime
import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
base_url = "https://www.jumia.co.ke"
headers = {
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
}
#This script scrapes laptop data from Jumia Kenya and saves it to a CSV file.
# It collects product name, current price, old price, discount, and the date of scraping.
def scrape_laptop_data():
    all_data = []
    today = datetime.date.today()

    for page in range(1,7):
        category_url = f"https://www.jumia.co.ke/mlp-laptops/?page={page}"
        print(f"\n📄 Scraping Page {page}...")

        try:
            response = requests.get(category_url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('article', class_='c-prd')

            for i, product in enumerate(products):
                a_tag = product.find('a', class_='core')
                if not a_tag:
                    continue

                product_url = base_url + a_tag.get('href')
                try:
                    product_response = requests.get(product_url, headers=headers, timeout=10)
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
                    time.sleep(1)

                except requests.exceptions.RequestException as e:
                    print(f"Product error: {e}")
                    continue

            # Save to CSV after each page
            pd.DataFrame(all_data, columns=['Name', 'Current Price', 'Old Price', 'Discount', 'Date']).to_csv(
                'JumiaLaptopScrape.csv', index=False
            )

        except requests.exceptions.RequestException as e:
            print(f"Page error: {e}")
            continue

    return all_data
#This script loads scraped laptop data into the bronze layer of the database
# It connects to the PostgreSQL database and inserts the data into the bronze.jumia_raw_laptops table
def load_to_bronze(data):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="jumia_db",
            user="postgres",
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE bronze.jumia_raw_laptops;")
        insert_query = """
            INSERT INTO bronze.jumia_raw_laptops (
                product_name, new_price, old_price, discount, scraped_on
            ) VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query,data)
        conn.commit()
        print("Data loaded to bronze layer.")

    except Exception as e:
        print(f"Bronze insert error: {e}")
    finally:
        if conn:
            conn.close()
#This script runs the silver layer procedure in the database
# It assumes the silver layer procedure is already defined in the database, which is true.
def run_silver_layer_procedure():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="jumia_db",
            user="postgres",
            password=os.getenv("DB_PASSWORD")
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
#This script runs the gold layer procedure in the database
# It assumes the gold layer procedure is already defined in the database, which is true
def run_gold_layer_procedure():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="jumia_db",
            user="postgres",
            password=os.getenv("DB_PASSWORD")
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


#This script runs the entire ETL pipeline
# It scrapes laptop data, loads it to the bronze layer, and runs silver and gold          
if __name__ == "__main__":
    data = scrape_laptop_data()
    load_to_bronze(data)
    run_silver_layer_procedure()
    run_gold_layer_procedure()
