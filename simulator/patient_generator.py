from kafka import KafkaProducer
import json
import random
import time
import csv
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers='127.0.0.1:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Define realistic patient baselines
patients = {
    "P001": {
        "hr_range": (70, 85),
        "spo2_range": (95, 100),
        "temp_range": (36.5, 37.2),
        "sys_range": (110, 125),
        "dia_range": (70, 85)
    },
    "P002": {
        "hr_range": (60, 75),
        "spo2_range": (94, 99),
        "temp_range": (36.4, 37.0),
        "sys_range": (105, 120),
        "dia_range": (65, 80)
    },
    "P003": {
        "hr_range": (80, 95),
        "spo2_range": (96, 100),
        "temp_range": (36.8, 37.5),
        "sys_range": (115, 130),
        "dia_range": (75, 90)
    }
}

file = "data/live_vitals.csv"

with open(file, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp","patient_id","heart_rate","spo2","temperature","systolic_bp","diastolic_bp"])

print("Starting multi-patient monitor...\n")

while True:
    patient_id = random.choice(list(patients.keys()))
    baseline = patients[patient_id]

    # 80% normal, 20% abnormal
    if random.random() < 0.8:
        heart_rate = random.randint(*baseline["hr_range"])
        spo2 = random.randint(*baseline["spo2_range"])
        temperature = round(random.uniform(*baseline["temp_range"]), 1)
        systolic = random.randint(*baseline["sys_range"])
        diastolic = random.randint(*baseline["dia_range"])
        status = "NORMAL"
    else:
        heart_rate = random.randint(120, 170)
        spo2 = random.randint(80, 90)
        temperature = round(random.uniform(38.5, 41.0), 1)
        systolic = random.randint(150, 200)
        diastolic = random.randint(95, 120)
        status = "ABNORMAL"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [timestamp, patient_id, heart_rate, spo2, temperature, systolic, diastolic]

    with open(file, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

    print(f"{timestamp} | {patient_id} | HR:{heart_rate} SpO2:{spo2}% Temp:{temperature} BP:{systolic}/{diastolic} --> {status}")

    data = {
        "timestamp": timestamp,
        "patient_id": patient_id,
        "heart_rate": heart_rate,
        "spo2": spo2,
        "temperature": temperature,
        "systolic_bp": systolic,
        "diastolic_bp": diastolic
    }

    producer.send("patient_vitals", data)
    producer.flush()

    time.sleep(2)