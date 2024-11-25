import time
import datetime
import re
import os
import csv
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class DcinsideCoroller:
    def __init__(self):
        targetday = datetime.date.today() - datetime.timedelta(days=1)
        nonetargetday = datetime.date.today() - datetime.timedelta(days=2)
        self.today = datetime.date.today().strftime("%m.%d")
        self.driver = self._get_driver()
        self.driver.implicitly_wait(20)
        self.targetday = targetday.strftime("%m.%d")
        self.targetday = targetday.strftime("%m.%d")
        self.nonetargetday = nonetargetday.strftime("%m.%d")
        self.today_time_pattern = re.compile(r'^\d{2}:\d{2}$')
        self.all_posts = []
        self.current_page_url = ""
    
    def _get_driver(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")  # GUI 없이 실행
        return webdriver.Chrome(options=chrome_options)
    
    def get_unique_filename(self, filename):
        base, extension = os.path.splitext(filename)
        counter = 1
        new_filename = filename

        while os.path.exists(new_filename):
            new_filename = f"{base}_{counter}{extension}"
            counter += 1

        return new_filename

    def save_to_csv(self, filename=None, keyword=None):
        try:
            if filename is None:
                filename = os.path.join(os.getcwd(), f"dcinside_crawl_{self.today}_{keyword}.csv")
            
            filename = self.get_unique_filename(filename)  # 고유한 파일 이름 생성

            file_dir = os.path.dirname(filename)
            if file_dir:
                os.makedirs(file_dir, exist_ok=True)
            
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                if self.all_posts:
                    fieldnames = list(self.all_posts[0].keys())
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for post in self.all_posts:
                        writer.writerow(post)
                    print(f"Saved {len(self.all_posts)} posts to {filename}")
                else:
                    print("No posts to save.")
        except OSError as e:
            print(f"Error creating directory or opening file: {e}")
        except KeyError as e:
            print(f"Error accessing post data: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    def is_find_date(self, page_url=""):
        self.driver.get(page_url)
        date_list = self.driver.find_elements(By.CLASS_NAME, "gall_date")
        return self.targetday in [date.text for date in date_list]



    def today_keyword_find(self, keyword):
        page_url = f"https://gall.dcinside.com/board/lists/?id=bitcoins_new1&page=1&search_pos=&s_type=search_subject_memo&s_keyword={keyword}"
        self.driver.get(page_url)
        finish = False
        processed_indices = set()
        keyword_posts = []
        first_page = True
        self.current_page_url = page_url
        while not finish:
            try:
                bound_page_list = self.find_page_list(first_page)
                for page in bound_page_list:
                    page_url = re.sub(r'page=\d+', f'page={page}', self.current_page_url)
                    self.driver.get(page_url)
                    try:
                        index_info = self.get_index()
                    except:
                        page_url = re.sub(r'page=\d+', f'page={page}', self.current_page_url)
                        self.driver.get(page_url)
                    for index in index_info:
                        if index in processed_indices:
                            continue
                        try:
                            page_url = f"https://gall.dcinside.com/board/view/?id=bitcoins_new1&no={index}&s_type=search_subject_memo&s_keyword={keyword}"
                            self.driver.get(page_url)
                            date_element = self.driver.find_element(By.CLASS_NAME, "gall_date") ##삭제된 게시물일수 있음. 그냥 넘기자
                            post_date = date_element.text
                            date_part = re.search(r'\d{4}\.(\d{2}\.\d{2})', post_date).group(1)
                        except:
                            continue

                        if self.today == date_part:
                            post_data = self.today_get_data(index)
                            if post_data == {}:
                                continue
                            post_data['keyword'] = keyword
                            keyword_posts.append(post_data)
                            processed_indices.add(index)
                        else:
                            finish = True
                            break
                    if finish:
                        break
                if not finish:
                    page_url = f"https://gall.dcinside.com/board/lists/?id=bitcoins_new1&page={page}&search_pos=&s_type=search_subject_memo&s_keyword={keyword}"
                    self.driver.get(page_url)
                    if len(bound_page_list) < 15:
                        if index in processed_indices:
                            finish = True
                            continue
                        self.click_search_page()
                        continue
                    else:
                        try:
                            next_page = self.driver.find_element(By.CLASS_NAME, "sp_pagingicon.page_next")
                            if page == bound_page_list[-1]:
                                first_page = False
                            next_page.click()
                            continue
                        except:
                            self.click_search_page()
                            continue
            except Exception as e:
                self.all_posts.extend(keyword_posts)
                return keyword_posts

    
    def click_search_page(self):
        next_page = self.driver.find_element(By.CLASS_NAME, "search_next")
        self.current_page_url = next_page.get_attribute('href')
        next_page.click()
    
    def find_page_list(self, first_page:bool):
        page_box = self.driver.find_element(By.CLASS_NAME, 'bottom_paging_box.iconpaging')
        page_list = []
        pages = page_box.find_elements(By.TAG_NAME, "a")
        for page in pages:
            if page.text.isdigit():
                page_list.append(page.text)
        empages = page_box.find_element(By.TAG_NAME, "em")
        if first_page:
            page_list.insert(0, empages.text)
        else:
            page_list.append(empages.text)
        return page_list
    
    def get_index(self):
        #container > section.left_content.result > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child(4) > td.gall_num
        gall_list = self.driver.find_element(By.CLASS_NAME, "gall_list")
        rows = gall_list.find_elements(By.CLASS_NAME, "gall_num")
        not_post = ["설문", "AD", "공지"]
        index_list = [index.text for index in rows if index.text not in not_post]
        return index_list
    
    def today_get_data(self, index):
        def remove_specific_phrases(input_str):
            # 제거할 패턴 목록
            patterns = [r'#한글', r'- dc official App', r'- dc App', r'coinranktop \. co \. kr']
            # 각 패턴을 문자열에서 제거
            for pattern in patterns:
                input_str = re.sub(pattern, '', input_str)
            return input_str
        try:
            title = self.driver.find_element(By.CLASS_NAME, "title_subject").text
            write = self.driver.find_element(By.CLASS_NAME, "write_div").text.replace("\n\n", " ")
            write = remove_specific_phrases(write)
            if write.count("'") > 100:
                return {}
            gall_count = int(self.driver.find_element(By.CLASS_NAME, "gall_count").text.replace("조회", ""))        
            try:
                gall_comment = int(self.driver.find_element(By.CLASS_NAME, "gall_comment").text.replace("댓글", ""))
                gall_replynum = int(self.driver.find_element(By.CLASS_NAME, "gall_reply_num").text.replace("추천", ""))
                
                if gall_comment > 0:
                    replys = self.driver.find_elements(By.CLASS_NAME, 'usertxt.ub-word')
                    comment_str = "\n".join([reply.text for reply in replys if '✓' not in reply.text])
                    comment_str = remove_specific_phrases(comment_str)
                else:
                    comment_str = ""
            except:
                gall_comment = 0
                gall_replynum = 0
                comment_str = ""
            
            return {
                "index": index,
                "title": title,
                "writer": write,
                "views": gall_count,
                "comments_count": gall_comment,
                "likes": gall_replynum,
                "comments": comment_str
            }
        except:
            return {}

def read_keywords_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            keywords = [line.strip() for line in file if line.strip()]
        return keywords
    except FileNotFoundError:
        print(f"Keywords file {filename} not found.")
        return []

def crawl_keyword(keyword, result_queue):
    croller = DcinsideCoroller()
    posts = croller.today_keyword_find(keyword)
    result_queue.put(posts)  # Queue에 결과 저장
    croller.driver.quit()

def main():
    keywords = read_keywords_from_file('keywords.txt')
    
    if not keywords:
        print("No keywords found. Exiting.")
        return
    
    manager = multiprocessing.Manager()
    result_queue = manager.Queue()

    processes = []
    for keyword in keywords:
        print(f"Starting crawl for keyword: {keyword}")
        p = multiprocessing.Process(target=crawl_keyword, args=(keyword, result_queue))
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()  
    
    all_posts = []
    while not result_queue.empty():
        all_posts.extend(result_queue.get())

    if all_posts:
        dc_croller = DcinsideCoroller()
        dc_croller.all_posts = all_posts
        dc_croller.save_to_csv()

if __name__ == "__main__":
    main()
