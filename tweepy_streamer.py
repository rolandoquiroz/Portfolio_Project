#!/usr/bin/env python3
import json
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class TwitterClient():
    """
    Twitter Client
    """
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
    
    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

class TwitterAuthenticator():
    """
    Twitter Authenticator
    """
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.consumer_key, twitter_credentials.consumer_secret)
        auth.set_access_token(twitter_credentials.access_token, twitter_credentials.access_token_secret)
        return auth

class TwitterStreamer():
    """
    Twitter Streamer
    Class for streaming and processing live tweets
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        """
        This handles Twitter authentication and the connection to the Twitter Streaming API
        """
        """1- We create an object of StdOutListener class"""
        listener = TwitterListener(fetched_tweets_filename)
        """2- Authenticate: Create an object from TwitterAuthenticator and call method"""
        auth = self.twitter_authenticator.authenticate_twitter_app()
        """stream receives auth and listener"""
        stream = Stream(auth, listener)
        """This line filter Twitter Streams to Capture data by the keywords"""
        stream.filter(hash_tag_list)

class TwitterListener(StreamListener):
    """
    Twitter Stream Listener
    This class allow us print the tweets
    This is a basic listener class that just prints received tweets to stdout 
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename=fetched_tweets_filename

    def on_data(self, data):
        """It does somethig you want on_data"""
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print ("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        """What happens on error"""
        if status == 420:
            """Returning False on_data method in case rate limit occurs"""
            return False
        print(status)

class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets
    """
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['retweeted'] = np.array([tweet.retweeted for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        

        return df

if __name__ == "__main__":
    """ hash_tag_list = ["python", "javascript", "java"]
    fetched_tweets_filename = "tweets.json"

    twitter_client = TwitterClient('HolbertonCOL')
    print(twitter_client.get_user_timeline_tweets(1)) """

    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
    
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="delavallevale", count=100)

    """print(dir(tweets[0]))
 
    print(tweets[3].retweet_count)   
    print(tweets[3].favorite_count)  
    print(tweets[1].text)"""  
    df = tweet_analyzer.tweets_to_data_frame(tweets)

    # print(df.head(5))

    """Get average lenght over all tweets"""
    # print(np.mean(df['len']))

    """Get the number of likes for the most liked tweet"""
    print(np.max(df['likes']))

    """Get the number of retweets for the retweeted tweet"""
    print(np.max(df['retweets']))

    """Likes Time Series"""
    """time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    time_likes.plot(figsize=(16, 4), color='r')
    plt.show()"""

    """Retweets Time Series"""
    """time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    time_retweets.plot(figsize=(16, 4), color='b')
    plt.show()"""

    time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    time_likes.plot(figsize=(16, 4), label="likes", legend=True, color='b')
    time_retweets.plot(figsize=(16, 4), label="retweets", legend=True, color='r')

    plt.show(block = False)
    plt.savefig("likes_and_retweets.pdf")
    plt.show()
