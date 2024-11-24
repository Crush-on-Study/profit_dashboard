import time
import datetime
import re
import os
import csv
import asyncio
import aiohttp
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DcinsideCoroller:
    def __init__(self):
        self._setup_dates()
        self.all_posts = []
        self.session = None
        
    def _setup_dates(self):
        today = datetime.date.today()
        self.today = today.strftime("%m.%d")
        self.targetday = (today - datetime.timedelta(days=1)).strftime("%m.%d")
        self.nonetargetday = (today - datetime.timedelta(days=2)).strftime("%m.%d")
        self.today_time_pattern = re.compile(r'^\d{2}:\d{2}$')
    
    def _get_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        return webdriver.Chrome(options=chrome_options)
    
    def save_to_csv(self, filename=None, keyword=None):
        if not filename:
            filename = os.path.join(os.getcwd(), f"dcinside_crawl_{self.today}_{keyword}.csv")
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            if self.all_posts:
                fieldnames = list(self.all_posts[0].keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.all_posts)
                print(f"Saved {len(self.all_posts)} posts to {filename}")
            else:
                print("No posts to save.")

    def process_page(self, page, keyword, processed_indices):
        driver = self._get_driver()
        try:
            page_posts = []
            page_url = f"https://gall.dcinside.com/board/lists/?id=bitcoins_new1&page={page}&search_pos=&s_type=search_subject_memo&s_keyword={keyword}"
            driver.get(page_url)
            
            wait = WebDriverWait(driver, 10)
            index_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "gall_num")))
            
            indices = [elem.text for elem in index_elements if elem.text.isdigit()]
            
            for index in indices:
                if index in processed_indices:
                    continue
                    
                try:
                    post_data = self.process_post(driver, index, keyword)
                    if post_data:
                        page_posts.append(post_data)
                        processed_indices.add(index)
                except Exception as e:
                    print(f"Error processing post {index}: {e}")
                    continue
                    
            return page_posts, self.today in [date.text for date in driver.find_elements(By.CLASS_NAME, "gall_date")]
        finally:
            driver.quit()

    def process_post(self, driver, index, keyword):
        page_url = f"https://gall.dcinside.com/board/view/?id=bitcoins_new1&no={index}&s_type=search_subject_memo&s_keyword={keyword}"
        try:
            driver.get(page_url)
            wait = WebDriverWait(driver, 5)
            
            date_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gall_date")))
            post_date = date_element.text
            date_part = re.search(r'\d{4}\.(\d{2}\.\d{2})', post_date).group(1)
            
            if self.today != date_part:
                return None
                
            return self.extract_post_data(driver, index, keyword)
        except Exception as e:
            print(f"Error in process_post for index {index}: {e}")
            return None

    def extract_post_data(self, driver, index, keyword):
        try:
            title = driver.find_element(By.CLASS_NAME, "title_subject").text
            write = self._clean_text(driver.find_element(By.CLASS_NAME, "write_div").text)
            gall_count = int(driver.find_element(By.CLASS_NAME, "gall_count").text.replace("조회", ""))
            
            try:
                gall_comment = int(driver.find_element(By.CLASS_NAME, "gall_comment").text.replace("댓글", ""))
                gall_replynum = int(driver.find_element(By.CLASS_NAME, "gall_reply_num").text.replace("추천", ""))
                
                comment_str = ""
                if gall_comment > 0:
                    replys = driver.find_elements(By.CLASS_NAME, 'usertxt.ub-word')
                    comment_str = "\n".join(self._clean_text(reply.text) for reply in replys)
            except:
                gall_comment = gall_replynum = 0
                comment_str = ""
            
            return {
                "index": index,
                "title": title,
                "writer": write,
                "views": gall_count,
                "comments_count": gall_comment,
                "likes": gall_replynum,
                "comments": comment_str,
                "keyword": keyword
            }
        except Exception as e:
            print(f"Error extracting post data: {e}")
            return None

    def _clean_text(self, text):
        patterns = [r'#한글', r'- dc official App', r'- dc App', r'coinranktop \. co \. kr']
        cleaned = text.replace("\n\n", " ")
        for pattern in patterns:
            cleaned = re.sub(pattern, '', cleaned)
        return cleaned.strip()

def crawl_keyword(keyword):
    crawler = DcinsideCoroller()
    processed_indices = set()
    keyword_posts = []
    page = 1
    
    while True:
        try:
            posts, has_target_date = crawler.process_page(page, keyword, processed_indices)
            if posts:
                keyword_posts.extend(posts)
            
            if not has_target_date or page >= 15:  # Limit to 15 pages maximum
                break
                
            page += 1
        except Exception as e:
            print(f"Error processing page {page} for keyword {keyword}: {e}")
            break
    
    return keyword_posts

def process_keywords_parallel(keywords):
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(crawl_keyword, keywords))
    
    all_posts = []
    for posts in results:
        if posts:
            all_posts.extend(posts)
    
    if all_posts:
        crawler = DcinsideCoroller()
        crawler.all_posts = all_posts
        crawler.save_to_csv()

def read_keywords_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Keywords file {filename} not found.")
        return []

def main():
    keywords = read_keywords_from_file('keywords.txt')
    if not keywords:
        print("No keywords found. Exiting.")
        return
        
    process_keywords_parallel(keywords)

if __name__ == "__main__":
    main()