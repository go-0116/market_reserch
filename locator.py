from selenium.webdriver.common.by import By

class Recommendation_for_you(object):
    show_more = (By.XPATH,'//*[@id="main-content"]/div/div/div/div/button')
    reviewrate_normal = (By.XPATH,'//*[@id="main-content"]/div[3]/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/div[3]')
    reviewcounts_noraml = (By.XPATH,'//*[@id="main-content"]/div[3]/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/div[5]')
    reviewrate_delivery_fee = (By.XPATH,'//*[@id="main-content"]/div[3]/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/div[7]')
    reviewcounts_delivery_fee = (By.XPATH,'//*[@id="main-content"]/div[3]/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/div[9]')

    