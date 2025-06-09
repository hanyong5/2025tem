
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
import json


options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


url = "https://www.naver.com"

# browser에서 url 열기
browser.get(url)
print(browser.title)

browser.find_element(By.ID, 'query').click()
browser.find_element(By.ID, 'query').send_keys("날씨") # 검색어 입력
browser.find_element(By.CLASS_NAME,'btn_search').click()


# 온도 정보가 나타날 때까지 최대 10초 대기
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.temperature_text strong'))
)


data = browser.find_element(By.CSS_SELECTOR, '.temperature_text strong').text.replace('현재 온도', '').replace('°', '').strip()

print(data)



# 현재 날짜와 시간 가져오기
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 데이터프레임 생성
# df = pd.DataFrame({
#     'datetime': [current_time],
#     'temperature': [data]
# })

# CSV 파일이 존재하면 추가, 없으면 새로 생성
# try:
#     existing_df = pd.read_csv('data.csv')
#     updated_df = pd.concat([existing_df, df], ignore_index=True)
#     updated_df.to_csv('data.csv', index=False)
# except FileNotFoundError:
#     df.to_csv('data.csv', index=False)


# 현재 데이터를 딕셔너리 형태로 변환
data_dict = {
    'datetime': current_time,
    'temperature': data
}

try:
    # 기존 JSON 파일 읽기
    with open('data.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
        if isinstance(existing_data, list):
            existing_data.insert(0, data_dict)
        else:
            existing_data = [data_dict]
except FileNotFoundError:
    # 파일이 없는 경우 새로운 리스트 생성
    existing_data = [data_dict]

# JSON 파일로 저장
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=4)



print(f"데이터가 저장되었습니다: {current_time}, {data}")

