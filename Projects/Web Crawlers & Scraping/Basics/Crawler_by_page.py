# -*- coding: utf-8 -*-
"""
Created on Mon May  9 22:11:50 2022

@author: shenc
"""

# Import library
import requests
from bs4 import BeautifulSoup
import numpy as py
import pandas as pd

brands = []
products = []
prices = []

def job_spider(max_pages):
    
    page = 1
    
    while page <= max_pages:
        
        # Forge URL
        url='https://www.ssense.com/en-us/women?sort=popularity-desc&page=' + str(page)
        print('Accessing:\n', url)
        
        # Get source code (user agent header to avoid being detected as non-human)
        # Generate random user agent: https://generate-name.net/user-agent
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
        response = requests.get(url, headers=headers)
        
        # Get plain text
        plain_text = response.text
        
        # Create soup obj
        soup = BeautifulSoup(plain_text, features='lxml')
        print(soup.prettify())
        print('start crawling...')
        
        # Crawl
        for description in soup.findAll('div', {'class': 'product-tile__description'}):
            brand = description.contents[0].span.text[1:-2]
            product = description.contents[2].span.text[1:-2]
            price = description.contents[4].span.text[1:-2]
            print(f'brand: {brand}, product: {product}, price: {price}')
            brands.append(brand)
            products.append(product)
            prices.append(price)
        # Increment page number
        page += 1
    
            

job_spider(10)

#brands = np.array(brands)
#products = np.array(products)
#prices = np.array(products)

output_df = pd.DataFrame({'brand': brands, 'product': products, 'price': prices})
output_df.to_csv('SSENSE_latest_trend_women.csv')









