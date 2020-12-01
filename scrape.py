'''
TODO: Scrape through each of the items whether hourly or in minutes
    Define the logic for looping through this URL will help:
    https://towardsdatascience.com/scraping-multiple-amazon-stores-with-python-5eab811453a8
    Update the lowest price found if another one is found that's lower than the limit
    Update the command line interface for better functionality

    UPDATE:
    Populate with images, pretend to click on zoom and found out how to get images to populate the app
    overall results will have the amount you have left in your budget. 

    Use these resources: https://stackoverflow.com/questions/54868328/html-how-to-automatically-create-bootstrap-cards-from-a-js-file
    https://getbootstrap.com/docs/4.0/components/card/
    
    Fix when trying to get products again

    Fix error handling and some things in javascript
       - a bit more of error handling

    Fix buttons
        Form button works correctly
        Reset too, but change how to select
    Change how to select stuff using query selector or whatever is appropiate



'''

from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlparse
import requests
import csv
import argparse
import io

'''
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
'''
class Scraper:

    def __init__(self):
        self.limit = 0
        self.products = {}
        self.driver = None

    def reset(self):
        self.limit = 0
        self.products = {}
        if self.limit or self.products:
            return False
        else:
            return True

    def get_limit(self):
        return self.limit

    def get_products(self):
        return self.products

    def set_limit(self,x):
        self.limit = x
    
    def set_driver(self):
        self.driver = webdriver.Safari()

    def is_valid(self,url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme) and ('www.amazon.com' == parsed.netloc)


    def get_purchase_outcome(self,url):
        #response = requests.get(url,headers=HEADERS)
        
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        
        try:
            soup.select('#availability .a-color-state')[0].text.strip()
            available = 0
        except:
            # checking if there is "Out of stock" on a second possible position
            try:
                soup.select('#availability .a-color-price')[0].text.strip()
                available = 0
            except:
                available = 1
        title = soup.find('span',id='productTitle').text.strip()

        if available:
            
            try:
                price = float(soup.find(id='priceblock_ourprice').text.replace('$','').replace(',','').strip())
            
            except:
                try:
                    price = float(soup.find(id='priceblock_saleprice').text.replace('$','').replace(',','').strip())
                except:
                    return "Could not extract the price for {}".format(title)

            try:
                review_score = float(soup.select('span[class*="a-size-medium a-color-base"]')[0].text.split(' ')[0])
            except:
                try:
                    review_score = float(soup.select('i[class*="a-icon a-icon-star a-star-5"]')[1].text.split(' ')[0])
                except:
                    review_score = ''


            if self.limit > 0 and price < self.limit:
                image = self.get_product_image()
                self.limit-=price
                self.products[title] = [price,image,url,review_score]
                return "The {} is available and is ${}<br>".format(title,price)
            else:
                return '<strong>Oops sorry! </strong> You went over your budget<br>'
        else:
            return "{} is not available. <br>".format(title)



    def get_product_image(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        product = soup.find(id="imgTagWrapperId")
        return product.img['src']
    

    def get_product_names(self):
        items = ""
        try:
            for key in self.products.keys():
                items = items + key + "<br>"
        except KeyError:
            pass
        return items



    def extract_to_CSV(self):
        si = io.StringIO()
        results_writer = csv.writer(si)
        results_writer.writerow(["Title","Price (US Dollars)"])
        for key,value in self.products.items():
            results_writer.writerow([key,value[0]])
        return si



    def quit_driver(self):
        self.driver.quit()
        
