from selenium.webdriver.support.expected_conditions import number_of_windows_to_be
from pages.home_page import home_page
from pages.restaurant_page import restaurant_page
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import pandas as pd
import json
import requests
from time import sleep
import streamlit as st
import base64
import chromedriver_binary
import requests
import traceback
import json

hook_url="https://hooks.slack.com/services/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"

chrome_options = Options()
#chrome_options.add_argument("--headless", )
#chrome_options.add_argument("--no-sandbox")

browser = webdriver.Chrome(options=chrome_options)

def market_reserch(home_url):
    market = home_page(browser)
    market.browser.get(home_url)
    market.show_more()
    count = 1
    count += market.number_of_first_recommendation(count)
    print(count)
    count += market.find_category(count)
    print(count)
    count += market.number_of_first_recommendation(count) #first_recommendationの間にcategoryがあるため二回行っている
    print(count)
    number_of_restaurant = market.number_of_restaurant('//*[@id="main-content"]/div/div[3]/div[2]/div/div[2]/div')
 
    urls = []
    names = []

    
    while count <= number_of_restaurant:
        url_path = '//*[@id="main-content"]/div/div[3]/div[2]/div/div[2]/div[' + str(count) + ']/div'
        name_path = '//*[@id="main-content"]/div/div[3]/div[2]/div/div[2]/div[' + str(count) + ']/div/a/h3' 
        print(market.get_url(url_path))
        print(market.get_name(name_path))
        urls.append(market.get_url(url_path))
        names.append(market.get_name(name_path))
        count += 1
    
    if 'https://www.ubereats.com/jp/taco-bout-awkward' in urls :
        urls.remove('https://www.ubereats.com/jp/taco-bout-awkward')

    df = pd.DataFrame(index=[],columns=[])
    df['URL'] = urls
    df['NAME'] = names

    URL = df['URL'].to_list()
    review_counts = []
    review_rates = []

    hook_url="https://hooks.slack.com/services/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"

    Restaurants = restaurant_page(browser)
    for a in URL:
        Restaurants.browser.get(a)
        sleep(5)
        review_rate, review_count = Restaurants.get_review_rate_and_count()
        
        review_rates.append(review_rate)
        review_counts.append(review_count)

    
    Restaurants.check_percentage_of_0(hook_url, "#fdm-market-research-scraping")

    df['Revie_rate'] = review_rates
    df['Review_count'] = review_counts

    df = Restaurants.remove_chain_store(df)
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


if st.button('適用'):
    
    data_0 = {
        'payload': '{"channel": "#fdm-market-research-scraping", "username": "webhookbot", "text": "開始", "icon_emoji": "✅"}'
        }
    response = requests.post(hook_url, data=data_0)

    st.write('----------------------------------------------')
    if len (selected_url_1 ) > 0 or len(selected_name_1) > 0:
        try :
            df1 = pd.DataFrame()
            df1 = market_reserch(selected_url_1)
        except Exception as f:
            error_message = traceback.format_exc()
            data=json.dumps({
                "text":f"エラー発生{f}"+error_message,
                "icon_emoji": "💥",
                "username": "webhookbot",
                "channel": "#fdm-market-research-scraping"
                })
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
            df2 = market_reserch(selected_url_2)
        except Exception as f:
            error_message = traceback.format_exc()
            data=json.dumps({
                "text":f"エラー発生{f}"+error_message,
                "icon_emoji": "💥",
                "username": "webhookbot",
                "channel": "#fdm-market-research-scraping"
                })
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
            df3 = market_reserch(selected_url_3)
        except Exception as f:
            error_message = traceback.format_exc()
            data=json.dumps({
                "text":f"エラー発生{f}"+error_message,
                "icon_emoji": "💥",
                "username": "webhookbot",
                "channel": "#fdm-market-research-scraping"
                })
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
            df4 = market_reserch(selected_url_4)
        except Exception as f:
            error_message = traceback.format_exc()
            data=json.dumps({
                "text":f"エラー発生{f}"+error_message,
                "icon_emoji": "💥",
                "username": "webhookbot",
                "channel": "#fdm-market-research-scraping"
                })
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
            df5 = market_reserch(selected_url_5)
        except Exception as f:
            error_message = traceback.format_exc()
            data=json.dumps({
                "text":f"エラー発生{f}"+error_message,
                "icon_emoji": "💥",
                "username": "webhookbot",
                "channel": "#fdm-market-research-scraping"
                })
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
