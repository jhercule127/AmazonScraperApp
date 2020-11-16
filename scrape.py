'''
TODO: Scrape through each of the items whether hourly or in minutes
    Define the logic for looping through this URL will help:
    https://towardsdatascience.com/scraping-multiple-amazon-stores-with-python-5eab811453a8
    Update the lowest price found if another one is found that's lower than the limit
    Update the command line interface for better functionality

    UPDATE:
    Populate with images, pretend to click on zoom and found out how to get images to populate the app
    overall results will have the amount you have left in your budget. 
    Selenium can be used to get images, use Safari Webdriver for now

'''

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import csv
import argparse

'''
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
'''
class Scraper:

    def __init__(self):
        self.limit = 0
        self.products = {}
        self.driver = webdriver.Safari()

    def reset(self):
        self.limit = 0
        self.products = {}

    def get_limit(self):
        return self.limit

    def set_limit(self,x):
        self.limit = x
    

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
                    price = ''
            try:
                review_score = float(soup.select('i[class*="a-icon a-icon-star a-star-5"]')[0].text.split(' ')[0])
                review_count = int(soup.select('#acrCustomerReviewText')[0].text.split(' ')[0].replace(",", ""))
            except:
                try:
                    review_score = float(soup.select('i[class*="a-icon a-icon-star a-star-5"]')[1].text.split(' ')[0])
                    review_count = int(soup.select('#acrCustomerReviewText')[0].text.split(' ')[0].replace(",", ""))
                except:
                    review_score = ''
                    review_count = ''
        
            if self.limit > 0 and price < self.limit:
                self.limit-=price
                self.products[title] = price
                return "The {} is available and is ${}<br>".format(title,price)
            else:
                return '<strong>Oops sorry! </strong> You went over your budget<br>'
        else:
            return "{} is not available. <br>".format(title)


    def get_product_image(self,url):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        product = soup.find(id="imgTagWrapperId")
        return product.img['src']
    

    def overall(self):
        final = "You are able to buy the following items: <br>"
        items = ""
        try:
            for key in self.products.keys():
                items = items + key + "<br>"
        except KeyError:
            pass
        return final + items


    def extract_to_CSV(self):
        results = open("results.csv",'w')
        results_writer = csv.writer(results)
        results_writer.writerow(["Title","Price (US Dollars)"])
        for key,value in self.products.items():
            results_writer.writerow([key,value])
    
    def quit_driver(self):
        self.driver.quit()
