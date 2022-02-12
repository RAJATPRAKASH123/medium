import pandas as pd
from math import sqrt

def calculateAuthorClapResponseGM():
    csv_input = pd.read_csv(f'articles_authors.csv')

    claps = [ 1 if clap == 0 else clap for clap in csv_input['claps']]
    responses = [ 1 if response == 0 else response for response in csv_input['responses']]

    clap_response_gm = []
    for clap, response in zip(claps, responses):
        clap_response_gm.append( sqrt(clap * response ) )

    csv_input['claps'] = claps
    csv_input['responses'] = responses
    csv_input['clap_response_GM'] = clap_response_gm

    csv_input.to_csv(f'articles_authors_gm.csv', index=False)

def removeNotInterestedTags():
    csv_input = pd.read_csv(f'articles_tags.csv')
    csv_not_interested = pd.read_csv(f'Medium_articles_tags - articles_tags.csv')

    nonInterestTags = set()
    temp = 0
    for tag, status in zip(csv_not_interested['tag'], csv_not_interested['status'] ):
        if status == 'n':
            nonInterestTags.add("'" + str(tag))
    print(nonInterestTags)
      

    deleteTags = []     
    count = 0
    for tag in csv_input['tag']:
        if tag in nonInterestTags:
            print(tag)
            deleteTags.append(count)
        count += 1
    csv_input.drop(csv_input.index[deleteTags] , inplace=True)

    print(deleteTags)
    csv_input.to_csv(f'articles_tags_interested.csv', index=False)


if __name__ == '__main__':
    calculateAuthorClapResponseGM()
    removeNotInterestedTags()
    # pass