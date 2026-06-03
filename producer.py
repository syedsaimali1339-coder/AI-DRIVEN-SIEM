from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

ips = ["192.168.1.10", "10.0.0.5", "172.16.0.8"]

print("🚀 Producer running...")

while True:
    log = {
        "src_ip": random.choice(ips),
        "failed_logins": random.randint(0, 20),
        "event_count": random.randint(1, 50)
    }

    producer.send("security-logs", log)
    print("Sent:", log)

    time.sleep(2)
