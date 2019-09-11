#!/usr/bin/env python
# coding: utf-8

# In[12]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
import time


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_scraped_info = {}

    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results_title = soup.find_all('div', class_ ="content_title")[1]
    news_title = results_title.a.text.strip()
    
    results_p = soup.find('div', class_="image_and_description_container")
    news_p = results_p.a.text.strip()

##

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    browser.click_link_by_partial_text('.jpg')

    html1 = browser.html
    soup = BeautifulSoup(html1, 'html.parser')
    
    featured_img_url = soup.find('img').get('src')

##

    url1 = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url1)

    soup = BeautifulSoup(response.text, 'html.parser')
    tweets = soup.find_all('div', class_ ="content")[0]
    
    mars_weather_latest_tweet = tweets.find('p').text

##    
    
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    mars_df = tables[1]
    mars_df = mars_df.rename(columns={0: ' ', 1:' '})
    
    mars_table = mars_df.to_html(index = False)
    mars_table.replace('\n', '')
    
##

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results1 = soup.find_all('div',class_='item')
    hemp_image_urls = []

    for result in results1:
        dict_1 = {}
        title = result.h3.text.strip() 
        title = title.replace('Enhanced',' ')
    
        browser.click_link_by_partial_text('Hemisphere Enhanced')
        url = browser.find_by_text('Sample')['href'] 

        dict_1['title'] = title
        dict_1['url'] = url
        hemp_image_urls.append(dict_1)


##  
    mars_scraped_info['title'] = news_title
    mars_scraped_info['paragraph'] = news_p
    mars_scraped_info['image'] = featured_img_url
    mars_scraped_info['weather'] = mars_weather_latest_tweet
    mars_scraped_info['facts'] = mars_table
    mars_scraped_info['Hemis'] = hemp_image_urls

    browser.quit()
    
    return mars_scraped_info


