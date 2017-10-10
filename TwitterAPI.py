import tweepy
import json
from datetime import datetime
import pytz 

class TwitterAPI:
    def __init__(self, keys_filename):
        self.api = None
        self.authenticate_api(keys_filename)

    def authenticate_api(self, keys_filename):
        # Open the file containing the API keys and authenticate tweepy
        try:
            with open(keys_filename) as json_data:
                keys = json.load(json_data)
                auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
                auth.set_access_token(keys["access_token"], keys["access_token_secret"])
                self.api = tweepy.API(auth)
        except FileNotFoundError as e:
            # Assume mocked data is going to step in as we have no api now
            print("No auth found!!")
            return

    def download_tweets(self, username, start_date, end_date):
        tweets = []

        # Load in a page of results at a time
        for tweet_page in self.tweepy_timeline(username):
            print("Processing page")
            for tweet in tweet_page:
                # Exit once the tweets have past our start date
                if (tweet.created_at < start_date):
                    return tweets

                # Add this tweet to our list if it's within the date range
                if (tweet.created_at > start_date and tweet.created_at <= end_date):
                    tweets.append(tweet)

        return tweets

    def tweepy_timeline(self, username):
        return tweepy.Cursor(self.api.user_timeline, id=username).pages()

