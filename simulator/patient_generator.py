from kafka import KafkaProducer
import json
import random
import time
import csv
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers='127.0.0.1:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    linger_ms=0,
    acks='all',
    retries=5,
    max_in_flight_requests_per_connection=1
)

# normal human ranges
def generate_normal_vitals():
    heart_rate = random.randint(65, 90)          # bpm
    spo2 = random.randint(96, 100)               # %
    temperature = round(random.uniform(36.5, 37.2), 1)  # °C
    systolic = random.randint(110, 125)
    diastolic = random.randint(70, 85)

    return [heart_rate, spo2, temperature, systolic, diastolic]

# abnormal condition
def generate_abnormal_vitals():
    heart_rate = random.randint(120, 160)
    spo2 = random.randint(82, 90)
    temperature = round(random.uniform(38.5, 40.5), 1)
    systolic = random.randint(140, 180)
    diastolic = random.randint(95, 120)

    return [heart_rate, spo2, temperature, systolic, diastolic]


file = "data/live_vitals.csv"

# create CSV header
with open(file, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp","heart_rate","spo2","temperature","systolic_bp","diastolic_bp"])

print("Starting patient monitor...\n")

while True:
    # 85% normal, 15% abnormal
    if random.random() < 0.85:
        vitals = generate_normal_vitals()
        status = "NORMAL"
    else:
        vitals = generate_abnormal_vitals()
        status = "ABNORMAL"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp] + vitals

    # append to csv
    with open(file, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

    print(f"{timestamp} | HR:{vitals[0]}  SpO2:{vitals[1]}%  Temp:{vitals[2]}°C  BP:{vitals[3]}/{vitals[4]}  --> {status}")

    data = {
    "heart_rate": vitals[0],
    "spo2": vitals[1],
    "temperature": vitals[2],
    "systolic_bp": vitals[3],
    "diastolic_bp": vitals[4]
}

    producer.send("patient_vitals", data)
    producer.flush()  # keep this

    time.sleep(2)