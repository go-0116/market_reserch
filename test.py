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

browser = webdriver.Chrome(options=chrome_options)
url = 'https://www.ubereats.com/jp/store/%E3%83%9E%E3%82%AF%E3%83%88%E3%83%8A%E3%83%AB%E3%83%88-%E6%B8%8B%E8%B0%B7%E5%BA%97-mcdonalds-shibuya/04J4ikZqRyuOijQ20HoUDw'
browser.get(url)