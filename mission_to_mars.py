#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
#!pip install pymongo
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # Initialize PyMongo to work with MongoDBs
    # conn = 'mongodb://localhost:27017'
    # client = pymongo.MongoClient(conn)

    # URL of page to be scraped
    url = 'https://redplanetscience.com/'


    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=3)

    response = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response, 'html.parser')
    soup2=soup.select_one('div.list_text')

    news_title = soup2.find('div', class_="content_title").get_text()
    news_p=soup2.find('div', class_="article_teaser_body").get_text()

    # # Featured Image Scraping


    # Featured space image 
    #https://spaceimages-mars.com

    
        
    featured_image_url= "https://spaceimages-mars.com/"
    browser.visit(featured_image_url)
    response = browser.html

    soup = BeautifulSoup(response, 'html.parser') 
    button = soup.find('button', class_='btn btn-outline-light')
    images = soup.find_all('img')
    featured_image=soup.find('img', class_='headerimage fade-in')['src']
   

    #put together final url for featured image only
    photo_url= featured_image_url + featured_image


    # # Mars Facts Scraping


    #use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

    mars_facts_url = "https://galaxyfacts-mars.com"
    tables = pd.read_html(mars_facts_url)
    tables
    df = tables [0]
  
    html_table = df.to_html(classes=["table-bordered", "table-striped", "table-hover"])
    


    # # Mars Hemispheres

    hemispheres_url = "https://marshemispheres.com/"
    browser.visit(hemispheres_url)
    #the webpage contains a list of links that need to be clicked in order to view full image.


    hemisphere_links = {}
    hemisphere_list = []
    click_links = browser.find_by_css('a.product-item img')
    
    for i in range(len(click_links)):
        browser.find_by_css('a.product-item img')[i].click()
        sample = browser.links.find_by_text("Sample").first
        hemisphere_links['img_url'] = sample['href']
        hemisphere_links['img_title'] = browser.find_by_css('h2.title').text
        hemisphere_list.append(hemisphere_links)
        browser.back()


    browser.quit()
    mars_dict = {
        'news_title': news_title, 
        'news_paragraph': news_p,
        'hemisphere_list': hemisphere_list,
        'featured_image': photo_url,
        'fact_table': html_table
    }
    return mars_dict
if __name__ == '__main__':
    scrape()
