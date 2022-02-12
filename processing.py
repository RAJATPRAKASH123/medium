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
from pathlib import Path
from time import time
import time

def scrollTillEnd(driver):
        # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

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

    # if Path("allArticles.csv").is_file():
    #     print("File already exists")
    #     return

    # merging the files
    joined_files = os.path.join("articles_csv/", "*.csv")
    
    # A list of all joined files is returned
    joined_list = glob.glob(joined_files)
    print(joined_list)
    # Finally, the files are joined
    df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True)
    df.to_csv("allArticles.csv")
    findTags()

# Taking each keyword and searching in the page
def findTags():

    for file in glob.glob("articles_csv_demo/*.csv"):
        
        filename = open(f'{file}', 'r', encoding='utf-8')
        story_urls = []

        newFile = filename.name[filename.name.find("/")+1:filename.name.find(".")]
        print(newFile)


        with open(file, 'r') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)

            # extracting field names through first row
            fields = next(csvreader)
        
            # extracting each data row one by one
            for row in csvreader:
                story_urls.append(row[3])
                
        story_urls = list(set(story_urls))
        options = webdriver.ChromeOptions() 
        options.headless = True
        options.add_argument('--start-maximized');
        options.add_argument('--start-fullscreen');
        # To paas CloudFare security checks : https://stackoverflow.com/questions/50328849/is-there-any-possible-ways-to-bypass-cloudflare-security-checks
        driver = uc.Chrome(options=options)

        # Example URL : 'https://medium.com/search/posts?q=private%20cloud%2B&count=500'
        articleTags = []
        relatedUrl = []
        count = len(story_urls)
        print("Total Count : ", count)
        for i in range(count):
            try:
                print(i)
                page = driver.get(f'{story_urls[i]}')
                scrollTillEnd(driver)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                # print(driver.page_source)
                try:
                    tags = [ driver.page_source[i+4: driver.page_source.find("\"", i+4, min(i + 200, len(driver.page_source))) ] for i in findall('Tag:', driver.page_source )]
                    articleTags.append(tags)
                    print(tags)
                except:
                    articleTags.append("NA")
                try:
                    urls = [ driver.page_source[i+13: driver.page_source.find("\"", i+13, min(i + 1000, len(driver.page_source))) ] for i in findall("\"mediumUrl\":", driver.page_source )]
                    relatedUrl.append(urls)
                    print(urls)
                except:
                    relatedUrl.append("NA")
            except:
                articleTags.append("NA")
                relatedUrl.append("NA")
            # print(allUrlBodyText)
        # return
        
        newFile = filename.name[filename.name.find("/")+1 :filename.name.find(".")]

        
        csv_input = pd.read_csv(f'articles_csv_demo/{newFile}.csv')
        csv_input['tags'] = articleTags
        csv_input['relatedUrl'] = relatedUrl
        csv_input.to_csv(f'articles_csv_demo/{newFile}.csv', index=False)


if __name__ == '__main__':
    # freeze_support()
    main()
    findTags()
    