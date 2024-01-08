'''Twitter API connector'''

import os

import tweepy
import streamlit as st

# Assign credentials from env variable or streamlit secrets dict
consumer_key = os.getenv('TWITTER_CONSUMER_KEY') or st.secrets['TWITTER_CONSUMER_KEY']
consumer_secret = (
    os.getenv('TWITTER_CONSUMER_SECRET') or st.secrets['TWITTER_CONSUMER_SECRET']
)
access_key = os.getenv('TWITTER_ACCESS_KEY') or st.secrets['TWITTER_ACCESS_KEY']
access_secret = (
    os.getenv('TWITTER_ACCESS_SECRET') or st.secrets['TWITTER_ACCESS_SECRET']
)


class Tweets:
    '''Twitter API connector'''

    def __init__(self, account):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth)
        self.account = account

    def fetch_tweets(self) -> list:
        '''Fetch tweets from account'''
        try:
            tweets = self.api.user_timeline(
                screen_name=self.account,
                tweet_mode='extended',
                count=50,
                exclude_replies=True,
                include_rts=False,
            )
            return [tweet.full_text for tweet in tweets][:10]
        except tweepy.errors.NotFound:
            st.error('Twitter account not found')
        except tweepy.errors.Unauthorized:
            st.error('Twitter account is private')
        return []