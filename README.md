# 📊 Data Pipeline Using Kafka & Hadoop HDFS (Step-by-Step Guide)

This project demonstrates a **real-world data pipeline** where data is collected from **Twitter**, streamed through **Apache Kafka**, and finally stored in **Hadoop HDFS** running on a **Virtual Machine**.

This README explains:

* The **architecture**
* **Installation & configuration** steps
* **How to run the project step by step**
* **All problems encountered** and **how we solved them** (very important for learning & interviews)

---

## 🏗️ Architecture Overview

```
Twitter API
   ↓
Kafka Producer (Python – Windows Host)
   ↓
Kafka Topic (twitter_data)
   ↓
Kafka Consumer (Python – Windows Host)
   ↓
HDFS (Hadoop 2.x on Ubuntu Virtual Machine)
```

### Key Points

* Kafka & Python run on **Windows (Host)**
* Hadoop HDFS runs on **Ubuntu (VirtualBox VM)**
* Communication happens via **network IP (not localhost)**

---

## 🧰 Technologies Used

* **Python 3.13**
* **Apache Kafka 3.8.1** (Windows)
* **Apache Hadoop 2.7.x** (Ubuntu VM)
* **Twitter API v2 (Tweepy)**
* **VirtualBox**

---

## 📁 Project Structure

```
Data-Pipeline-using-Kafka-and-Hadoop-HDFS/
│
├── kafka_tweet_preducer.py      # Twitter → Kafka producer
├── kafka_tweet_consumer.py      # Kafka → Console consumer (test)
├── hdfs_consumer.py             # Kafka → HDFS consumer
├── secret.txt                   # Twitter API keys
├── test.py                      # HDFS connection test
└── README.md
```

---

## 🖥️ Step 1 – Setup Hadoop HDFS (Ubuntu VM)

### 1️⃣ Install Hadoop on Ubuntu

* Hadoop 2.7.x installed in:

```
/home/vboxuser/Desktop/hadoop2/hadoop-2.7.3
```

### 2️⃣ Check HDFS Services

```bash
jps
```

Expected:

```
NameNode
DataNode
SecondaryNameNode
```

### 3️⃣ HDFS Web UI

From **Windows browser**:

```
http://<VM_IP>:50070
```

Example:

```
http://192.168.1.106:50070
```

---

## 🌐 Step 2 – Network Configuration (VERY IMPORTANT)

### VM IP Address

```bash
ip a
```

Example:

```
eth0 → 192.168.1.106
```

➡️ This IP **must be used everywhere** (never `localhost`).

---

## ⚙️ Step 3 – Hadoop Configuration Files

### ✅ core-site.xml

```xml
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://192.168.1.106:9000</value>
  </property>
</configuration>
```

### ✅ hdfs-site.xml (FINAL FIXED VERSION)

```xml
<configuration>

  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>

  <property>
    <name>dfs.namenode.name.dir</name>
    <value>/home/vboxuser/Desktop/hdfs/namenode</value>
  </property>

  <property>
    <name>dfs.datanode.data.dir</name>
    <value>/home/vboxuser/Desktop/hdfs/datanode</value>
  </property>

  <!-- Force IP usage instead of hostname -->
  <property>
    <name>dfs.client.use.datanode.hostname</name>
    <value>false</value>
  </property>

  <property>
    <name>dfs.datanode.use.datanode.hostname</name>
    <value>false</value>
  </property>

  <!-- Bind DataNode to all interfaces -->
  <property>
    <name>dfs.datanode.address</name>
    <value>0.0.0.0:50010</value>
  </property>

  <property>
    <name>dfs.datanode.http.address</name>
    <value>0.0.0.0:50075</value>
  </property>

</configuration>
```

### Restart HDFS

```bash
stop-dfs.sh
start-dfs.sh
```

---

## 🪟 Step 4 – Windows DNS Fix (CRITICAL)

### ❌ Problem

Hadoop returns this hostname:

```
ubuntu.myguest.virtualbox.org
```

Windows **cannot resolve it**, causing HDFS writes to fail.

### ✅ Solution – Edit Windows hosts file

Open **Notepad as Administrator** and edit:

```
C:\Windows\System32\drivers\etc\hosts
```

Add:

```
192.168.1.106   ubuntu.myguest.virtualbox.org
```

Flush DNS:

```powershell
ipconfig /flushdns
```

---

## 🧪 Step 5 – Test HDFS from Windows

```powershell
python test.py
```

Expected output:

```
WRITE SUCCESS
```

Verify on VM:

```bash
hdfs dfs -cat /twitter_data/test.txt
```

---

## 🧵 Step 6 – Setup Kafka (Windows)

Go to Kafka directory:

```powershell
cd C:\kafka\kafka_2.13-3.8.1
```

### Start Zookeeper

```powershell
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

### Start Kafka Broker

```powershell
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

### Create Topic

```powershell
.\bin\windows\kafka-topics.bat --create --topic twitter_data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

---

## 🐍 Step 7 – Run the Pipeline

### Terminal 1 – HDFS Consumer

```powershell
python hdfs_consumer.py
```

### Terminal 2 – Twitter Producer

```powershell
python kafka_tweet_preducer.py
```

Expected output:

```
Stored 50 tweets in /twitter_data/tweets_YYYYMMDD_HHMMSS.json
```

Verify in HDFS:

```bash
hdfs dfs -ls /twitter_data
```

---

## ⚠️ Common Problems & Solutions

### ❌ UnicodeEncodeError on Windows

**Cause:** Unicode arrow character `→`

**Fix:**

```python
print("Kafka -> HDFS consumer started...")
```

---

### ❌ HDFS Connection Error

**Cause:** Hadoop hostname not resolvable on Windows

**Fix:** Add hostname to `hosts` file

---

### ❌ Kafka commands not recognized

**Cause:** Using `.sh` scripts on Windows

**Fix:** Use `.bat` scripts

---

## 🎓 Interview-Ready Explanation

> “I built a Kafka-based streaming pipeline where data is ingested from Twitter, streamed via Kafka, and persisted in HDFS running on a virtual machine. I solved real-world issues such as Hadoop hostname resolution, Windows encoding errors, and cross-OS networking.”

---

## 🚀 Conclusion

This project demonstrates:

* Real-time data streaming
* Distributed storage with HDFS
* Cross-platform integration
* Real production-level debugging

✅ **Pipeline fully functional**

---

## 📌 Author

**ESSEDIK MOHAMMED**

Feel free to fork, improve, or extend this project 🚀
