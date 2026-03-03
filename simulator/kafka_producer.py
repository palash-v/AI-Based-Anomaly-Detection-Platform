from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

# connect to kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Connected to Kafka... Sending live vitals")

while True:
    data = {
        "timestamp": str(datetime.now()),
        "heart_rate": random.randint(60, 140),
        "spo2": random.randint(90, 100),
        "temperature": round(random.uniform(36.5, 39.5), 1),
        "systolic_bp": random.randint(110, 160),
        "diastolic_bp": random.randint(70, 100)
    }

    producer.send("patient_vitals", data)
    print("Sent:", data)

    time.sleep(2)