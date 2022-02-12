import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import os, glob
import time

import ssl;
ssl._create_default_https_context = ssl._create_stdlib_context
import undetected_chromedriver as uc
from selenium import webdriver
from pathlib import Path

# function to get the whole data of webpage via scrolling the webpage
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
        # updating last_height back to new_height
        last_height = new_height

def main():

    # scraping all articles csv data
    for file in glob.glob("articles_csv/*.csv"):
        
        filename = open(f'{file}', 'r', encoding='utf-8')
        story_urls = []

        # creating the new file name
        newFile = filename.name[filename.name.find("/")+1:filename.name.find(".")]
        print(newFile)

        # If any result already exists, don't try again.
        if Path(f'url_bodytest_csv/{newFile}bodyText.csv').is_file():
            continue

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
        allUrlBodyText = []
        count = len(story_urls)
        print("Total Count : ", count)

        for i in range(count):
            try:
                print(i)
                page = driver.get(f'{story_urls[i]}') # get the page
                scrollTillEnd(driver) # scroll till whole webapage is not loaded
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                # traverse paragraphs from soup
                bodyText = ""
                for data in soup.find_all("p"):
                    bodyText += data.get_text() + "\n" # updating body text
                allUrlBodyText.append([story_urls[i], bodyText])
            except:
                allUrlBodyText.append([story_urls[i], "NA"])
            # print(allUrlBodyText)

        header = ["story_url", "bodyText"] # header for output bodyText csv file
        newFile = filename.name[filename.name.find("/")+1:filename.name.find(".")] # cratubg name of output file
        with open(f'url_bodytest_csv/{newFile}bodyText.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(header)

            # write multiple rows
            writer.writerows(allUrlBodyText)
        print(newFile)
if __name__ == '__main__':
    # freeze_support()
    main()