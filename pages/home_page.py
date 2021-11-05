from logging import exception
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.locator import Recommendation_for_you


class home_page:
    def __init__(self,browser):
        self.browser = browser
    def show_more(self):
        try:
            for a in range(10):
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                show_more_element = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(Recommendation_for_you.show_more))
                show_more_element.click() #さらに表示クリック
        except TimeoutException:
            print('a')

    def number_of_first_recommendation(self,count): 
        Count = 0
        for c  in range(30): 
            try:
                recommendation_element =  self.browser.find_element_by_xpath('//*[@id="main-content"]/div/div[3]/div[2]/div/div[2]/div[' + str(count+Count) + ']/div/section') 
                print(recommendation_element)
                Count += 1
            except Exception as e:
                break
        return Count

    def find_category(self,count):
        Count = 0
        try: 
            f = self.browser.find_element_by_xpath('//*[@id="main-content"]/div/div[3]/div[2]/div/div[2]/div[' + str(count) + ']/div/div[1]/div[1]')
            Count += 1
        except Exception as e:
            print('start point was not finded') 
        return Count

    def number_of_restaurant(self,xpath):
        element = self.browser.find_elements_by_xpath(xpath)
        number_of_restaurant = len(element)
        return number_of_restaurant

    def get_url(self,url_path):
        url_element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH,url_path)))
        restaurant_url = url_element.find_element_by_tag_name("a").get_attribute("href")
        return restaurant_url 

    def get_name(self,name_path):    
        restaurant_name = self.browser.find_element_by_xpath(name_path).text
        return restaurant_name
    
