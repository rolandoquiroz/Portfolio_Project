#!/usr/bin/env python3

import tweepy
import json
import twitter_credentials


# OAuthHandler object instantiation
auth = tweepy.OAuthHandler(twitter_credentials.consumer_key, twitter_credentials.consumer_secret)
auth.set_access_token(twitter_credentials.access_token, twitter_credentials.access_token_secret)

# class api object instantiation
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# Get my on user info in a objet type user
# my_data = api.me()
# json receives a dictionary or a json
# print (json.dumps(my_data._json, indent=2))
# Get anothr user info
# user_data = api.get_user("_LynaPerez")
# print (json.dumps(user_data._json, indent=2))

# Getting user followers
# data = api.followers(screen_name="__Celeeste")
# Getting user followers using Cursor
# for user in tweepy.Cursor(api.followers, screen_name="__Celeeste").items(100):
#    print (json.dumps(user._json, indent=2))

# Getting user friends using Cursor
# for user in tweepy.Cursor(api.friends, screen_name="andresbarreto").items(100):
#     print (json.dumps(user._json, indent=2))


# Getting a timeline user
for tweet in tweepy.Cursor(api.user_timeline, screen_name="HolbertonCOL", tweet_mode="extended").items(5):
    # print (json.dumps(tweet._json, indent=2))
    print(tweet._json["full_text"])

# for tweet in tweepy.Cursor(api.search, q="estaba mal", tweet_mode="extended").items(5):
    # print (json.dumps(tweet._json, indent=2))
#    print (tweet._json["full_text"])
