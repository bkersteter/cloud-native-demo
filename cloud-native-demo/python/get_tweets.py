# get_tweets.py
#
# Demo python script using the tweepy library to connect to the twitter search
#   API and write the output to a local file.
#
# Built with tweepy 3.6.0
#
#   Bart Kersteter - bkersteter@gmail.com
#
# 03/10/2018    Initial
#

import tweepy
import sys
import os
import jsonpickle

# Twitter Oauth variables -
consumer_key="<ADD_YOUR_CONSUMER_KEY>"
consumer_secret="<ADD_YOUR CONSUMER_SECRET>"
access_token="<ADD_YOUR_ACCESS_TOKEN>"
access_token_secret="<ADD_YOUR_ACCESS_TOKEN_SECRET"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Error handling
if (not api):
    print ("Problem connecting to the Twitter API")

#Getting Geo ID for USA to limt searches to US-based accounts
places = api.geo_search(query="USA", granularity="country")

#Copy USA id
place_id = places[0].id
print('USA id is: ',place_id)
# NOTE:  place_id for US should be 96683cc9126741d1

#Switching to application authentication
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

#Setting up new api wrapper, using authentication only
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

#Error handling
if (not api):
    print ("Problem Connecting to Twitter API using AppAuthHandler")


# Set up the search query we'll use to collect tweets
#searchQuery = 'place:96683cc9126741d1 #vikings OR #minnesotavikings' \
#               'OR #mnvikings OR #skol'
searchQuery = '"Kirk Cousins" OR #vikings OR #minnesotavikings OR #mnvikings OR #skol'
#
#   Set up some variables for the searches
#

print("Current Twitter API Resource Usage")
print api.rate_limit_status()['resources']['search']

#Maximum number of tweets we want to collect
maxTweets = 1000000

#The twitter Search API allows up to 100 tweets per query
tweetsPerQry = 100

tweetCount=0

with open('vikings_tweets.json', 'w') as tweetfile:
    for tweet in tweepy.Cursor(api.search,q=searchQuery).items(maxTweets) :
        #if tweet.place is not None:
            tweetfile.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
            tweetCount += 1

    print("Downloaded {0} tweets".format(tweetCount))





# Count how many tweets were returned
num_tweets=0

# tweepy puts a max of 100 records per api call.  The Twitter API rate limits
#  searches as well, which makes this inefficient for doing mass searches.
#
# A better option to generate a larger result set is to use the twitter
#  streaming api

#public_tweets = api.search(q='#vikings',count=100)
#for tweet in public_tweets:
#    print(tweet.text)
#    num_tweets +=1
#
#print(num_tweets)
