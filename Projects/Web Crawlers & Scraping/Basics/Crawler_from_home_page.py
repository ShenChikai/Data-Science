# -*- coding: utf-8 -*-
"""
Created on Tue May 10 18:26:31 2022

@author: shenc
"""

# Import library
import requests
import queue
from pathlib import Path
from bs4 import BeautifulSoup
import numpy as py
import pandas as pd

def crawl_home(home_url, start_anchor):
    search_anchors = queue.Queue()
    results =[]
    iter_count = 0
    max_iter = 10000
    
    while True:
        if not start_anchor:
            # empty start_anchor
            start_anchor = '/'
        
        # GET response with requests
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
        response = requests.request('GET', home_url + start_anchor, headers=headers)
        
        # Create Soup
        soup = BeautifulSoup(response.text, 'lxml')
        #print(soup.prettify())
        
        # Find anchors (links) with the customized function
        anchors = find_local_anchors(soup, start_anchor)
        
        if anchors:
            # Not empty
            for a in anchors:
                # Construct the anchor
                target_url = home_url + a
                if target_url in results:
                    # exists?
                    continue
                if not Path(a).suffix:
                    # pdf, png, etc.?
                    search_anchors.put(a)
                # Append to results
                results.append(a)
        
        # Done if nothing to search
        # Go on if queue has smth
        if search_anchors.empty():
            break
        start_anchor = search_anchors.get()
        
        print('... ', sep='',end='')
        
        # Max iteraions break condition
        iter_count += 1
        if iter_count == max_iter:
            break
        
    return results

def find_local_anchors(soup, start_anchor):
    anchors = []
    
    for link in soup.find_all('a'):
        # Get link in href
        if 'href' in link.attrs:
            anchor = link.attrs['href']
        else:
            anchor = ''
        #print(anchor, start_anchor)
        
        # if it is in the direction of the start_anchor
        if anchor.startswith(start_anchor):
            anchors.append(anchor)

    return anchors

# Execute
home_url = 'https://overthewire.org/wargames/'
start_anchor = '/'

results = crawl_home(home_url, start_anchor)
print(len(results),'\n',results)