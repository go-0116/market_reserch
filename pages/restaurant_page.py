from logging import exception

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import requests
import traceback
from utils.locator import Recommendation_for_you
import json

class restaurant_page :
    def __init__(self,browser):
        self.browser = browser
    def get_review_rate_and_count(self):
        for review_xpath in Recommendation_for_you.top_review_xpath:
            try:
                elements = self.browser.find_elements_by_xpath(review_xpath+"/div")
                place_of_review_count = len(elements)
                place_of_review_rate = place_of_review_count -2
                rate_element = self.browser.find_element_by_xpath(review_xpath+"/div["+str(place_of_review_rate)+"]")
                count_element = self.browser.find_element_by_xpath(review_xpath+"/div["+str(place_of_review_count)+"]")
                judge =1
                break
            except Exception as t:
                judge = 2
                
        if judge == 1 : 
            review_rate =rate_element.text
            review_count = count_element.text.replace("(", "").replace(")", "") 
            if not self.is_number(review_rate):
                review_rate = 0
                review_count = 0
                print('haha')
        else :
            review_rate = 0
            review_count = 0
        print(review_rate)
        print(review_count)
        return (review_rate,review_count)

    def is_number(self,text):
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
    
    def check_percentage_of_0(self,hook_url,channel) :
        percentage_0 = self.review_rates.count(0) / len(self.review_rates)
        if percentage_0 > 0.5:
            data=json.dumps({
                "text":"0が50％以上",
                "icon_emoji": "💥",
                "username": "webhookbot",
                "channel": channel
                })
            response = requests.post(hook_url, data=data)
    
    def remove_chain_store(df):
        df_rm = df.index[df.NAME.astype(str).str.contains(
        "マクドナルド|モスバーガー|バーガーキング|ウェンディーズ|ロッテリア|フレッシュネスバーガー|ファーストキッチン|ケンタッキー|吉野家|松屋|すき家|なか卯|ガスト|デニーズ|ロイヤルホスト|ローソン|ほっともっと|ココス|スターバックス|幸楽苑|スシロー|ピザハット|ドミノ・ピザ|ピザーラ|ほっかほっか亭|ジョナサン|サブウェイ|いきなりステーキ|丼丸|大漁丼家|魚丼|てんや",na=False
        )]
        df = df.drop(df_rm)
        return df
