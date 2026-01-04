from kafka import KafkaConsumer
from hdfs import InsecureClient
import json
import time
from datetime import datetime

consumer = KafkaConsumer(
    "twitter_data",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="twitter_hdfs_group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

hdfs_client = InsecureClient("http://localhost:9870", user="hadoop")
hdfs_dir = "/twitter_data/"

BATCH_SIZE = 50
buffer = []

print("Kafka → HDFS consumer started...")

for message in consumer:
    buffer.append(message.value)

    if len(buffer) >= BATCH_SIZE:
        filename = f"tweets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        hdfs_path = hdfs_dir + filename

        try:
            hdfs_client.write(
                hdfs_path,
                json.dumps(buffer, indent=2),
                encoding="utf-8"
            )
            print(f"Stored {len(buffer)} tweets in {hdfs_path}")
            buffer.clear()
        except Exception as e:
            print("HDFS write error:", e)
            time.sleep(2)
