from selenium.webdriver.common.by import By

class Recommendation_for_you(object):
    show_more = (By.XPATH,'//*[@id="main-content"]/div/div/div/div/button')
    top_review_xpath = ['//*[@id="main-content"]/div[3]/div/div[4]/div[3]/div[1]/div[2]/div[2]/div[1]',
    '//*[@id="main-content"]/div[3]/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]',
    '//*[@id="main-content"]/div[3]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div[1]']

    