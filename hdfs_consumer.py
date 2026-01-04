from kafka import KafkaConsumer
from hdfs import InsecureClient
import json
import time

# ---------- Kafka Consumer ----------
consumer = KafkaConsumer(
    "twitter_data",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="twitter_group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

# ---------- HDFS Client ----------
# Replace namenode URL and port
hdfs_client = InsecureClient('http://localhost:9870', user='hadoop')  

# HDFS directory to store tweets
hdfs_dir = "/twitter_data/"

print("Listening for tweets and saving to HDFS...")

for message in consumer:
    tweet = message.value
    tweet_id = tweet['id']

    # HDFS file path (you can use timestamp or tweet ID to make it unique)
    hdfs_path = hdfs_dir + f"tweet_{tweet_id}.json"

    try:
        # Write tweet JSON to HDFS
        hdfs_client.write(hdfs_path, json.dumps(tweet), encoding='utf-8')
        print(f"Stored tweet {tweet_id} in HDFS")
    except Exception as e:
        print(f"Error storing tweet {tweet_id}: {e}")
        time.sleep(1)
