# cloud-native-demo

This repo contains the files and a short presentation covering 'cloud-native' design principles for data pipelines and data systems.

The scripts are all designed to work on a local desktop or laptop.  Some sort of internet connection is needed to access the Twitter API via the two producer scripts.  The Twitter API rate limits the number of queries you can make to 450 in a 15-minute time span so you shouldn't have worry about overwhelming your machine and filling up the local drive.

# Required Software

This demo was built to run on a Mac so your mileage may vary on Windows or other systems.

- Python 2.7
- Java 1.8
- Additional Python Libraries:  tweepy, psycopg, kafka-python
- Apache Kafka 1.0.0
- Apache Zookeeper (latest version)
- Postgres 10.3

In addition, in order to work with the Twitter API to search and grab tweets, you'll need to have a valid twitter account and set up the consumer keys and access tokens through https://apps.twitter.com.  
