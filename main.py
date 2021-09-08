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

            for a in range(9):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                more_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="main-content"]/div/div/div/div/button')))
                more_element.click() #さらに表示クリック
                

            while i < 800 :
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
            while i < 800 :
                url_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,url_path)))
                urls.append(url_element.find_element_by_tag_name("a").get_attribute("href"))
                name_element = browser.find_element_by_xpath(name_path).text
                names.append(name_element)
                i += 1
                url_path = '//*[@id="main-content"]/div/div/div[2]/div/div[2]/div[' + str(i) + ']/div'
                name_path = '//*[@id="main-content"]/div/div/div[2]/div/div[2]/div[' + str(i) + ']/div/a/h3'
                        
        except NoSuchElementException:
            while i < 800 :
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
    return df

selected_url = st.text_input(
    label = 'URLを入力して下さい'
)


def filedownload(df):
    csv = df.to_csv(index=True)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="ranking.csv">Download CSV File</a>'
    return href

if st.button('適用'):
    df1 = scraping(selected_url)
    st.markdown(filedownload(df1), unsafe_allow_html=True)
else:
    st.write('URL入力後適用を押してください')