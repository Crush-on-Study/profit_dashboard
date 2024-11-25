import time
import datetime
import re
import os
import csv
import multiprocessing
from typing import List, Dict, Set, Optional
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dcinside import DcinsideCoroller

@dataclass
class Post:
    coin_name: str
    total_cost: str
    coin_count: int
    price: float
    likes: int
    volume: str
    supply: str

class CoinMarketApp(DcinsideCoroller):
    BASE_URL = 'https://coinmarketcap.com/ko/'

    def __init__(self):
        super().__init__()
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.all_posts = []
        self.today = datetime.datetime.now().strftime("%Y%m%d")

    def today_vol_croll(self):
        try:
            self.driver.get(self.BASE_URL)
            
            # Wait for the page to load
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'sc-31e84ac2-1.cDNchY')))
            
            # Sort by volume
            vol_col = self.driver.find_elements(By.CLASS_NAME, 'sc-31e84ac2-1.cDNchY')[7]
            vol_col.click()
            
            # Wait for sorting to complete
            time.sleep(2)
            
            # Collect top 10 coins data
            coin_names = self.driver.find_elements(By.CLASS_NAME, 'sc-65e7f566-0.iPbTJf.coin-item-name')
            total_cost = self.driver.find_element(By.CLASS_NAME, 'sc-11478e5d-1.jfwGHx').text
            prices = self.driver.find_elements(By.CLASS_NAME, 'sc-b3fc6b7-0.dzgUIj')
            volumes = self.driver.find_elements(By.CLASS_NAME, 'sc-71024e3e-0.bbHOdE.font_weight_500')
            supplies = self.driver.find_elements(By.CLASS_NAME, 'sc-71024e3e-0.hhmVNu')
            
            # Process and store data
            self.all_posts = []
            for i in range(min(10, len(coin_names))):  # Limit to top 10
                post = Post(
                    coin_name=coin_names[i].text,
                    total_cost=total_cost,
                    coin_count=i+1,
                    price=float(prices[i].text.replace('₩', '').replace(',', '')),
                    likes=0,  # No likes data available
                    volume=volumes[i].text,
                    supply=supplies[i].text
                )
                self.all_posts.append(post.__dict__)
            
            print(f"Collected data for {len(self.all_posts)} coins")
        
        except Exception as e:
            print(f"Error during crawling: {e}")
        finally:
            self.driver.quit()

    def save_to_csv(self, filename=None):
        try:
            if filename is None:
                filename = os.path.join(os.getcwd(), f"coinmarket_volume_{self.today}.csv")
            
            # Ensure unique filename
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(filename):
                filename = f"{base}_{counter}{ext}"
                counter += 1
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                if self.all_posts:
                    fieldnames = list(self.all_posts[0].keys())
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for post in self.all_posts:
                        writer.writerow(post)
                    print(f"Saved {len(self.all_posts)} coins to {filename}")
                else:
                    print("No coin data to save.")
        
        except Exception as e:
            print(f"Error saving to CSV: {e}")

def main():
    croller = CoinMarketApp()
    try:
        croller.today_vol_croll()
        croller.save_to_csv()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()