#Dependency
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from splinter import Browser

#initialyzing the browser
def init_browser():
    #load the chrome driver
    executable_path ={'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

#scraping   
def scrape():

    #Nasa Mars News Site

    browser = init_browser()    
    #Scraping data from the existing NASA Mars News website 
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    #find latest News Title and Paragraph by beautiful soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    content_title = soup.find_all('div', class_='content_title')
    teaser_body = soup.find_all('div', class_='article_teaser_body')

    #list items to store info
    article_header_ls = []
    article_body_ls = []

    #loop through titles
    for title in content_title:
        
        art_title = title.find_all('a')
        
        for art in art_title:
            first_title = art.text.strip()
            article_header_ls.append(first_title)

    #loop through body        
    for body in teaser_body:
        body = body.text.strip()
        article_body_ls.append(body)

    #set header and body 1 variables    
    article_1_header = article_header_ls[0]
    article_1_body = article_body_ls[0]

    #Image Scrape

    #visit the URL for the JPL Featured Space Image by splinter
    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_2)

    html_2 = browser.html
    soup_2 = BeautifulSoup(html_2, 'html.parser')

    images = soup_2.find_all('a', class_='button fancybox')

    #loop through images
    for image in images:
        
        relative_img_path = image["data-fancybox-href"]
        
        base_url = 'https://www.jpl.nasa.gov'
        
        featured_image_url = base_url + relative_img_path

    #Mars Facts Table

    url_3 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_3)
    tables

    df = tables[0]
    df

    html_table = df.to_html()

    #Mars Hemispheres

    #visit the Mars Hemispheres web url
    url_4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_4)
    #HTML object and parser
    html_4 = browser.html
    soup_4 = BeautifulSoup(html_4, 'html.parser')
    
    #find the all item 
    hemisphere_img_urls=[]
    base_url = 'https://astrogeology.usgs.gov'

    items = soup_4.find_all('div', class_='item')
    
    #loop through items
    for item in items:
        title = item.find("h3").text
        h_img_url = item.find("a", class_="itemLink product-item")["href"]
        
        browser.visit(base_url + h_img_url)
        
        image_html = browser.html
        soup_5 = BeautifulSoup(image_html, "html.parser")
        
        full_img_url = base_url + soup_5.find("img", class_="wide-image")["src"]
        
        hemisphere_img_urls.append({"title":title, "img_url":full_img_url})

    #mars data dictionary
    Mars_data = {
        "Mars_News_Title": article_1_header,
        "Mars_News_Paragraph": article_1_body,
        "Mars_Featured_Image": featured_image_url,
        "Mars_Facts": html_table,
        "Mars_Hemisphere_Images": hemisphere_img_urls
    }

    browser.quit()
    
    return Mars_data