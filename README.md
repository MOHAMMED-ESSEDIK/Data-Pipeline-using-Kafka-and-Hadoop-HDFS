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


flowchart TB
    subgraph Data_Source
        A[Twitter API]
    end

    subgraph Streaming_Layer
        B[Kafka Producer]
        C[Kafka Broker]
    end

    subgraph Storage_Layer
        D[Kafka Consumer]
        E[HDFS]
    end

    A --> B
    B --> C
    C --> D
    D --> E

## 🧩 System Architecture

```mermaid
flowchart LR
    A[Twitter API] -->|Tweets| B[Kafka Producer<br/>Python + Tweepy]
    B -->|Stream| C[Kafka Topic<br/>twitter_data]
    C -->|Consume| D[Kafka Consumer<br/>Python]
    D -->|JSON Files| E[Hadoop HDFS]




```md
### 🔍 Architecture Explanation

1. **Twitter API**  
   Provides real-time tweets based on a search query.

2. **Kafka Producer**  
   Collects tweets using Tweepy and publishes them to Kafka.

3. **Kafka Topic (twitter_data)**  
   Acts as a message buffer to decouple producers and consumers.

4. **Kafka Consumer**  
   Reads streaming tweets from Kafka in real time.

5. **Hadoop HDFS**  
   Stores tweets as JSON files for large-scale data analysis.
