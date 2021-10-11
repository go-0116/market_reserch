from logging import exception
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

chrome_options = Options()
#chrome_options.add_argument("--headless", )

browser = webdriver.Chrome(options=chrome_options)
url = 'https://www.ubereats.com/jp/store/%E3%81%A1%E3%82%83%E3%81%82%E3%81%97%E3%82%85%E3%81%86%E3%82%84%E4%BA%80%E7%8E%8B-chasyuya-kiou/hboalW7DQzqAjkLyzg2OJQ?mod=storeDeliveryTime&modctx=%7B%22encodedStoreUuid%22%3A%22hboalW7DQzqAjkLyzg2OJQ%22%7D&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMiVFNSU4QSVBMCVFNSU4RiVBNCVFNSVCNyU5RCVFNyU5NCVCQSVFNSVBRiVCQSVFNSVBRSVCNiVFNyU5NCVCQSVFRiVCQyU5MSVFRiVCQyU5NCVFRiVCQyU5MSUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUp1MmtUa0JIWVZEVVJyV2pXWG0yWnd4cyUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EzNC43NjU1NjM3JTJDJTIybG9uZ2l0dWRlJTIyJTNBMTM0LjgzNzE4OTklN0Q%3D&ps=1'
browser.get(url)

try:
    review_rate_element = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="main-content"]/div[3]/div/div[4]/div[3]/div[1]/div[2]/div[2]/div[1]/div[1]')))
    review_rate_1 = review_rate_element.text
    print(review_rate_1)
    print('km' in review_rate_1)
    if 'km' in review_rate_1:
        review_rate_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="main-content"]/div[3]/div/div[4]/div[3]/div[1]/div[2]/div[2]/div[1]/div[3]')))
        review_counts_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="main-content"]/div[3]/div/div[4]/div[3]/div[1]/div[2]/div[2]/div[1]/div[5]')))
        review_counts_1 = review_counts_element.text.replace('(','')
        review_counts_2 = review_counts_1.replace(')','')
        judge =1
    else :
        review_counts_element = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="main-content"]/div[3]/div/div[4]/div[3]/div[1]/div[2]/div[2]/div[1]/div[3]')))
        review_counts_1 = review_counts_element.text.replace('(','')
        review_counts_2 = review_counts_1.replace(')','')
        judge =1

except TimeoutException:
    judge =2

if judge == 1 :
    print(review_rate_element.text)
    print(review_counts_2)
else:
    print('nothing')


