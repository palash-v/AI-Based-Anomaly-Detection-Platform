# 🏥 Healthcare Anomaly Detection System

This project simulates real-time patient vitals and detects abnormal conditions using Machine Learning and Kafka.

---

## 📌 Features

- Simulates patient vitals (Heart Rate, SpO2, Temperature, Blood Pressure)
- Streams data using Apache Kafka
- Detects abnormal patient conditions
- Generates real-time alerts

---

## 🛠 Technologies Used

- Python
- Apache Kafka
- Scikit-learn
- Pandas
- Joblib

---

## ⚡ Quick Setup (Windows)

1. Clone the repository
2. Double-click `setup.bat`
3. Wait for installation to finish

---

## 📦 Prerequisites

Before running this project, make sure you have:

- Python 3.10+
- Apache Kafka installed
- Git installed

---

## 🚀 How To Run (Complete Guide - Windows)

⚠️ Make sure Apache Kafka is installed on your system.

---

### 🟢 Step 1 — Start Zookeeper

Open Command Prompt and run:

cd C:\kafka
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties

Wait until it fully starts.

---

### 🟢 Step 2 — Start Kafka Server

Open another Command Prompt and run:

cd C:\kafka
.\bin\windows\kafka-server-start.bat .\config\server.properties

Wait until you see:
KafkaServer id=0 started

---

### Create two different terminals for next two steps

### 🟢 Step 3 — Start Anomaly Detector

Open VS Code terminal inside project folder:

venv\Scripts\activate
python backend/anomaly_detector.py

You should see:
AI Monitoring Started...

---

### 🟢 Step 4 — Start Patient Generator

Open another terminal inside project folder:

venv\Scripts\activate
python simulator/patient_generator.py

You should now see live vitals and alerts working in real-time.

---