# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import requests

def scrape():
    #Setting up Splinter
    executable_path = {'executable_path' : ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Url Setup
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html

    soup = bs(html, 'html.parser')

    post_title = soup.find_all('div', class_ = "content_title")[0].text

    post_paragraph = soup.find_all('div', class_="article_teaser_body")[0].text

    # Exit Browser
    browser.quit()

    # ----------------------------------------------------------------------------------------------------------------------------------- #

    ## Image site scrapping ##
    image_url = 'https://spaceimages-mars.com/'

    browser.visit(image_url)

    image_html = browser.html

    image_soup = bs(image_html, 'html.parser')

    image = image_soup.find_all('a', class_="fancybox-thumbs")[0]

    image_full_link = image_url + image["href"]

    # Exit Browser
    browser.quit()

    # ----------------------------------------------------------------------------------------------------------------------------------- #

    ## Mars Facts ##

    facts_url = 'https://galaxyfacts-mars.com'

    tables = pd.read_html(facts_url)

    mars_facts_info = tables[1]

    mars_facts_comparison = tables[0]

    mars_facts_info.columns = ['Measurement', 'Value']

    # mars_facts_info = mars_facts_info.reset_index(drop=True)

    mars_facts_comparison.columns = ['Description', 'Mars', 'Earth']

    # Exit Browser
    browser.quit()

    # ----------------------------------------------------------------------------------------------------------------------------------- #

    ## Mars Hemispheres ## 

    mars_hemispheres_url = 'https://marshemispheres.com/'

    browser.visit(mars_hemispheres_url)

    mars_hemispheres_html = browser.html

    mars_hemispheres_soup = bs(mars_hemispheres_html, 'html.parser')

    mars_hemisphere_details = []

    x = mars_hemispheres_soup.find_all('div', class_='description')

    # print(x)

    for i in range(len(x)):
        m_h_image_title = x[i].h3.text    
        # print(m_h_image_title)
        
        m_h_image_description = x[i].p.text  
        # print(m_h_image_description)
        
        m_h_image_url = mars_hemispheres_url + x[i].a['href']
        # print(m_h_image_url)
        
        browser.visit(m_h_image_url)
        
        image_url_html = browser.html
            
        image_url_soup = bs(image_url_html, 'html.parser')
        
        hemisphere_img_url = mars_hemispheres_url + image_url_soup.find_all('img')[4]['src']
        # print(hemisphere_img_url)
        
        mars_hemisphere_details.append({'title': m_h_image_title, 'image_link': hemisphere_img_url})
        
    mars_hemisphere_details

    # Exit Browser
    browser.quit()

    # ----------------------------------------------------------------------------------------------------------------------------------- #

    # Storing scraped data #
    missions_to_mars = {
        "title": post_title,
        "description": post_paragraph,
        "image_link": image_full_link,
        "mars_info": mars_facts_info,
        "mars_comparison": mars_facts_comparison,
        "hemisphere": mars_hemisphere_details
    }

    # Return results
    return missions_to_mars
