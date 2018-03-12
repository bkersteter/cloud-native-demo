tart Services

brew services start postgresql
brew services start zookeeper
brew services start kafka

#Important to start zookeeper before Kafka

# Postgres Info

Created database bjk.  Default db you log into


#Kafka commands
# All binaries in /usr/local/bin
#zookeeper args are mandatory

#list topics
kafka-topics --list --zookeeper localhost:2181

#create topic
kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic tweets

# Show topic detailsf
kafka-topics --describe --zookeeper localhost:2181 --topic tweets

#  Dump topic to stdout
#  NOTE:  kafka-console-consumer should use bootstrap-server instead of zookeeper going forward
kafka-console-consumer --bootstrap-server localhost:9092 --topic tweets --from-beginning

# Delete topic
kafka-topics --delete --zookeeper localhost:2181 --topic tweets

# List Kafka Consumer Groups
kafka-consumer-groups --bootstrap-server localhost:9092 --list

#Describe stats for a given Kafka Consumer Group
kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group test

# Reset consumer group to seek_to_beginning
kafka-consumer-groups --bootstrap-server localhost:9092 --reset-offsets --to-earliest --group test --all-topics
