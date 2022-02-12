# ssl, selenium, Beautiful Soup and undetected_chromedriver used 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

import ssl; 
ssl._create_default_https_context = ssl._create_stdlib_context
import undetected_chromedriver as uc
from selenium import webdriver

# keywords used to extract articles
keywords = ["cloud computing", "cloud" ,"aws", "azure", "google cloud", "public cloud", "private cloud", "saas", "paas", "iaas", "external cloud", "Google Cloud Platform", "cloud native", "cloud storage","cloud services"]

# Taking each keyword and searching in the page
def main():
    options = webdriver.ChromeOptions() 
    options.headless = True
    options.add_argument('--start-maximized');
    options.add_argument('--start-fullscreen');
    # To paas CloudFare security checks : https://stackoverflow.com/questions/50328849/is-there-any-possible-ways-to-bypass-cloudflare-security-checks
    driver = uc.Chrome(options=options)
    # Enter a keyword, Example : aws, google cloud, internal cloud etc
    for keyword in keywords:
        # Use this to get better results individually

        # keyword = input().split() 
        keyword = keyword.split()
        articleCount = 400
        print("Webpage saved for : ",keyword)
        searchSubUrl = "" # Part of URL which will get updated on each input
        for i, cur in enumerate(keyword):
            if i != 0:
                searchSubUrl += "%20"
            searchSubUrl += cur

        # Example URL : 'https://medium.com/search/posts?q=private%20cloud%2B&count=500'
        
        page = driver.get(f'https://medium.com/search/posts?q={searchSubUrl}%2B&count={articleCount}')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # writing the output html in webpages folder
        with open(f'webpages/{"".join(keyword)}.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))
        

if __name__ == '__main__':
    # freeze_support()
    main()
