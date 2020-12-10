#Dependency
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver

#initialyzing the browser
def init_browser():
    #load the crome driver
    executable_path ={'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

#scraping   
def scrape():
    browser = init_browser()    
    #Scraping data from the existing NASA Mars News website 
    url =  "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(url)
    soup = bs(response.text,"html.parser")

    #find latest News Title and Paragraph by beautiful soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    content_title = soup.find_all('div', class_='content_title')
    teaser_body = soup.find_all('div', class_='article_teaser_body')

    article_header_ls = []
    article_body_ls = []

    for title in content_title:
        
        art_title = title.find_all('a')
        
        for art in art_title:
            first_title = art.text.strip()
            article_header_ls.append(first_title)
            
    for body in teaser_body:
        body = body.text.strip()
        article_body_ls.append(body)
        
    article_1_header = article_header_ls[0]
    article_1_body = article_body_ls[0]

    print(article_1_header)
    print(article_1_body)

    #visit the URL for the JPL Featured Space Image by splinter
    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_2)

    html_2 = browser.html
    soup_2 = BeautifulSoup(html_2, 'html.parser')

    images = soup_2.find_all('a', class_='button fancybox')

    for image in images:
        
        relative_img_path = image["data-fancybox-href"]
        
        base_url = 'https://www.jpl.nasa.gov'
        
        featured_image_url = base_url + relative_img_path

    print(featured_image_url)

    #main existing url
    main_url = "https://www.jpl.nasa.gov"

    url_3 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_3)
    tables

    df = tables[0]
    df

    html_table = df.to_html()
    html_table

    #visit the Mars Hemispheres web url
    Mars_Hem="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(Mars_Hem)
    #HTML object and parser
    html_Hem = browser.html
    soup = bs(html_Hem, "html.parser")
    #find the all item 
    Mars_Hem_item=soup.find_all("div", class_="item")
    #declare a list of Hamisphere url list
    Hem_image_url=[]
    # bring the main url 
    Hem_main_url = "https://astrogeology.usgs.gov"
    #use for loop to containg the image link
    for item in Mars_Hem_item:
        #to get the title
        title=item.find("h3").text
        #to get the partial image url
        partial_image_url=item.find("a", class_="itemLink product-item")["href"]
        #visit the both url
        browser.visit(Hem_main_url + partial_image_url)
        #HTML object and parser
        partial_image_html=browser.html
        soup=bs(partial_image_html, "html.parser")
        # to get the  full image url 
        full_image_url = Hem_main_url + soup.find("img", class_="wide-image")["src"]
        #put the data in the list
        Hem_image_url.append({"title":title, "img_url" : full_image_url })

    Mars_Hemispheres_data= {
        "Mars_News_Title": news_title,
        "Mars_News_Paragraph": news_p,
        "Mars_Featured_Image": featured_image_url,
        "Mars_Facts": Mars_Facts_htmldata,
        "Mars_Hemisphere_Images": Hem_image_url
    }
    browser.quit()
    
    return Mars_Hemispheres_data