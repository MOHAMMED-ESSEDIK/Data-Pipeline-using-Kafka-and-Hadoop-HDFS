from kafka import KafkaConsumer
import json

# ---------- Kafka Consumer ----------
consumer = KafkaConsumer(
    "twitter_data",                  # Topic to subscribe to
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",    # Start from the beginning of the topic
    enable_auto_commit=True,         # Automatically commit offsets
    group_id="twitter_group",        # Consumer group name
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))  # Decode JSON
)

print("Listening for messages...")

for message in consumer:
    tweet = message.value
    print(f"Tweet ID: {tweet['id']}")
    print(f"Created at: {tweet['created_at']}")
    print(f"Text: {tweet['text']}")
    print(f"User Location: {tweet['user_location']}")
    print(f"Retweets: {tweet['retweets']}, Likes: {tweet['likes']}")
    print(f"Followers: {tweet['followers']}, Language: {tweet['lang']}")
    print("-" * 50)
