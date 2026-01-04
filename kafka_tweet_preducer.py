import tweepy
import json
import time
from kafka import KafkaProducer

# ---------- Load secrets ----------
def load_secrets(path="secret.txt"):
    secrets = {}
    with open(path, "r") as f:
        for line in f:
            if "=" in line:
                k, v = line.split("=", 1)
                secrets[k.strip()] = v.strip().strip("'").strip('"')
    return secrets

secrets = load_secrets("secret.txt")

# ---------- Twitter Client ----------
client = tweepy.Client(
    bearer_token=secrets["bearer_token"],
    wait_on_rate_limit=True
)

# ---------- Kafka Producer ----------
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

query = "music lang:en -is:retweet"

try:
    response = client.search_recent_tweets(
        query=query,
        max_results=10,
        tweet_fields=["created_at", "lang", "public_metrics"],
        user_fields=["location", "public_metrics"],
        expansions=["author_id"]
    )

    if response.data:
        users = {u.id: u for u in response.includes["users"]}

        for tweet in response.data:
            user = users[tweet.author_id]

            data = {
                "id": tweet.id,
                "created_at": tweet.created_at.isoformat(),
                "text": tweet.text,
                "user_location": user.location,
                "retweets": tweet.public_metrics["retweet_count"],
                "likes": tweet.public_metrics["like_count"],
                "followers": user.public_metrics["followers_count"],
                "lang": tweet.lang
            }

            producer.send("twitter_data", data)
            print(f"Sent tweet {tweet.id} to Kafka")

except tweepy.TooManyRequests:
    time.sleep(900)

producer.flush()
