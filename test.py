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

chrome_options = Options()
chrome_options.add_argument("--headless", )

browser = webdriver.Chrome(options=chrome_options)
url = 'https://www.ubereats.com/jp/feed?pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMiVFNSVBNSVBNSVFNiVCMiVBMiVFRiVCQyU5NSVFNCVCOCU4MSVFNyU5QiVBRSVFRiVCQyU5MiVFRiVCQyU5OCVFMiU4OCU5MiVFRiVCQyU5MSVFRiVCQyU5NSUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUo5X2s0M2g3MUdHQVJxMlNZeThkTjlaQSUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EzNS42MDYzNDk4JTJDJTIybG9uZ2l0dWRlJTIyJTNBMTM5LjY2Nzk4MzglN0Q%3D&ps=1&sf=JTVCJTdCJTIydXVpZCUyMiUzQSUyMjFjN2NmN2VmLTczMGYtNDMxZi05MDcyLTI2YmMzOWY3YzAyMSUyMiUyQyUyMm9wdGlvbnMlMjIlM0ElNUIlN0IlMjJ1dWlkJTIyJTNBJTIyNGM3Y2Y3ZWYtNzMwZi00MzFmLTkwNzItMjZiYzM5ZjdjMDIzJTIyJTdEJTVEJTdEJTVE'
browser.get(url)
try:
    for a in range(9):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        more_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="main-content"]/div/div/div/div/button')))
        more_element.click() #さらに表示クリック
except TimeoutException:
    print('E')

try:
    print('2')
except:
    print('5')

