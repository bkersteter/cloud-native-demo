# tweet_loader.py
#
#       Demo python scipt to read tweets from Kafka and load them
#       into a local Postgres database
#
#
#   Bart Kersteter - bkersteter@gmail.com
#
# 03/11/2018    Initial
#

from kafka import KafkaConsumer, KafkaClient
import psycopg2
import json
from io import StringIO

###############################################################################
#   Set up Postgres Connection - Assumes localhost & default port
###############################################################################
conn = psycopg2.connect("dbname=bjk user=bjk")

# Test Connection to make sure everything works
#cur = conn.cursor()
#cur.execute("CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, num integer, data varchar);")
#cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))
#cur.execute("SELECT * FROM test;")
#foo = cur.fetchone()
#(1, 100, "abc'def")
#print foo
#conn.commit()
#cur.close()
#conn.close()
###############################################################################
#  Set up Kafka Consumer
###############################################################################
consumer = KafkaConsumer(
                        bootstrap_servers='localhost:9092',
                        auto_offset_reset='smallest',  # Reset partition offsets upon OffsetOutOfRangeError
                        group_id='tweet_test',   # must have a unique consumer group id
                        value_deserializer=lambda m: json.loads(m.decode('utf-8')))
                        #consumer_timeout_ms=10000)
                                # How long to listen for messages - we do it for 10 seconds
                                # because we poll the kafka broker only each couple of hours

consumer.subscribe(topics='tweets')

#  Start reading messages from Kafka & insert them into postgres

cur=conn.cursor()

#consumer.seek_to_beginning()
print consumer.topics()
num_tweets = 0

#csv_buffer = StringIO()
for msg in consumer:
    #csv_buffer.write(message.value.decode() + '\n')
    #print (msg.value.decode())
    tweet_userid,tweet_create_timestamp,tweet_followers_count,tweet_location,tweet_favorite_count,tweet_retweet_count,tweet_text,empty = msg.value.decode().split(';;;')
    print (tweet_text)
    #slow but it works
    SQL = "INSERT INTO tweets VALUES  (%s, %s, %s, %s, %s, %s, %s)"
    data = (tweet_userid,tweet_create_timestamp,tweet_followers_count,tweet_location,tweet_favorite_count,tweet_retweet_count,tweet_text)
    cur.execute(SQL, data)
    conn.commit()
    num_tweets += 1



# Make sure we clean up before exiting
conn.close()
print("Processed {0} tweets".format(num_tweets))
