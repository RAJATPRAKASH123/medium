from collections import defaultdict
import csv
from email.policy import default
import pandas as pd
import random
import os, glob
import sys
import csv
from pathlib import Path
from time import time
import time

# import spacy

# nlp = spacy.load('en') 



# increasing csv field size limit
csv.field_size_limit(sys.maxsize)

# Taking each keyword and searching in the page
def convert(value):
    if value:
        # determine multiplier
        multiplier = 1
        if value.endswith('K'):
            multiplier = 1000
            value = value[0:len(value)-1] # strip multiplier character
        elif value.endswith('M'):
            multiplier = 1000000
            value = value[0:len(value)-1] # strip multiplier character

        # convert value to float, multiply, then convert the result to int
        return int(float(value) * multiplier)

    else:
        return 0

# retriving tags and author data
def getTagsAuthors():

    # dictionaries to store tag_response, tag_clap, author_response, author_clap, author_tag_count
    tagResponses = defaultdict(int)
    tagClap = defaultdict(int)
    authorResponses = defaultdict(int)
    authorClap = defaultdict(int)
    authorTagCount = defaultdict(defaultdict)

    # total articles for each keyword extracted
    keywordFile_numRows = defaultdict(int)

    # traversing through files for all the articles for each keyword
    story_urls = set()
    for file in glob.glob("articles_csv/*.csv"):
        
        filename = open(f'{file}', 'r', encoding='utf-8')

        with open(file, 'r') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)

            # extracting field names through first row
            fields = next(csvreader)

            # extracting each data row one by one
            for row in csvreader:
                keywordFile_numRows[filename] += 1
                author = row[2]
                claps = convert(row[5])
                responses = int(row[6].split()[0])
                if row[3] in story_urls:
                    continue
                story_urls.add(row[3])
                for tag in row[8].strip('][').split(', '):
                    
                    if 3 < len(tag) <= 50 and tag[-1] == '\'' and sum([tag.count(i) for i in [" ", "#F", "=", "_", "\"", "--", "}", "{", ",", "png", "jpeg", "gif", "\\", ":", ")", "(", "[", "]"]]) == 0:
                        # if tag[1:-1]
                        tagResponses[tag] += responses
                        tagClap[tag] += claps
                        if tag not in authorTagCount[author]:
                            authorTagCount[author][tag] = 1
                        else:
                            authorTagCount[author][tag] += 1
                    authorResponses[author] += responses
                    authorClap[author] += claps

    # removing the wrong tags : 
    # Whenever I am fetching a tag from html webpage, it is returning their two occurences
    # Observation : wrongly fetched tags have only a single occurance
    # So, I removed them.

# Used to update count of tags, because many times tag counts are repeated for certain authors
    for author, tag_count in authorTagCount.items():
        even_count = len(list(filter(lambda x: (x%2 == 0) , tag_count.values())))
        if even_count == len(tag_count.values()):
            for tag, count in tag_count.items():
                tag_count[tag] = count//2

    # creating file for tag_clap_response
    tag_clap_response = []
    for tag, clap in sorted(tagClap.items(), key = lambda item : 1/ (item[1] + 1)): # sorted by claps
        tag_clap_response.append([tag, clap, tagResponses[tag]])

    df_tag = pd.DataFrame(tag_clap_response)
    df_tag.to_csv('articles_tags.csv', index=False, header=["tag", "claps", "responses"]) 

    # creating file for author_clap_response
    author_clap_response = []
    for author, clap in authorClap.items():
        topTags = [[0, ""], [0, ""], [0, ""]]
        for tag, count in authorTagCount[author].items():
            if count != 1:
                topTags.append([count, tag])
        topTags.sort(key = lambda x : x[0], reverse = True)
        topTagsCount = sum( tag[0] for tag in topTags[:3])
        author_clap_response.append([author, clap, authorResponses[author], authorTagCount[author], topTags[0] if topTags[0][0] != 0 else "", topTags[1] if topTags[1][0] != 0 else "", topTags[2] if topTags[2][0] != 0 else "", sum(authorTagCount[author].values()), topTagsCount  ])

    df = pd.DataFrame(author_clap_response)
    df.to_csv('articles_authors.csv', index=False, header=["author", "claps", "responses", "tag_count", "Popular Tag : 1", "Popular Tag : 2", "Popular Tag : 3", "Total Tags", "Total Top 3 tags"]) 

    print(keywordFile_numRows)

# def groupSimilarTagClapResponse():

#     # creating grouped tags 
#     csv_input = pd.read_csv('articles_tags.csv')



#     similarTagsClaps = defaultdict(int)
#     similarTagsResponses = defaultdict(int)
#     tagsProcessed = set()

#     for tag1 in csv_input['tags']:
#         for tag2 in csv_input['tags']:
#             if tag1 not in tagsProcessed and tag1 != tag2:
#                 tag1_spacy, tag2_spacy = nlp(f'{tag1} {tag2}')
#                 if tag1_spacy.similarity(tag2_spacy) > 0.8:
#                     tagsProcessed.add(tag2)
#                     if similarTagsClaps[tag1] == 0:
#                         similarTagsClaps[tag1] += 

#     csv_input['tags'] =
#     csv_input.to_csv('articles_tags_grouped.csv', index=False)

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
    getTagsAuthors()
    

if __name__ == '__main__':
    # freeze_support()
    main()