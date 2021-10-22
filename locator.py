from selenium.webdriver.common.by import By

class Recommendation_for_you(object):
    show_more = (By.XPATH,'//*[@id="main-content"]/div/div/div/div/button')
    reviewrate_normal = (By.XPATH,'//*[@id="main-content"]/div[3]/div/div[4]/div[3]/div[1]/div[2]/div[2]/div[1]/div[3]')
    reviewcounts_noraml = (By.XPATH,')//*[@id="main-content"]/div[3]/div/div[4]/div[3]/div[1]/div[2]/div[2]/div[1]/div[5]')
    reviewrate_delivery_fee = (By.XPATH,'//*[@id="main-content"]/div[3]/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/div[7]')
    reviewcounts_delivery_fee = (By.XPATH,'//*[@id="main-content"]/div[3]/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/div[9]')
    reviewrate_km = (By.XPATH,'//*[@id="main-content"]/div[3]/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/div[5]')
    reviewcounts_km = (By.XPATH,'//*[@id="main-content"]/div[3]/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/div[7]')

#//*[@id="main-content"]/div[3]/div/div[4]/div[3]/div[1]/div[2]/div[2]/div[1]/div[1]
#//*[@id="main-content"]/div[3]/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/div[7]
#//*[@id="main-content"]/div[3]/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/div[7]
#//*[@id="main-content"]/div[3]/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/div[9]
#//*[@id="main-content"]/div[3]/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/div[7]
#//*[@id="main-content"]/div[3]/div/div[4]/div[3]/div[1]/div[2]/div[2]/div[1]/div[3]
#//*[@id="main-content"]/div[3]/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/div[5]
#//*[@id="main-content"]/div[3]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div[1]/div[7]
#//*[@id="main-content"]/div[3]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div[1]/div[9]
#//*[@id="main-content"]/div[3]/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/div[9]
#main-content > div:nth-child(4) > div > div.ez.ah.ai.f0.ag > div.f3.f4.ah.dy > div:nth-child(1) > div.ah.e1.f6.dm.b0.f7 > div:nth-child(2) > div.ce.cz.cg.e9.f9.ah.c3 > div:nth-child(9)
#//*[@id="main-content"]/div[3]/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/div
#//*[@id="main-content"]/div[3]/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[1]/div[3]
#//*[@id="main-content"]/div[3]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div[1]/div[5]