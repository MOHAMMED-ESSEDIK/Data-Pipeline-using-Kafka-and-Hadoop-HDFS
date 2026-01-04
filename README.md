# Data-Pipeline-using-Kafka-and-Hadoop-HDFS
Real-Time Twitter Data Pipeline using Kafka and Hadoop HDFS

#  Real-Time Twitter Data Pipeline with Kafka & Hadoop HDFS

##  Project Overview
This project demonstrates a **real-time Big Data pipeline** that collects tweets from the Twitter API, streams them using **Apache Kafka**, and stores them in **Hadoop HDFS** for large-scale data processing.

It simulates a real-world **Data Engineering / Big Data architecture**.

---

##  Architecture
Twitter API  
➡️ Kafka Producer  
➡️ Kafka Topic (`twitter_data`)  
➡️ Kafka Consumer  
➡️ Hadoop HDFS  

---

##  Technologies Used
- Python
- Twitter API (Tweepy)
- Apache Kafka
- Apache Zookeeper
- Hadoop HDFS
- JSON

---
## Start Kafka Server
---
bin/windows/kafka-server-start.bat config/server.properties


##Create Kafka Topic
---
bin/windows/kafka-topics.bat --create \
--topic twitter_data \
--bootstrap-server localhost:9092 \
--partitions 1 \
--replication-factor 1


##Create HDFS Directory
---
hdfs dfs -mkdir -p /twitter_data

##Run the Producer
---
python producer/twitter_producer.py

##Run the Consumer
---
python consumer/kafka_to_hdfs_consumer.py

