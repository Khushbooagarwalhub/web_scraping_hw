# Import BeautifulSoup and other requirements
import requests
import bs4 
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape ():
    
    
    browser = init_browser()
    mission_mars_dictionary = {}
    
    # Visit the following URL
    url_news = "https://mars.nasa.gov/news/"
    browser.visit(url_news)
    time.sleep(1)
    ## Create a Beautiful Soup object
    html = browser.html
    soup = bs(html, 'html.parser')
    #chceck if the url is connected 
    soup.title
    #check the item lists
    news_list = soup.find('ul', class_='item_list')
    #find the latest news title
    title_latestnews = soup.find('div', class_='content_title').text
    
    #find the latest news paragraph
    latest_paragraph = soup.find('div',class_='article_teaser_body').text
    
    ## Visit the following URL
    url_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_images)
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')
    time.sleep(1)
    #create a beautiful soup object
    html = browser.html
    image_soup = bs(html, 'html.parser')
    #extract the url for images 
    my_imgs =image_soup.findAll('figure',{'class':'lede'})
    for img_link in my_imgs:
            print(img_link.img['src'])
            img_path = img_link.img['src']
    
    #get the final url for image
    final_image_path =f'https://www.jpl.nasa.gov{img_path}'
    
    #visit the following url
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)
    #create a beautiful soup object
    html = browser.html
    soup_tweeting = bs(html, 'html.parser')
    #find the latest tweet on weather
    first_tweet = soup_tweeting.find('p', class_='TweetTextSize').text
    
    #visit the website 
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(1)
    #extract the html file using pandas
    mars_data_facts = pd.read_html(url)
    
    #convert the data to dataframe and change it to html file for the required data
    #mars_data_facts = mars_data_facts[0]
    #mars_data_facts
    mars_data_fact_df = pd.DataFrame(mars_data_facts[0])
    mars_data_html = mars_data_fact_df.to_html()
    
    
    #visit the following link
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    time.sleep(1)
    #create a beautiful soup object
    html_hem = browser.html
    soup_hemisphere1 = bs(html_hem, 'html.parser')
    #check if the url is working
    soup_hemisphere1.title

    #Extract the required url using loops
    #create an empty list to store the output
    hemisphere = []
    #store the main url 
    main_url = 'https://astrogeology.usgs.gov'

    # Retreive all items that contain  hemispheres facts
    items = soup_hemisphere1.find_all('div', class_='item')
    #run a for loop over each item to get the final url
    for item in items:
           each_title = item.find('h3').text
           #title.append(each_title)
           each_url = item.find('a')['href']
           final_url = main_url + each_url 
           browser.visit(final_url)
           html_links = browser.html
           soup_hem_links = bs(html_links, 'html.parser')
           hemisphere_images = soup_hem_links.find('img', class_='wide-image')['src']
           hemisphere_url = main_url + hemisphere_images
           hemisphere.append({"title": each_title, "img_url": hemisphere_url})


    mission_mars_dictionary = {
        "title_latestnews": title_latestnews,
        "latest_paragraph": latest_paragraph,
        "final_image_path": final_image_path,
        "weather": first_tweet,
        "facts": mars_data_html,
        "hemispheres": hemisphere
    }
    
    
    browser.quit()

    return mission_mars_dictionary







    

    
    
    
    
