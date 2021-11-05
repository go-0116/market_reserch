from selenium.webdriver.support.expected_conditions import number_of_windows_to_be
from pages.home_page import home_page
from pages.restaurant_page import restaurant_page
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import pandas as pd
import json
import requests
from time import sleep

chrome_options = Options()
#chrome_options.add_argument("--headless", )
#chrome_options.add_argument("--no-sandbox")


browser = webdriver.Chrome(options=chrome_options)

def market_reserch(home_url):
    market = home_page(browser)
    market.browser.get(home_url)
    market.show_more()
    count = 1
    count += market.number_of_first_recommendation(count)
    print(count)
    count += market.find_category(count)
    print(count)
    count += market.number_of_first_recommendation(count) #first_recommendationの間にcategoryがあるため二回行っている
    print(count)
    number_of_restaurant = market.number_of_restaurant('//*[@id="main-content"]/div/div[3]/div[2]/div/div[2]/div')
 
    urls = []
    names = []

    
    while count <= number_of_restaurant:
        url_path = '//*[@id="main-content"]/div/div[3]/div[2]/div/div[2]/div[' + str(count) + ']/div'
        name_path = '//*[@id="main-content"]/div/div[3]/div[2]/div/div[2]/div[' + str(count) + ']/div/a/h3' 
        print(market.get_url(url_path))
        print(market.get_name(name_path))
        urls.append(market.get_url(url_path))
        names.append(market.get_name(name_path))
        count += 1
    
    if 'https://www.ubereats.com/jp/taco-bout-awkward' in urls :
        urls.remove('https://www.ubereats.com/jp/taco-bout-awkward')

    df = pd.DataFrame(index=[],columns=[])
    df['URL'] = urls
    df['NAME'] = names

    URL = df['URL'].to_list()
    review_counts = []
    review_rates = []

    hook_url="https://hooks.slack.com/services/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"

    Restaurants = restaurant_page(browser)
    for a in URL:
        Restaurants.browser.get(a)
        sleep(5)
        review_rate, review_count = Restaurants.get_review_rate_and_count()
        
        review_rates.append(review_rate)
        review_counts.append(review_count)

    
    Restaurants.check_percentage_of_0(hook_url, "#fdm-market-research-scraping")

    df['Revie_rate'] = review_rates
    df['Review_count'] = review_counts

    df = Restaurants.remove_chain_store(df)
    return df


df = market_reserch('https://www.ubereats.com/jp/feed?ps=1&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMiVFOSVCOSVCRiVFNSU4NSU5MCVFNSVCMyVCNiVFNSVCOCU4MiUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUpQY1hqQUZKaFBqVVJoVmhjWGEzOTNKbyUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EzMS41OTY4NTM5JTJDJTIybG9uZ2l0dWRlJTIyJTNBMTMwLjU1NzEzOTIlN0Q%3D')


