from logging import exception
from pandas.core.frame import DataFrame
from selenium import webdriver
from selenium.webdriver import Chrome
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import streamlit as st
import base64
import chromedriver_binary

chrome_options = Options()
chrome_options.add_argument("--headless", )
chrome_options.add_argument("--no-sandbox")

def scraping(URL):
    browser = webdriver.Chrome(options=chrome_options)
    url = URL
    browser.get(url)

    urls = []
    names = []
    i = 1
    url_path = '//*[@id="main-content"]/div/div/div[2]/div/div[2]/div[' + str(i) + ']/div'
    url_path_2 = '//*[@id="main-content"]/div/div/div[2]/div/div[4]/div[' + str(i) + ']/div'
    url_path_3 = '//*[@id="main-content"]/div/div/div/div/div[5]/div[' + str(i) + ']/div'
    name_path = '//*[@id="main-content"]/div/div/div[2]/div/div[2]/div[' + str(i) + ']/div/a/h3'
    is_selected_popular_sorted = False
    try:
        popular_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/input[2]')))
        #if not popular_element.is_selected():   
        popular_element.find_element_by_xpath("following-sibling::label").click()  #最も人気の料理クリック

        for a in range(9):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                more_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="main-content"]/div/div/div/div/button')))
                more_element.click() #さらに表示クリック

    except Exception as e:
        print(e)
    else:
        is_selected_popular_sorted = True
        

    if not is_selected_popular_sorted:
        try:
            rearrange_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="main-content"]/div/div[3]/div/div/div[1]/div/div[1]/div')))
            rearrange_element.click()
            popular_element = browser.find_element_by_xpath('//*[@id="main-content"]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/label[2]')
            popular_element.click()  #最も人気の料理クリック 

            for a in range(2):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                more_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="main-content"]/div/div/div/div/button')))
                more_element.click() #さらに表示クリック
                

            while i < 10 :
                url_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,url_path_3)))
                urls.append(url_element.find_element_by_tag_name("a").get_attribute("href"))
                name_element = browser.find_element_by_xpath(name_path).text
                names.append(name_element)
                name_path = '//*[@id="main-content"]/div/div/div[2]/div/div[2]/div[' + str(i) + ']/div/a/h3'
                i += 1
                url_path_3 = '//*[@id="main-content"]/div/div/div/div/div[5]/div[' + str(i) + ']/div'
                name_path = '//*[@id="main-content"]/div/div/div[2]/div/div[2]/div[' + str(i) + ']/div/a/h3'

        except Exception as f:
            print(f)

    elif is_selected_popular_sorted:
        try:
            while i < 10 :
                url_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,url_path)))
                urls.append(url_element.find_element_by_tag_name("a").get_attribute("href"))
                name_element = browser.find_element_by_xpath(name_path).text
                names.append(name_element)
                i += 1
                url_path = '//*[@id="main-content"]/div/div/div[2]/div/div[2]/div[' + str(i) + ']/div'
                name_path = '//*[@id="main-content"]/div/div/div[2]/div/div[2]/div[' + str(i) + ']/div/a/h3'
                        
        except NoSuchElementException:
            while i < 10 :
                url_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,url_path_2)))
                urls.append(url_element.find_element_by_tag_name("a").get_attribute("href"))
                name_element = browser.find_element_by_xpath(name_path).text
                names.append(name_element)  
                i += 1
                url_path_2 = '//*[@id="main-content"]/div/div/div[2]/div/div[4]/div[' + str(i) + ']/div'     
                name_path = '//*[@id="main-content"]/div/div/div[2]/div/div[2]/div[' + str(i) + ']/div/a/h3'

        except Exception as e:
            print(e)

    df = pd.DataFrame(index=[],columns=[])
    df['URL'] = urls
    df['NAME'] = names
    
    URL = df['URL'].to_list()
    review_count = []
    review_rate = []
    print(URL)

    for a in URL:
        try:
            browser.get(a)
            review_rate_element = browser.find_element_by_xpath('//*[@id="main-content"]/div[3]/div/div[4]/div[3]/div[1]/div[2]/div[2]/div[1]/div[1]')
            review_rate.append(review_rate_element.text)

            review_counts_element = browser.find_element_by_xpath('//*[@id="main-content"]/div[3]/div/div[4]/div[3]/div[1]/div[2]/div[2]/div[1]/div[3]')
            review_counts_1 = review_counts_element.text.replace('(','')
            review_counts_2 = review_counts_1.replace(')','')
            review_count.append(review_counts_2)
        except NoSuchElementException:
            review_rate.append('0')
            review_count.append('0')
    review_rate_1 = [x for x in review_rate if x != '配達予定時間と配送手数料を表示します。\nお届け先の住所を入力してください']
    print(review_rate_1)
    print(review_count)

    df['Revie_rate'] = review_rate
    df['Review_count'] = review_count
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
    st.write('----------------------------------------------')
    if len (selected_url_1 ) > 0 or len(selected_name_1) > 0:
        df1 = scraping(selected_url_1)
        st.write(selected_name_1 + 'のダウンロードはこちら↓') 
        st.markdown(filedownload(df1), unsafe_allow_html=True)
    else:
        st.write('1. URL・地域名を入力して下さい')
    st.write('----------------------------------------------')

    if len (selected_url_2 ) > 0 or len(selected_name_2) > 0:
        df2 = scraping(selected_url_2)
        st.write(selected_name_2 + 'のダウンロードはこちら↓') 
        st.markdown(filedownload(df2), unsafe_allow_html=True)
    else:
        st.write('2. URL・地域名を入力して下さい')
    st.write('----------------------------------------------')
    if len (selected_url_3 ) > 0 or len(selected_name_3) > 0:
        df3 = scraping(selected_url_3)
        st.write(selected_name_3 + 'のダウンロードはこちら↓') 
        st.markdown(filedownload(df3), unsafe_allow_html=True)
    else:
        st.write('3. URL・地域名を入力して下さい')
    st.write('----------------------------------------------')
    if len (selected_url_4 ) > 0 or len(selected_name_4) > 0:
        df4 = scraping(selected_url_4)
        st.write(selected_name_4 + 'のダウンロードはこちら↓') 
        st.markdown(filedownload(df4), unsafe_allow_html=True)
    else:
        st.write('4. URL・地域名を入力して下さい')
    st.write('----------------------------------------------')
    if len (selected_url_5 ) > 0 or len(selected_name_5) > 0:
        df5 = scraping(selected_url_5)
        st.write(selected_name_5 + 'のダウンロードはこちら↓') 
        st.markdown(filedownload(df5), unsafe_allow_html=True)
    else:
        st.write('5. URL・地域名を入力して下さい')
else:
    st.write('URL入力後適用を押してください')