import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import os, glob

import ssl;
ssl._create_default_https_context = ssl._create_stdlib_context
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from requests_html import HTMLSession


from pathlib import Path
from time import time
import time


import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin



def findall(p, s):
    '''Yields all the positions of
    the pattern p in the string s.'''
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)


def scrollTillEnd(driver):
        # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(5)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

def findall(p, s):
    '''Yields all the positions of
    the pattern p in the string s.'''
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)

def main():
    authorMetaData()

# Taking each keyword and searching in the page
def authorMetaData():

        csv_input = pd.read_csv('Medium_shortlisted_authors_list.csv')
        print(csv_input.columns)
                
        author_urls = csv_input["author"]
        options = Options()
        # options.headless = True
        options.add_argument('--start-maximized');
        options.add_argument('--start-fullscreen');
    
        # To paas CloudFare security checks : https://stackoverflow.com/questions/50328849/is-there-any-possible-ways-to-bypass-cloudflare-security-checks
        driver = uc.Chrome(options=options)
        # Example URL : ''
        



        for i in range(len(author_urls)):
            
            print(i)
            # page = driver.get(f'{author_urls[i]}')
            
    ###################################################
            ##### Web scrapper for infinite scrolling page #####
            # driver = webdriver.Chrome(executable_path=r"E:\Chromedriver\chromedriver_win32_chrome83\chromedriver.exe")
            driver.get(f'{author_urls[i]}')
            time.sleep(2)  # Allow 2 seconds for the web page to open
            scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
            screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
            i = 1

            while True:
                # scroll one screen height each time
                driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
                i += 1
                time.sleep(scroll_pause_time)
                # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
                scroll_height = driver.execute_script("return document.body.scrollHeight;")  
                # Break the loop when the height we need to scroll to is larger than the total scroll height
                if (screen_height) * i > scroll_height:
                    break 


    ###################################################
            # scrollTillEnd(driver)
            
  
            # soup = BeautifulSoup(driver.page_source, 'html.parser')


            # for x in soup.find_all('article'):
            #     for y in x.find_all('section',attrs={'class':'cw ht hu cr hv'}):
            #         print(y)

            page = driver.page_source

            # Followers
            try:
                print( page[ page.index(">", page.index("Followers")-7 , ) + 1: page.index("Followers") ] )
            except:
                pass

            # Follows
            try:
                print( page[page.index("See all") + 9 : page.index( ")", page.index("See all") , ) ])
            except:
                pass
                    # writing the output html in webpages folder
            
            # Tags
            try:
                tags = [ page[ i + 5: page.find("\"", min(i + 5, len(page)), ) ] for i in findall("\"Tag:", page )]
                print(tags)
            except:
                pass

            # ClapCount
            try:
                claps = [ page[ i + 11: page.find(",", min(i + 11, len(page)), ) ] for i in findall("clapCount\":", page )]
                print(claps)
            except:
                pass
            # print(soup.find_all("button"))

            session = HTMLSession()
            r = session.get(author_urls[i])

            r.html.render(timeout=20)

            with open(f'author_webpages/{i}.html', 'w+', encoding='utf-8') as f:
                f.write(str(driver.page_source))

            divs = r.html.find('div')

            lst = []
            try:
                for div in divs:
                    soup = BeautifulSoup(div.html,'html5lib')
                    div_tag = soup.find()
                    try:
                        title = div_tag.section.div.h1.a.text
                        if title not in lst: 
                            lst.append(title)
                    except:
                        pass

                    # for line in soup:
                    #     if "clapCount:" in line:print(line)
                    
                    # for x in soup.find_all('article'):
                    #     for y in x.find_all('section',attrs={'class':'cw ht hu cr hv'}):
                    #         print(y)
            except:
                pass

            print("\n".join(lst))

        csv_input.to_csv(f'authors_metadata.csv', index=False)


if __name__ == '__main__':
    # freeze_support()
    main()
    
    