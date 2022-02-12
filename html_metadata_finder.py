from bs4 import BeautifulSoup
import pandas as pd
import os, glob
import csv
def main():
    # open all the webpages
    for file in glob.glob("webpages/*.html"):
        file = open(f'{file}', 'r', encoding='utf-8')
        soup = BeautifulSoup(file, 'html.parser')
        stories = soup.select('.js-block')
        # print(stories)
        # titles = soup.select(".graf--title")
        # print(titles)
        articles = []

        for story in stories:
            each_story = []
            date = story.select("time")
            author_box = story.find('div', class_='postMetaInline u-floatLeft u-sm-maxWidthFullWidth')
            author_url = author_box.find('a')['href']
            reading_time = "na"
            try:
                reading_time = author_box.find('span', class_='readingTime')['title']
            except:
                continue

            title = story.find('h3').text if story.find('h3') else '-'
            subtitle = story.find('h4').text if story.find('h4') else '-'

            if story.find('button', class_='button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents'):

                claps = story.find('button', class_='button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents').text
            
            else:
                claps = 0

            if story.find('a', class_='button button--chromeless u-baseColor--buttonNormal'):
                
                responses = story.find('a', class_='button button--chromeless u-baseColor--buttonNormal').text
            
            else:
                responses = '0 responses'

            story_url = story.find('a', class_='button button--smaller button--chromeless u-baseColor--buttonNormal')['href']
            articles.append([title, subtitle, author_url, story_url, date, claps, responses, reading_time])
        # print(file, articles[0])
        newFile = file.name[file.name.find("/")+1:file.name.find(".")]
        print(newFile)
        header = ["title", "subtitle", "author_url", "story_url", "date", "claps", "responses", "reading_time"]
        with open(f'articles_csv/{newFile}.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(header)

            # write multiple rows
            writer.writerows(articles)
if __name__ == '__main__':
    # freeze_support()
    main()