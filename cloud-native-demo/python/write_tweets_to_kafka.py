# write_tweets_to_kafka.py
#
# Demo python script using the tweepy library to connect to the twitter search
#   API and write the output to a local kafka instance.
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
import json
from kafka import KafkaProducer, KafkaClient
###############################################################################
#  Set up Twitter Connections
###############################################################################

# Twitter Oauth variables
consumer_key="<ADD_YOUR_CONSUMER_KEY>"
consumer_secret="<ADD_YOUR_CONSUMER_SECRET>"
access_token="<ADD_YOUR_ACCESS_TOKEN>"
access_token_secret="<ADD_YOUR_ACCESS_TOKEN_SECRET>"

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
################################################################################

################################################################################
#Create new producer & use default location of localhost:9092
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
################################################################################

tweetCount=0

# using three semicolons as field separators to try and work around random
#  garbarge in Twitter user profiles and/or tweet bodies
for i in tweepy.Cursor(api.search,q=searchQuery).items(maxTweets) :
        record = ''
        record += str(i.user.id_str)
        record += ';;;'
        record += str(i.created_at)
        record += ';;;'
        record += str(i.user.followers_count)
        record += ';;;'
        record += str(i.user.location.encode("ascii","ignore"))
        record += ';;;'
        record += str(i.favorite_count)
        record += ';;;'
        record += str(i.retweet_count)
        record += ';;;'
        record += str(i.text.encode("ascii","ignore"))
        record += ';;;'
        producer.send('tweets', record.encode("ascii","ignore"))
        producer.flush()
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
