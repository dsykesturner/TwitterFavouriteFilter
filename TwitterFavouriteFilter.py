#!/usr/bin/env/ python3

import TwitterAPI as twitter_api
import argparse
from datetime import datetime
from datetime import timedelta


class TwitterFavouriteFilter:

    # Open the key file and authenticate
    def __init__(self):
        self.t_api = twitter_api.TwitterAPI("keys.json")

    def grab_tweets(self, username, days):
        start_date = datetime.now() - timedelta(days=days)
        end_date = datetime.now()
        
        print("Getting all tweets from "+username+" between "+str(start_date)+" and "+str(end_date))
        tweets = self.t_api.download_tweets(username, start_date, end_date)

        return tweets



def get_user_input():
    parser = argparse.ArgumentParser(description='Analyses tweets of a given user and summarises the tweets here')
    parser.add_argument('-i', help='id of the user to analyse. Should start with @', required=True)
    parser.add_argument('-d', help='the number of days back to look for tweets', required=True)

    return parser.parse_args()


# runs only if not imported
if __name__ == '__main__':
    # Get those input argggg
    args = get_user_input()
    tweet_graph = TweetGraph()
    # Get those tweets
    tweet_data = tweet_graph.grab_tweets(args.i, int(args.d))

    # Sort those tweets (by most favourite)
    tweet_data = sorted(tweet_data, key=lambda tweet: tweet.favorite_count, reverse=True)

    # Print the top few or so
    top_few_or_so = 20
    for i in range(len(tweet_data)):
        tweet = tweet_data[i]
        tweet_date = tweet.created_at.strftime("%Y-%m-%d")
        print(str(i+1)+". ❤️  "+str(tweet.favorite_count)+", 🗓  "+tweet_date+": "+tweet.text)

        if top_few_or_so == i+1:
            break
