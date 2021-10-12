#!/usr/bin/env bash

export KAFKA_HOME=/home/mark/kafka_2.12-2.6.2

echo "Starting Zookeeper..."

# Start ZooKeeper Server
$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties > zookeeper.log 2> zookeeper.err.log &

sleep 5

echo "Starting Kafka..."

# Start Kafka Server
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties > kafka.log 2> kafka.err.log &