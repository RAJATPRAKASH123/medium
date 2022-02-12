from collections import defaultdict
import matplotlib.pyplot as plt  # used for plotting
import seaborn as sns
from datetime import datetime
import pandas as pd
# import plotly.express as px
# from plotly.subplots import make_subplots
# import plotly.graph_objects as go


from matplotlib import pyplot as plt
# read tag and dates data

def plotTagMonthly():
    csv_input = pd.read_csv('allArticles.csv')
    print(csv_input.columns)
    tag_date = defaultdict(list)

    # creating a dictionary with {tag : [list of dates]}
    for date, tagList in zip(csv_input["date"], csv_input["tags"]):
        try:
            for tag in tagList.strip('][').split(', '):
                tag_date[tag].append(date)
        except:
            pass

    tag_occurance_list = []
    for tag, dates in tag_date.items():
        if len(tag) > 2:
            tag_occurance_list.append([tag, len(dates)])

    tag_occurance_list.sort(key = lambda x : x[1], reverse = True)

    # find count of top 10 tags for 
    tagDateList = [[tag, tag_date[tag]] for tag, count in tag_occurance_list[:15]]

    for tag, dateList in tagDateList:
        # print(tag, dateList)
        month_count = defaultdict(int)
        year = "2021"
        for date in dateList:
            if year in date: 
                month = date[date.index(">") + 1: date.index(" ", date.index(">"), )]
                month_count[month] += 1
        monthList = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        countList = [month_count[month] for month in monthList]
        # Creating histogram
        print(tag)
        plt.title(tag + " in : " + year)
        plt.bar(monthList, countList)
        # Show plot
        plt.xlabel('Month')
        plt.ylabel(f'Article Count with tag : {tag}')
        plt.savefig(f'plots/{tag}.png')
        plt.show()



if __name__ == '__main__':
    plotTagMonthly()