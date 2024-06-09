# https://jheaon.tistory.com/128
# https://velog.io/@one_step/selenium-%EA%B8%B0%EC%B4%88 기초
# 기사 검색 후 무한 스크롤까지 모듈화   /   기사 스크랩 모듈화
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from tkinter import messagebox

import time
import pyautogui
import webbrowser
import tkinter as tk
import datetime

keywords = []
Input_keyword = pyautogui.prompt("검색어를 입력하세요.")
keywords.append(Input_keyword)

# 유사검색어 추가
similar_keyword = messagebox.askquestion(
    "질문", "유사 검색어 추가를 하시겠습니까?", icon='warning', default='no')
if similar_keyword == 'yes':
    while True:
        search_term = pyautogui.prompt("유사 검색어 추가 (cancel을 누르면 추가종료)")
        if search_term is None:  # User pressed Cancel
            break
        else:
            keywords.append(search_term)


result = messagebox.askquestion(
    "질문", "기간 검색을 하시겠습니까?", icon='warning', default='no')
if result == 'yes':
    # 기간 검색
    start_date = pyautogui.prompt("시작일을 지정하세요 (ex) 2014.01.01")  # 2014.01.01
    end_date = str(datetime.date.today().strftime("%Y.%m.%d"))  # TODAY
    url = f"https://search.naver.com/search.naver?where=news&query="+Input_keyword+"&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds="+start_date+"&de="+end_date + \
        "&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20140101to20240211&is_sug_officeid=0&office_category=0&service_area=0"
else:
    # 일반검색
    url = f"https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query="+Input_keyword
driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)


# infinite-scroller
# 스크롤 왜 되는거지? https://ddingmin00.tistory.com/entry/Selenium-%ED%8E%98%EC%9D%B4%EC%A7%80%EB%A5%BC-%EB%82%B4%EB%A0%A4%EA%B0%80%EB%A9%B0-%EB%AC%B4%ED%95%9C-%ED%81%AC%EB%A1%A4%EB%A7%81-%ED%95%98%EA%B8%B0
actions = driver.find_element(By.CSS_SELECTOR, 'body')  # 어째서 스크롤 기능을 하는거지?
before_h = driver.execute_script("return window.scrollY")
# cnt = 0
while True:
    actions.send_keys(Keys.END)  # 스크롤
    time.sleep(1)
    after_h = driver.execute_script("return window.scrollY")

    # 더이상 스크롤이 되지 않는다면
    # if cnt == 50:
    #     break
    if after_h == before_h:
        break
    before_h = after_h


# crowling, 검사 (제목, 본문)
links_selector = " #main_pack > section > div.api_subject_bx > div.group_news > ul > li > div > div > div.news_contents > a.news_tit"
links = driver.find_elements(By.CSS_SELECTOR, links_selector)

texts_selector = "#main_pack > section > div.api_subject_bx > div.group_news > ul > li > div > div > div.news_contents > div > div > a"
texts = driver.find_elements(By.CSS_SELECTOR, texts_selector)

url_list = []
for link, text in zip(links, texts):
    news_tit = link.get_attribute("title")  # 제목
    news_tex = text.get_attribute("text")  # 본문

    # if any(표현식 for 변수 in 순회할_리스트)  -> `keywords` 리스트의 각 요소를 하나씩 순회하면서, 해당 요소가 `news_tit`에 포함되어 있다면 `True`를 반환
    if any(keyword in news_tit for keyword in keywords):  # 제목 O
        news_url = link.get_attribute("href")
        print("제목 : ", news_tit)
        print("링크 : ", news_url)
        print()
        url_list.append(news_url)
    elif any(keyword in news_tex for keyword in keywords):  # 제목 x, 본문 o
        news_url = link.get_attribute("href")
        print("제목 : ", news_tit)
        print("링크 : ", news_url)
        print("본문 O")
        print()
        url_list.append(news_url)

print("총 갯수 : ", len(url_list))
driver.quit()

# window 창
# button 생성
# button 기능
# click count

# Create window
window = tk.Tk()
# Set window title
window.title("Button Window")
# Resize window
window_width = 250
window_height = 100
window.geometry(f"{window_width}x{window_height}")


# url_list의 url로 기사 띄우기 전 범위 설정
start = 0
article_cnt = 0
if len(url_list) >= 5:
    end = 5
else:
    end = len(url_list)


def button_clicked():
    global start, end, article_cnt, url_list
    for url in url_list[start:end]:
        webbrowser.open(url)
    if end+5 <= len(url_list):
        start = end
        article_cnt = end
        end += 5
    elif start == end:
        print("!!종료!!")
        window.quit()
    else:
        start = end
        article_cnt = end
        end = len(url_list)

    # print(start, end)
    label_click_count.config(text=f"{article_cnt} / {len(url_list)}")


# Create button    + lambda는 def 같은거
button = tk.Button(window, text="Click Me!", command=button_clicked)
button.pack()
# Create a label to display click count
label_click_count = tk.Label(window, text=f"{article_cnt} / {len(url_list)}")
label_click_count.pack()

# Run the main event loop
window.mainloop()

url_list = []
