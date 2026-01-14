from hdfs import InsecureClient

client = InsecureClient(
    "http://192.168.1.106:50070",
    user="hadoop"
)

client.write(
    "/twitter_data/test.txt",
    "HDFS OK",
    encoding="utf-8"
)

print("WRITE SUCCESS")
