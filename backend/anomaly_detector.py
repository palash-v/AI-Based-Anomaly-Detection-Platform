import os
import csv
from datetime import datetime
from kafka import KafkaConsumer
import json
import joblib
import pandas as pd

# load trained model and scaler
model = joblib.load("model/anomaly_model.pkl")
scaler = joblib.load("model/scaler.pkl")

# connect to kafka topic
consumer = KafkaConsumer(
    'patient_vitals',
    bootstrap_servers='127.0.0.1:9092',
    auto_offset_reset='latest',   
    enable_auto_commit=True,
    group_id='live-monitor-v2',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("AI Monitoring Started...\n")

for message in consumer:
    data = message.value

    # convert to dataframe
    df = pd.DataFrame([{
        "heart_rate": data["heart_rate"],
        "spo2": data["spo2"],
        "temperature": data["temperature"],
        "systolic_bp": data["systolic_bp"],
        "diastolic_bp": data["diastolic_bp"]
    }])

    # scale features
    scaled = scaler.transform(df)

    # predict anomaly
    prediction = model.predict(scaled)

    if prediction[0] == -1:
        print("🚨 ALERT! Abnormal Patient Detected:", data)

        # save alert to file
        file_exists = os.path.isfile("data/alerts.csv")

        with open("data/alerts.csv", "a", newline="") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow([
                    "timestamp",
                    "heart_rate",
                    "spo2",
                    "temperature",
                    "systolic_bp",
                    "diastolic_bp"
                ])

            writer.writerow([
                datetime.now(),
                data["heart_rate"],
                data["spo2"],
                data["temperature"],
                data["systolic_bp"],
                data["diastolic_bp"]
            ])

    else:
        print("Normal:", data)