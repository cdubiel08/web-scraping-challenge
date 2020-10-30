from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd


return_dict = {}

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser = init_browser()
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    results = soup.find_all("li", class_="slide")

    #extract text from div tags from most recent news slide
    news_title = results[0].find('div', class_='content_title').a.get_text()
    news_p = results[0].find('div', class_='article_teaser_body').get_text()

    return_dict["news_title"] = news_title
    return_dict["news_p"] = news_p


    #Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser = init_browser()
    browser.visit(url)
    # browser.click_link_by_partial_text("FULL IMAGE")
    html = browser.html
    soup = bs(html, "html.parser")
    results = soup.find_all("article")
    url_end = results[0]['style'][24:-3]
    base_url = 'https://www.jpl.nasa.gov/'
    featured_image_url = f"{base_url}{url_end}"

    return_dict["featured_image_url"] = featured_image_url


    #scrape html table using pandas
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[2]
    html_table = df.to_html() 

    return_dict["html_table"] = html_table

    #scrape for hq imgs of hemispheres of Mars and add to dictionary
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    list_of_hemis = ['Cerberus Hemisphere', 'Valles Marineris Hemisphere', 'Schiaparelli Hemisphere', 'Syrtis Major Hemisphere']
    browser = init_browser()
    results = {}
    base_url = 'https://astrogeology.usgs.gov'

    for hemi in list_of_hemis:
        browser.visit(url)
        browser.click_link_by_partial_text(hemi)
        html = browser.html
        soup = bs(html, "html.parser")
        end = soup.find_all("img", class_ = "wide-image")[0]['src']
        img_url = base_url + end
        results[hemi.replace(" ", "_")] = img_url
    
    return_dict["hemi_imgs"] = results
    
    return return_dict
