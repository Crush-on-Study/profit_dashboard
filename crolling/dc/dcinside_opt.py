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

@dataclass
class Post:
    index: str
    title: str
    writer: str
    views: int
    comments_count: int
    likes: int
    comments: str
    date:str
    keyword: Optional[str] = None

class DcinsideCoroller:
    BASE_URL = "https://gall.dcinside.com/board"
    GALLERY_ID = "bitcoins_new1"
    
    def __init__(self):
        self.today = datetime.date.today().strftime("%m.%d")
        self.targetday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%m.%d")
        self.driver = self._get_driver()
        self.wait = WebDriverWait(self.driver, 60)
        self.all_posts: List[Dict] = []
        self.current_page_url = ""

    def _get_driver(self) -> webdriver.Chrome:
            """
            Chrome WebDriver를 설정하고 반환합니다.
            """
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920x1080")
            
            # WebGL 관련 경고 해결을 위한 옵션 추가
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
            chrome_options.add_argument("--enable-unsafe-swiftshader")
            chrome_options.add_argument("--disable-software-rasterizer")
            
            # 로그 레벨 설정 추가
            chrome_options.add_argument("--log-level=3")  # WARNING 이상의 로그만 표시
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 불필요한 로그 제외
            
            # PageLoadStrategy 설정
            chrome_options.page_load_strategy = 'eager'
            
            service = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=chrome_options)

    @staticmethod
    def get_unique_filename(filename: str) -> str:
        base, extension = os.path.splitext(filename)
        counter = 1
        new_filename = filename

        while os.path.exists(new_filename):
            new_filename = f"{base}_{counter}{extension}"
            counter += 1

        return new_filename

    def find_page_list(self, first_page: bool) -> List[str]:
            """
            페이지 번호 목록을 찾아서 반환합니다.
            
            Args:
                first_page (bool): 첫 페이지 여부
                
            Returns:
                List[str]: 페이지 번호 목록
            """
            try:
                # 페이징 박스를 찾고 명시적 대기 적용
                page_box = self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'bottom_paging_box.iconpaging'))
                )
                
                # 일반 페이지 번호들 수집
                page_list = []
                pages = page_box.find_elements(By.TAG_NAME, "a")
                for page in pages:
                    if page.text.isdigit():
                        page_list.append(page.text)
                
                # 현재 활성화된 페이지 번호 찾기
                try:
                    current_page = page_box.find_element(By.TAG_NAME, "em")
                    if first_page:
                        page_list.insert(0, current_page.text)
                    else:
                        page_list.append(current_page.text)
                except NoSuchElementException:
                    print("Warning: Could not find current page number")
                
                return sorted(list(set(page_list)), key=int)  # 중복 제거 및 정렬
                
            except TimeoutException:
                print("Warning: Timeout while finding page list")
                return []
            except Exception as e:
                print(f"Error in find_page_list: {e}")
                return []
    def get_index(self) -> List[str]:
            """
            현재 페이지의 게시물 인덱스 목록을 반환합니다.
            
            Returns:
                List[str]: 게시물 인덱스 목록 (설문, AD, 공지 제외)
            """
            try:
                # 명시적 대기로 게시글 목록 로딩 기다림
                gall_list = self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "gall_list"))
                )
                
                # 게시글 번호 요소들 찾기
                rows = gall_list.find_elements(By.CLASS_NAME, "gall_num")
                
                # 설문, AD, 공지 등 제외
                not_post = {"설문", "AD", "공지"}
                index_list = [index.text for index in rows if index.text not in not_post]
                
                return index_list
                
            except TimeoutException:
                print("Warning: Timeout while getting index list")
                return []
            except Exception as e:
                print(f"Error in get_index: {e}")
                return []

    def click_search_page(self) -> None:
        """
        검색 결과의 다음 페이지로 이동합니다.
        
        Raises:
            NoSuchElementException: 다음 페이지 버튼을 찾지 못한 경우
            TimeoutException: 페이지 로드 시간 초과
        """
        try:
            # 명시적 대기로 다음 페이지 버튼 찾기
            next_page = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "search_next"))
            )
            
            # URL 업데이트
            self.current_page_url = next_page.get_attribute('href')
            
            # 클릭 전 버튼이 클릭 가능할 때까지 대기
            clickable_next = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "search_next"))
            )
            clickable_next.click()
            
            # 페이지 로드 대기
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Navigation error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error in click_search_page: {e}")
            raise

    def save_to_csv(self, filename: Optional[str] = None, keyword: Optional[str] = None) -> None:
        try:
            if filename is None:
                filename = os.path.join(os.getcwd(), f"dcinside_crawl_{self.today}_{keyword}.csv")
            
            filename = self.get_unique_filename(filename)
            os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
            
            if not self.all_posts:
                print("No posts to save.")
                return

            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = list(self.all_posts[0].keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.all_posts)
                print(f"Saved {len(self.all_posts)} posts to {filename}")

        except Exception as e:
            print(f"Error saving to CSV: {e}")

    def today_keyword_find(self, keyword: str) -> List[Dict]:
        page_url = f"{self.BASE_URL}/lists/?id={self.GALLERY_ID}&page=1&search_pos=&s_type=search_subject_memo&s_keyword={keyword}"
        self.driver.get(page_url)
        
        processed_indices: Set[str] = set()
        keyword_posts: List[Dict] = []
        first_page = True
        self.current_page_url = page_url

        try:
            while True:
                bound_page_list = self.find_page_list(first_page)
                
                for page in bound_page_list:
                    page_url = re.sub(r'page=\d+', f'page={page}', self.current_page_url)
                    self.driver.get(page_url)
                    
                    try:
                        index_info = self.get_index()
                    except NoSuchElementException:
                        continue

                    for index in index_info:
                        if index in processed_indices:
                            continue

                        post_data = self._process_post(index, keyword)
                        if post_data:
                            keyword_posts.append(post_data)
                            processed_indices.add(index)
                        elif post_data is None:  # 날짜가 today가 아닌 경우
                            return keyword_posts

                if not self._handle_pagination(bound_page_list, first_page):
                    break
                first_page = False

        except Exception as e:
            print(f"Error in keyword find: {e}")
        finally:
            self.all_posts.extend(keyword_posts)
            return keyword_posts

    def _process_post(self, index: str, keyword: str) -> Optional[Dict]:
        try:
            page_url = f"{self.BASE_URL}/view/?id={self.GALLERY_ID}&no={index}&s_type=search_subject_memo&s_keyword={keyword}"
            self.driver.get(page_url)
            
            date_element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gall_date")))
            post_date = date_element.text
            date_part = re.search(r'\d{4}\.(\d{2}\.\d{2})', post_date).group(1)
            
            if self.today != date_part:
                return None

            post_data = self.today_get_data(index)
            if post_data:
                post_data['keyword'] = keyword
            return post_data

        except (TimeoutException, NoSuchElementException):
            return {}
        except Exception as e:
            print(f"Error processing post {index}: {e}")
            return {}

    def _handle_pagination(self, bound_page_list: List[str], first_page: bool) -> bool:
        if len(bound_page_list) < 15:
            try:
                self.click_search_page()
                return True
            except NoSuchElementException:
                return False
        
        try:
            if not first_page or bound_page_list[-1] == self.driver.find_element(By.CLASS_NAME, "sp_pagingicon.page_next").text:
                self.click_search_page()
            else:
                next_page = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "sp_pagingicon.page_next")))
                next_page.click()
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def today_get_data(self, index: str) -> Dict:
        try:
            title = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title_subject"))).text
            write = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "write_div"))).text
            write = self._clean_text(write)
            
            if write.count("'") > 100:
                return {}
                
            gall_count = int(self.wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "gall_count"))).text.replace("조회", ""))
            
            comment_data = self._get_comment_data()
            
            return Post(
                index=index,
                title=title,
                writer=write,
                views=gall_count,
                comments_count=comment_data['count'],
                likes=comment_data['likes'],
                comments=comment_data['text'],
                date=comment_data['date']
            ).__dict__
            
        except Exception:
            return {}

    def _clean_text(self, text: str) -> str:
        patterns = [r'#한글', r'- dc official App', r'- dc App', r'coinranktop \. co \. kr']
        text = text.replace("\n\n", " ")
        for pattern in patterns:
            text = re.sub(pattern, '', text)
        return text.strip()

    def _get_comment_data(self) -> Dict:
        try:
            gall_comment = int(self.driver.find_element(By.CLASS_NAME, "gall_comment").text.replace("댓글", ""))
            gall_replynum = int(self.driver.find_element(By.CLASS_NAME, "gall_reply_num").text.replace("추천", ""))
            gall_date = self.driver.find_element(By.CLASS_NAME, "gall_date").text
            comment_text = ""
            if gall_comment > 0:
                replys = self.driver.find_elements(By.CLASS_NAME, 'usertxt.ub-word')
                comment_text = "\n".join([reply.text for reply in replys if '✓' not in reply.text])
                comment_text = self._clean_text(comment_text)
            
            return {
                'count': gall_comment,
                'likes': gall_replynum,
                'text': comment_text,
                "date":gall_date
            }
        except NoSuchElementException:
            return {'count': 0, 'likes': 0, 'text': ""}

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

def process_keywords(keywords: List[str]) -> List[Dict]:
    with multiprocessing.Pool() as pool:
        results = pool.map(crawl_keyword, keywords)
    return [post for sublist in results for post in sublist if sublist]

def crawl_keyword(keyword: str) -> List[Dict]:
    try:
        crawler = DcinsideCoroller()
        return crawler.today_keyword_find(keyword)
    except Exception as e:
        print(f"Error crawling keyword {keyword}: {e}")
        return []

def read_keywords_from_file(filename: str) -> List[str]:
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

    all_posts = process_keywords(keywords)
    
    if all_posts:
        dc_crawler = DcinsideCoroller()
        dc_crawler.all_posts = all_posts
        dc_crawler.save_to_csv()

if __name__ == "__main__":
    main()