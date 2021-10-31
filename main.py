from logging import exception
from pandas.core.frame import DataFrame
from selenium import webdriver
from selenium.webdriver import Chrome
from time import sleep
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import streamlit as st
import base64
import chromedriver_binary
import requests
import traceback
from locator import Recommendation_for_you

chrome_options = Options()
#chrome_options.add_argument("--headless", )
#chrome_options.add_argument("--no-sandbox")

def scraping(URL):
    browser = webdriver.Chrome(options=chrome_options)
    url = URL
    browser.get(url)
    
    urls = []
    names = []
    i = 21
    url_path = '//*[@id="main-content"]/div/div[3]/div[2]/div/div[2]/div[' + str(i) + ']/div'
    name_path = '//*[@id="main-content"]/div/div[3]/div[2]/div/div[2]/div[' + str(i) + ']/div/a/h3'     
    try:
        for a in range(10):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            show_more_element = WebDriverWait(browser, 5).until(EC.presence_of_element_located(Recommendation_for_you.show_more))
            show_more_element.click() #さらに表示クリック
    except TimeoutException:
        print('a')
    try:
        while i < 820 :#i=21から800個がmax
            url_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,url_path)))
            urls.append(url_element.find_element_by_tag_name("a").get_attribute("href"))
            print(url_element.find_element_by_tag_name("a").get_attribute("href"))
            name_element = browser.find_element_by_xpath(name_path).text
            names.append(name_element)
            print(name_element)
            i += 1
            url_path = '//*[@id="main-content"]/div/div[3]/div[2]/div/div[2]/div[' + str(i) + ']/div'
            name_path = '//*[@id="main-content"]/div/div[3]/div[2]/div/div[2]/div[' + str(i) + ']/div/a/h3'
    except Exception as e:
        print('e')
    
    if 'https://www.ubereats.com/jp/taco-bout-awkward' in urls :
        urls.remove('https://www.ubereats.com/jp/taco-bout-awkward')
        
    df = pd.DataFrame(index=[],columns=[])
    df['URL'] = urls
    df['NAME'] = names
    
    URL = df['URL'].to_list()
    review_counts = []
    review_rates = []

    def is_number(text):
        if not text:
            return False

        if text.isdecimal():
            return True
        else:
            try:
                float(text)
                return True
            except ValueError:
                return False

    for a in URL:
        browser.get(a)
        sleep(5)
        for review_xpath in Recommendation_for_you.top_review_xpath:
            count = 3
            try:
                rate_element = browser.find_element_by_xpath(review_xpath+"/div["+str(count)+"]")
                for b in range(3):
                    if is_number(rate_element.text):
                        count += 2 
                        count_element = browser.find_element_by_xpath(review_xpath+"/div["+str(count)+"]")
                        judge = 1
                        break
                    else:
                        count += 2
                        rate_element = browser.find_element_by_xpath(review_xpath+"/div["+str(count)+"]")
                break
            except Exception as t:
                judge = 2
                
        if judge == 1 :    
            review_rate=rate_element.text
            print(review_rate)          
            review_count = count_element.text.replace("(", "").replace(")", "")
            print(review_count)
            review_rates.append(review_rate)
            review_counts.append(review_count)
        else :
            review_rates.append(0)
            review_counts.append(0)
            print('nothing')

    df['Revie_rate'] = review_rates
    df['Review_count'] = review_counts

    df_rm = df.index[df.NAME.astype(str).str.contains(
    "マクドナルド|モスバーガー|バーガーキング|ウェンディーズ|ロッテリア|フレッシュネスバーガー|ファーストキッチン|ケンタッキー|吉野家|松屋|すき家|なか卯|ガスト|デニーズ|ロイヤルホスト|ローソン|ほっともっと|ココス|スターバックス|幸楽苑|スシロー|ピザハット|ドミノ・ピザ|ピザーラ|ほっかほっか亭|ジョナサン|サブウェイ|いきなりステーキ|丼丸|大漁丼家|魚丼|てんや",na=False
    )]
    df = df.drop(df_rm)
    return df

    




def filedownload(df):
    csv = df.to_csv(index=True)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="ranking.csv">Download CSV File</a>'
    return href

selected_url_1 = st.text_input(
    label = '1. URLを入力して下さい'
)
selected_name_1 = st.text_input(
    label = '1. 地域名を入力して下さい'
)
st.write('----------------------------------------------')
selected_url_2 = st.text_input(
    label = '2. URLを入力して下さい'
)
selected_name_2 = st.text_input(
    label = '2. 地域名を入力して下さい'
)
st.write('----------------------------------------------')
selected_url_3 = st.text_input(
    label = '3. URLを入力して下さい'
)
selected_name_3 = st.text_input(
    label = '3. 地域名を入力して下さい'
)
st.write('----------------------------------------------')
selected_url_4 = st.text_input(
    label = '4. URLを入力して下さい'
)
selected_name_4 = st.text_input(
    label = '4. 地域名を入力して下さい'
)
st.write('----------------------------------------------')
selected_url_5 = st.text_input(
    label = '5. URLを入力して下さい'
)
selected_name_5 = st.text_input(
    label = '5. 地域名を入力して下さい'
)
selected_url = {selected_url_1:selected_name_2,selected_url_2:selected_name_2,selected_url_3:selected_name_3,selected_url_4:selected_name_4,selected_url_5:selected_name_5}

