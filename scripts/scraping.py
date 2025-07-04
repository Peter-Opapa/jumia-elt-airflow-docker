#Importing necessary libraries
from bs4 import BeautifulSoup
import requests
import time
import datetime
import pandas as pd
import os

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

    for page in range(1,3):
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
'/opt/airflow/dags/jumia/JumiaLaptopScrape.csv', index=False
            )

        except requests.exceptions.RequestException as e:
            print(f"Page error: {e}")
            continue

print(f"✔️ Scraped data saved to cvs file successfully.")