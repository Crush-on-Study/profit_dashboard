import re
# 입력 파일 경로
input_file_path = 'urls.txt'

# 파일에서 URL을 읽어옴
with open(input_file_path, 'r', encoding='utf-8') as file:
    urls = file.readlines()

# 페이지 번호 범위 설정
page_range = range(1, 11)

# 각 URL에 대해 페이지 번호를 변경하여 출력
for url in urls:
    base_url = url.strip()  # 줄 끝의 공백 문자 제거
    for page in page_range:
        # page 파라미터를 동적으로 변경
        
        print(current_page_url)
