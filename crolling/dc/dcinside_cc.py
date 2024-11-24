from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import datetime
import re
import csv
import os

class DcinsideCoroller:
    def __init__(self):
        targetday = datetime.date.today() - datetime.timedelta(days=1)
        nonetargetday = datetime.date.today() - datetime.timedelta(days=2)
        self.today = datetime.date.today().strftime("%m.%d")
        self.driver = webdriver.Chrome()
        self.targetday = targetday.strftime("%m.%d")
        self.nonetargetday = nonetargetday.strftime("%m.%d")
        self.today_time_pattern = re.compile(r'^\d{2}:\d{2}$')
        self.next_herf = ""
        self.all_posts = []  # List to store all posts across keywords

    def is_find_date(self, page_url=""):
        if page_url:
            self.driver.get(page_url)
        
        date_list = self.driver.find_elements(By.CLASS_NAME, "gall_date")
        dates = [date.text for date in date_list]
        
        return self.targetday in dates

    def today_keyword_find(self, keyword):
        # Initial search page for the keyword
        page_url = f"https://gall.dcinside.com/board/lists/?id=bitcoins_new1&s_type=search_subject_memo&s_keyword={keyword}"
        self.driver.get(page_url)
        
        found_target_day = False
        processed_indices = set()
        keyword_posts = []
        
        while not found_target_day:
            # Get page indices
            index_info = self.get_index()
            
            # Process each index
            for index in index_info:
                # Skip already processed indices
                if index in processed_indices:
                    continue
                
                # Get post data
                page_url = f"https://gall.dcinside.com/board/view/?id=bitcoins_new1&no={index}&s_type=search_subject_memo&s_keyword={keyword}"
                self.driver.get(page_url)
                
                # Get post date
                date_element = self.driver.find_element(By.CLASS_NAME, "gall_date")
                post_date = date_element.text
                
                # Check if post is from target day
                if self.targetday == post_date:
                    # Process and store the post data
                    post_data = self.get_data(index, keyword)
                    post_data['keyword'] = keyword  # Add keyword to the post data
                    keyword_posts.append(post_data)
                    found_target_day = True
                    processed_indices.add(index)
                elif not self.today_time_pattern.match(post_date):
                    # If the post is not from today and not a time (HH:MM)
                    break
                
                processed_indices.add(index)
            
            # If no more posts from target day, navigate to next page
            if not found_target_day:
                try:
                    link_element = self.driver.find_element(By.CLASS_NAME, 'search_next')
                    self.next_herf = link_element.get_attribute('href')
                    link_element.click()
                except:
                    # No more pages to search
                    break
        
        # Add collected posts to the overall list
        self.all_posts.extend(keyword_posts)
        return keyword_posts

    def get_index(self):
        indexes = self.driver.find_elements(By.CLASS_NAME, "gall_num")
        not_post = ["설문", "AD", "공지"]
        index_list = [index.text for index in indexes if index.text not in not_post]
        return index_list
    
    def get_data(self, index, keyword):
        page_url = f"https://gall.dcinside.com/board/view/?id=bitcoins_new1&no={index}&s_type=search_subject_memo&s_keyword={keyword}"
        self.driver.get(page_url)
        
        # Extract post details
        title = self.driver.find_element(By.CLASS_NAME, "title_subject").text
        write = self.driver.find_element(By.CLASS_NAME, "write_div").text.replace("\n\n", " ")
        gall_count = int(self.driver.find_element(By.CLASS_NAME, "gall_count").text.replace("조회", ""))
        
        # Optional: Get comments
        try:
            gall_comment = int(self.driver.find_element(By.CLASS_NAME, "gall_comment").text.replace("댓글", ""))
            gall_replynum = int(self.driver.find_element(By.CLASS_NAME, "gall_reply_num").text.replace("추천", ""))
            
            if gall_comment > 0:
                replys = self.driver.find_elements(By.CLASS_NAME, 'usertxt.ub-word')
                comment_str = "\n".join([reply.text for reply in replys])
            else:
                comment_str = ""
        except:
            gall_comment = 0
            gall_replynum = 0
            comment_str = ""
        
        # Return a dictionary of post details
        return {
            "index": index,
            "title": title,
            "writer": write,
            "views": gall_count,
            "comments_count": gall_comment,
            "likes": gall_replynum,
            "comments": comment_str
        }

    def save_to_csv(self, filename=None):
        # If no filename provided, create a default filename with today's date
        if filename is None:
            filename = f"dcinside_crawl_{self.today}.csv"
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Write to CSV
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            # If posts exist, write the CSV
            if self.all_posts:
                # Get all keys from the first post to use as fieldnames
                fieldnames = list(self.all_posts[0].keys())
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for post in self.all_posts:
                    writer.writerow(post)
                
                print(f"Saved {len(self.all_posts)} posts to {filename}")
            else:
                print("No posts to save.")

def read_keywords_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            keywords = [line.strip() for line in file if line.strip()]
        return keywords
    except FileNotFoundError:
        print(f"Keywords file {filename} not found.")
        return []

def main():
    # Read keywords from file
    keywords = read_keywords_from_file('keywords.txt')
    
    if not keywords:
        print("No keywords found. Exiting.")
        return
    
    # Create crawler instance
    croller = DcinsideCoroller()
    
    # Crawl for each keyword
    for keyword in keywords:
        print(f"Crawling for keyword: {keyword}")
        croller.today_keyword_find(keyword)
    
    # Save results to CSV
    croller.save_to_csv()
    
    # Close the browser
    croller.driver.quit()

if __name__ == "__main__":
    main()