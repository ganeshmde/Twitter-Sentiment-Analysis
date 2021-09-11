# -*- coding: utf-8 -*-
"""Twitter Sentiment Analyzer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Q3qmmmXKI-q12fTt2GUqrhJIl6KaPID1
"""

import numpy as np
import pandas as pd
import tweepy
import json
from tweepy import OAuthHandler

consumer_key = "LzsCOl12ZZ79FObx7BV9a1R3a"
consumer_secret = "gODxZ1kHJHDGgYfyP12AUN37UTlDd6yn3OsSV9Tl0iwu0K0cRY"
access_token = "296102538-kYIK8SULCmRK4vgvYD2DhKbwvSXrgTdTkWh0Nvsp"
access_token_secret = "Ib9obwgcE5tZk4S6tY5rAqI5iXOeJc9FGFg28qHoa4YpP"

auth = tweepy.OAuthHandler( consumer_key , consumer_secret )
auth.set_access_token( access_token , access_token_secret )
api = tweepy.API(auth)

query = "RCB winning IPL"

Tweets = api.search( query , count=10 , lang='en' , exclude='retweets' , tweet_mode='extended' )
# tweet_mode='extended'
# tweet_mode='compat'

for tweet in Tweets:
    print(tweet,"\n")
    print(".....................................\n")

df = pd.DataFrame(columns = ['Tweets' , 'User' , 'User_statuses_count' , 
                            'user_followers' , 'User_location' , 'User_verified' ,
                            'fav_count' , 'rt_count' , 'tweet_date'] )
print(df)
# print(df.shape)

def stream(data, file_name):
    i = 0
    for tweet in tweepy.Cursor(api.search, q=data, count=100, lang='en').items():
        print(i, end='\r')
        df.loc[i, 'Tweets'] = tweet.text
        df.loc[i, 'User'] = tweet.user.name
        df.loc[i, 'User_statuses_count'] = tweet.user.statuses_count
        df.loc[i, 'user_followers'] = tweet.user.followers_count
        df.loc[i, 'User_location'] = tweet.user.location
        df.loc[i, 'User_verified'] = tweet.user.verified
        df.loc[i, 'fav_count'] = tweet.favorite_count
        df.loc[i, 'rt_count'] = tweet.retweet_count
        df.loc[i, 'tweet_date'] = tweet.created_at
        df.to_excel('{}.xlsx'.format(file_name))
        i = i+1
        if i == 1000:
            break
        else:
            pass

stream(data=["RCB winning IPL"] , file_name='my_tweets')

df.head()

from textblob import TextBlob

import re
def clean_tweet(tweet):
    return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', tweet).split())

def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

df['clean_tweet'] = df['Tweets'].apply(lambda x : clean_tweet(x))

df.head()

df['Sentiment'] = df['clean_tweet'].apply(lambda x : analyze_sentiment(x) )
df.head()

n = 1
print("Original tweet:\n",df['Tweets'][n])
print()
print("Clean tweet:\n",df['clean_tweet'][n])
print()
print("Sentiment of the tweet:\n",df['Sentiment'][n])

n = 20
print("Original tweet:\n",df['Tweets'][n])
print()
print("Clean tweet:\n",df['clean_tweet'][n])
print()
print("Sentiment of the tweet:\n",df['Sentiment'][n])

n = 203
print("Original tweet:\n",df['Tweets'][n])
print()
print("Clean tweet:\n",df['clean_tweet'][n])
print()
print("Sentiment of the tweet:\n",df['Sentiment'][n])

df[df.Sentiment == 'Positive'].shape[0]

df[df.Sentiment == 'Neutral'].shape[0]

df[df.Sentiment == 'Negative'].shape[0]