hook_url = 'https://hooks.slack.com/services/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'

if st.button('適用'):
    data_0 = {
        'payload': '{"channel": "#fdm-market-research-scraping", "username": "webhookbot", "text": "開始", "icon_emoji": "✅"}'
        }
    response = requests.post(hook_url, data=data_0)

    st.write('----------------------------------------------')
    if len (selected_url_1 ) > 0 or len(selected_name_1) > 0:
        try :
            df1 = pd.DataFrame()
            df1 = scraping(selected_url_1)
        except Exception as f:
            error_message = traceback.print_exc()
            data = {
            'payload': '{"channel": "#fdm-market-research-scraping", "username": "webhookbot", "text": "エラー発生(eroorcode:f)", "icon_emoji": "💥"}'
            }
            response = requests.post(hook_url, data=data)
        st.write(selected_name_1 + 'のダウンロードはこちら↓') 
        st.markdown(filedownload(df1), unsafe_allow_html=True)
        data_1 = {
            'payload': '{"channel": "#fdm-market-research-scraping", "username": "webhookbot", "text": "終了", "icon_emoji": "✅"}'
            }
        response = requests.post(hook_url, data=data_1)
    else:
        st.write('1. URL・地域名を入力して下さい')

    st.write('----------------------------------------------')

    if len (selected_url_2 ) > 0 or len(selected_name_2) > 0:
        try :
            df2 = pd.DataFrame()
            df2 = scraping(selected_url_2)
        except Exception as f:
            error_message = traceback.print_exc()
            data = {
            'payload': '{"channel": "#fdm-market-research-scraping", "username": "webhookbot", "text": "エラー発生(eroorcode:f)", "icon_emoji": "💥"}'
            }
            response = requests.post(hook_url, data=data)
        st.write(selected_name_2 + 'のダウンロードはこちら↓') 
        st.markdown(filedownload(df2), unsafe_allow_html=True)
        data_1 = {
            'payload': '{"channel": "#fdm-market-research-scraping", "username": "webhookbot", "text": "終了", "icon_emoji": "✅"}'
            }
        response = requests.post(hook_url, data=data_1)
    else:
        st.write('2. URL・地域名を入力して下さい')
    st.write('----------------------------------------------')
    if len (selected_url_3 ) > 0 or len(selected_name_3) > 0:
        try :
            df3 = pd.DataFrame()
            df3 = scraping(selected_url_3)
        except Exception as f:
            error_message = traceback.print_exc()
            data = {
            'payload': '{"channel": "#fdm-market-research-scraping", "username": "webhookbot", "text": "エラー発生(eroorcode:f)", "icon_emoji": "💥"}'
            }
            response = requests.post(hook_url, data=data)
        st.write(selected_name_3 + 'のダウンロードはこちら↓') 
        st.markdown(filedownload(df3, unsafe_allow_html=True))
        data_1 = {
            'payload': '{"channel": "#fdm-market-research-scraping", "username": "webhookbot", "text": "終了", "icon_emoji": "✅"}'
            }
        response = requests.post(hook_url, data=data_1)
    else:
        st.write('3. URL・地域名を入力して下さい')
    st.write('----------------------------------------------')
    if len (selected_url_4 ) > 0 or len(selected_name_4) > 0:
        try :
            df4 = pd.DataFrame()
            df4 = scraping(selected_url_4)
        except Exception as f:
            error_message = traceback.print_exc()
            data = {
            'payload': '{"channel": "#fdm-market-research-scraping", "username": "webhookbot", "text": "エラー発生(eroorcode:f)", "icon_emoji": "💥"}'
            }
            response = requests.post(hook_url, data=data)
        st.write(selected_name_4 + 'のダウンロードはこちら↓') 
        st.markdown(filedownload(df4), unsafe_allow_html=True)
        data_1 = {
            'payload': '{"channel": "#fdm-market-research-scraping", "username": "webhookbot", "text": "終了", "icon_emoji": "✅"}'
            }
        response = requests.post(hook_url, data=data_1)
    else:
        st.write('4. URL・地域名を入力して下さい')
    st.write('----------------------------------------------')
    if len (selected_url_5 ) > 0 or len(selected_name_5) > 0:
        try :
            df5 = pd.DataFrame()
            df5 = scraping(selected_url_5)
        except Exception as f:
            error_message = traceback.print_exc()
            data = {
            'payload': '{"channel": "#fdm-market-research-scraping", "username": "webhookbot", "text": "エラー発生(eroorcode:f)", "icon_emoji": "💥"}'
            }
            response = requests.post(hook_url, data=data)
        st.write(selected_name_5 + 'のダウンロードはこちら↓') 
        st.markdown(filedownload(df5), unsafe_allow_html=True)
        data_1 = {
            'payload': '{"channel": "#fdm-market-research-scraping", "username": "webhookbot", "text": "終了", "icon_emoji": "✅"}'
            }
        response = requests.post(hook_url, data=data_1)
    else:
        st.write('5. URL・地域名を入力して下さい')
else:
    st.write('URL入力後適用を押してください')
