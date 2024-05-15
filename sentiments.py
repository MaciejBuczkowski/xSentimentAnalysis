from flask import Blueprint, render_template, request
import matplotlib.pyplot as plt
import os
from twikit import Client
import re
from textblob import TextBlob
import matplotlib


matplotlib.use('agg')

# register this file as a blueprint
second = Blueprint("second", __name__, static_folder="static",
                   template_folder="template")


# render page when url is called
@second.route("/sentiment_analyzer")
def sentiment_analyzer():
    return render_template("sentiment_analyzer.html")


# class with main logic
class SentimentAnalysis:

    def __init__(self):
        self.tweets = []

    # Function connects to twitter by logging into your account and returns searched for tweets
    # Could be biased as uses your personal account which could show more curated posts
    def collectData(self, keyword, num):

        #creating scraper using twikit (tweepy on free api plan no longer works for scraping)
        USERNAME = 'YOUR TWITTER @'
        EMAIL = 'YOUR TWITTER EMAIL'
        PASSWORD = 'YOUR ACCOUNT PASSWORD'

        # Initialize client
        client = Client(language='en-US')

        #TWITTER ACCOUNT IS NECESSARY
        client.login(
            auth_info_1=USERNAME,#Your @
            auth_info_2=EMAIL,#Your email
            password=PASSWORD#Your password
        )

        #To get more accurate query use twitters search page and fill out the filters you want
        #These filters are just put into the search bar along side your keyword
        #This query searches for tweets containing the keyword that are in english and arent replies or contain links
        #Due to limitations of this it can only return a max of 20 tweets in 1 go
        #for unknown reason you need to +2 to the the total number here. Otherwise it gets the wrong amount
        self.tweets = client.search_tweet(f'{keyword} lang:en -filter:links -filter:replies', product='Top',count=int(num)+2)

        # creating some variables to store info
        positive = 0
        negative = 0
        neutral = 0
        avg = []

        # iterating through tweets fetched
        for tweet in self.tweets:

            analysis = TextBlob(self.cleanTweet(tweet.text))

            # adding up polarities to find the average later
            polarity = analysis.sentiment.polarity

            avg.append(polarity)

            # adding reaction of how people are reacting to find average later
            if (polarity == 0.0):
                neutral += 1
            elif (polarity > 0.0 and polarity <= 1.0):
                positive += 1
            elif (polarity < 0.0 and polarity >= -1.0):
                negative += 1

        '''print(positive)
        print(negative)
        print(neutral)
        print(len(self.tweets))'''

        # finding average of how people are reacting
        positive_p = round((positive / len(self.tweets)) * 100,2)
        neutral_p = round((neutral / len(self.tweets)) * 100,2)
        negative_p = round((negative / len(self.tweets)) * 100,2)

        # finding average reaction
        average_pol = sum(avg)/len(avg)

        if (average_pol == 0):
            htmlpolarity = "Neutral"
        # print("Neutral")
        elif (average_pol > 0 and average_pol <= 0.3):
            htmlpolarity = "Weakly Positive"
            # print("Weakly Positive")
        elif (average_pol > 0.3 and average_pol <= 0.6):
            htmlpolarity = "Positive"
        elif (average_pol > 0.6 and average_pol <= 1):
            htmlpolarity = "Strongly Positive"
        elif (average_pol > -0.3 and average_pol <= 0):
            htmlpolarity = "Weakly Negative"
        elif (average_pol > -0.6 and average_pol <= -0.3):
            htmlpolarity = "Negative"
        elif (average_pol > -1 and average_pol <= -0.6):
            htmlpolarity = "strongly Negative"

        self.plotPieChart(positive_p, negative_p, neutral_p)
        print(average_pol, htmlpolarity)
        return average_pol, htmlpolarity, positive_p, negative_p, neutral_p, keyword, num

    def cleanTweet(self, tweet):
        # Remove Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])", " ", tweet).split())


    # function which sets and plots the pie chart. The chart is saved in an img file every time the project is run.
    # The previous image is overwritten. This image is called in the html page.
    def plotPieChart(self, positive, negative, neutral):
        fig = plt.figure()
        labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) +'%]']
        sizes = [positive, neutral, negative]
        colors = ['darkgreen','gold', 'red']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')
        plt.tight_layout()
        strFile = r"static/images/plot1.png"
        if os.path.isfile(strFile):
            os.remove(strFile)  # Opt.: os.system("rm "+strFile)
        plt.savefig(strFile)
        plt.show()


@second.route('/sentiment_logic', methods=['POST', 'GET'])
def sentiment_logic():
    # get user input of keyword to search and number of tweets from html form.
    keyword = request.form.get('keyword')
    tweets = request.form.get('tweets')
    sa = SentimentAnalysis()

    # set variables which can be used in the jinja supported html page
    polarity, htmlpolarity, positive, negative, neutral, keyword1, tweet1 = sa.collectData(keyword, tweets)
    return render_template('sentiment_analyzer.html', polarity=polarity, htmlpolarity=htmlpolarity, positive=positive,
                           negative=negative, neutral=neutral,keyword=keyword1, tweets=tweet1)


@second.route('/visualize')
def visualize():
    return render_template('PieChart.html')