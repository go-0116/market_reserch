'''
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


browser = webdriver.Chrome(options=chrome_options)
url = 'https://www.ubereats.com/jp/feed?ps=1&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMiVFNSU4QSVBMCVFNSU4RiVBNCVFNSVCNyU5RCVFNSVCOCU4MiUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUpnVU95UGVJblZUVVJuemZ1c0hMbDRqVSUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EzNC43NTY5MTkzJTJDJTIybG9uZ2l0dWRlJTIyJTNBMTM0Ljg0MTM2JTdE'
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
        count = 1
        try:
            rate_element = browser.find_element_by_xpath(review_xpath+"/div["+str(count)+"]")
            for b in range(4):
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
a = review_rates.count(0) / len(review_rates)
print(a)
if a > 0.5:
    print(1111)
'''
import slackweb

slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
slack.notify(text="pythonからslackさんへ")

