import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
import re
import csv

# Replace with your own Bearer Token
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAEd11AEAAAAA2FZ5EZj3BtWoX8NQrynrdy4ZhVs%3D1phCdCMztLNYbD7drXWjc7vYzYkUJ2WaVWAZYFQLkf6TaZM2Kb'

class SentimentAnalysis:

    def __init__(self):
        self.client = tweepy.Client(bearer_token=BEARER_TOKEN)
        self.tweets = []
        self.tweetText = []

    def cleanTweet(self, tweet):
        # Remove mentions, special chars, links
        return ' '.join(re.sub(r"(@[A-Za-z0-9_]+)|([^0-9A-Za-z \t])|(http\S+)", " ", tweet).split())

    def percentage(self, part, whole):
        return format(100 * float(part) / float(whole), '.2f')

    def DownloadData(self):
        searchTerm = input("Enter Keyword/Tag to search about: ")
        NoOfTerms = int(input("Enter how many tweets to search (max 100): "))

        query = f"{searchTerm} lang:en -is:retweet"
        response = self.client.search_recent_tweets(query=query, max_results=min(NoOfTerms, 100), tweet_fields=['lang'])

        tweets_data = response.data if response.data else []
        self.tweets = [tweet.text for tweet in tweets_data]

        polarity = 0
        positive = wpositive = spositive = 0
        negative = wnegative = snegative = 0
        neutral = 0

        csvFile = open('result.csv', 'w', newline='', encoding='utf-8')
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(['Tweet', 'Sentiment Polarity'])

        for tweet in self.tweets:
            cleaned_tweet = self.cleanTweet(tweet)
            analysis = TextBlob(cleaned_tweet)
            score = analysis.sentiment.polarity
            polarity += score
            self.tweetText.append(cleaned_tweet)
            csvWriter.writerow([cleaned_tweet, score])

            if score == 0:
                neutral += 1
            elif 0 < score <= 0.3:
                wpositive += 1
            elif 0.3 < score <= 0.6:
                positive += 1
            elif 0.6 < score <= 1:
                spositive += 1
            elif -0.3 < score <= 0:
                wnegative += 1
            elif -0.6 < score <= -0.3:
                negative += 1
            elif -1 <= score <= -0.6:
                snegative += 1

        csvFile.close()

        # Percentages
        positive = self.percentage(positive, NoOfTerms)
        wpositive = self.percentage(wpositive, NoOfTerms)
        spositive = self.percentage(spositive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        wnegative = self.percentage(wnegative, NoOfTerms)
        snegative = self.percentage(snegative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        polarity = polarity / NoOfTerms

        print("\nHow people are reacting on", searchTerm, "by analyzing", NoOfTerms, "tweets.\n")
        print("General Report: ")
        if polarity == 0:
            print("Neutral")
        elif 0 < polarity <= 0.3:
            print("Weakly Positive")
        elif 0.3 < polarity <= 0.6:
            print("Positive")
        elif 0.6 < polarity <= 1:
            print("Strongly Positive")
        elif -0.3 < polarity <= 0:
            print("Weakly Negative")
        elif -0.6 < polarity <= -0.3:
            print("Negative")
        elif -1 <= polarity <= -0.6:
            print("Strongly Negative")

        print("\nDetailed Report:")
        print(f"{spositive}% Strongly Positive")
        print(f"{positive}% Positive")
        print(f"{wpositive}% Weakly Positive")
        print(f"{neutral}% Neutral")
        print(f"{wnegative}% Weakly Negative")
        print(f"{negative}% Negative")
        print(f"{snegative}% Strongly Negative")

        self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = [
            'Strongly Positive [' + str(spositive) + '%]',
            'Positive [' + str(positive) + '%]',
            'Weakly Positive [' + str(wpositive) + '%]',
            'Neutral [' + str(neutral) + '%]',
            'Weakly Negative [' + str(wnegative) + '%]',
            'Negative [' + str(negative) + '%]',
            'Strongly Negative [' + str(snegative) + '%]'
        ]
        sizes = [float(spositive), float(positive), float(wpositive), float(neutral),
                 float(wnegative), float(negative), float(snegative)]
        colors = ['darkgreen', 'green', 'lightgreen', 'gold', 'lightsalmon', 'red', 'darkred']
        patches, texts, autotexts = plt.pie(sizes, colors=colors, startangle=90, autopct='%1.1f%%')
        plt.legend(patches, labels, loc="best")
        plt.title(f"Sentiment Analysis of '{searchTerm}' ({noOfSearchTerms} Tweets)")
        plt.axis('equal')
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()
