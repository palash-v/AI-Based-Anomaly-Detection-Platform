# 🏥 AI-Driven Healthcare Anomaly Detection System

A **real-time healthcare monitoring system** that detects abnormal patient vitals using **Machine Learning**, streams data through **Apache Kafka**, stores anomaly logs in **PostgreSQL (Docker container)**, and visualizes insights using **interactive dashboards** with automated **email alerts**.

---

# Project Overview

This project simulates wearable healthcare devices sending **patient vital data in real time**.

The system processes the incoming data using a **Machine Learning anomaly detection model (Isolation Forest)** to detect abnormal health conditions.

When anomalies occur, the system:

• Stores the event in a PostgreSQL database
• Updates the real-time dashboards
• Sends automated **email alerts**

---

# System Architecture

```
Wearable Sensors
        │
        ▼
Patient Generator (Simulator)
        │
        ▼
Apache Kafka (Real-Time Streaming)
        │
        ▼
ML Anomaly Detector (Isolation Forest)
        │
        ▼
PostgreSQL Database (Docker Container)
        │
        ▼
Flask Backend API
        │
        ▼
Analytics Dashboard + Live Monitor
        │
        ▼
Email Alerts to Doctors
```

---

# Features

## Real-Time Data Streaming

Simulates multiple patients generating vital signs:

* Heart Rate
* SpO₂
* Temperature
* Blood Pressure

Data is streamed through **Apache Kafka**.

---

## Machine Learning Anomaly Detection

The system uses **Isolation Forest** to detect abnormal health patterns.

Example anomalies:

* High heart rate
* Low oxygen levels
* High body temperature
* High blood pressure

Each anomaly receives a **severity level**:

```
LOW
MEDIUM
HIGH
```

---

## Explainable Alerts

Each anomaly includes **explainability insights**.

Example:

```
Explainability
• Heart Rate elevated
• Oxygen saturation decreased
• Body temperature elevated
```

This improves **trust and interpretability for doctors**.

---

## Email Alert System

Critical anomalies trigger **automated email alerts** containing:

* Patient ID
* Vital signs
* Anomaly score
* Explainability summary

A **cooldown system** prevents repeated emails.

---

# Dashboards

The system includes **two dashboards**.

---

## Analytics Dashboard

Displays system-wide insights:

* Active patients
* High-risk alerts
* Average anomaly score
* Severity distribution
* Heart rate trends
* SpO₂ trends
* Temperature variance
* Blood pressure trends

---

## Live Monitoring Dashboard

Displays:

* Real-time patient vitals
* Alert history
* Recent anomaly logs
* Heart rate trend chart
* Patient filter (All / P001 / P002 / P003)

---

# Technologies Used

## Backend

* Python
* Flask

## Data Streaming

* Apache Kafka

## Machine Learning

* Scikit-learn
* Isolation Forest

## Database

* PostgreSQL

## Containerization

* Docker

## Data Processing

* Pandas
* Joblib

## Visualization

* Chart.js

---

# Project Structure

```
AI-Driven-Healthcare-Anomaly-Detection-System
│
├── backend
│   ├── anomaly_detector.py
│   ├── dashboard_api.py
│
├── simulator
│   └── patient_generator.py
│
├── model
│   ├── anomaly_model.pkl
│   └── scaler.pkl
│
├── templates
│   ├── dashboard.html
│   └── monitor.html
│
├── requirements.txt
├── docker-compose.yml
├── start_all.bat
├── start_kafka.bat
├── start_consumer.bat
├── start_producer.bat
└── README.md
```

---

# Prerequisites

Make sure the following are installed on your system:

* Python 3.10+
* Apache Kafka
* PostgreSQL (runs inside Docker container)
* Docker / Docker Desktop
* Git

---

# Docker Setup (PostgreSQL Database)

The system uses **Docker to run PostgreSQL**.

Run the following command to start the database container:

```
docker run -d \
-p 5432:5432 \
--name healthcare_postgres \
-e POSTGRES_DB=healthcare_db \
-e POSTGRES_USER=admin \
-e POSTGRES_PASSWORD=admin \
postgres
```

Database credentials:

```
Database : healthcare_db
User     : admin
Password : admin
Host     : localhost
Port     : 5432
```

---

# Quick Setup

### Clone Repository

```
git clone https://github.com/palash-v/AI-Based-Anomaly-Detection-Platform.git
```

```
cd AI-Based-Anomaly-Detection-Platform
```

---

### Install Dependencies

```
pip install -r requirements.txt
```

---

# Running the Project


## Step 1 — Start Zookeeper

```
cd C:\kafka
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

---

## Step 2 — Start Kafka Server

```
cd C:\kafka
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

Wait until you see:

```
KafkaServer id=0 started
```

---

## Step 3 — Start Anomaly Detector

Open terminal inside the project folder:

```
venv\Scripts\activate
python backend/anomaly_detector.py
```

You should see:

```
AI Monitoring Started...
```

---

## Step 4 — Start Patient Generator

Open another terminal:

```
venv\Scripts\activate
python simulator/patient_generator.py
```

This starts the **real-time patient simulation**.

---

## Step 5 — Start Dashboard API

```
python backend/dashboard_api.py
```

---

## Step 6 — Open Dashboard

Open browser and visit:

```
http://127.0.0.1:5000/dashboard
```

You can switch between:

```
Analytics Dashboard
Live Patient Monitor
```

---

# System Testing

The system was tested with the following scenarios.

---

## Normal Vitals

```
Heart Rate: 72
SpO₂: 98
Temperature: 36.7
```

Result:

```
LOW severity
```

---

## Sustained Anomalies

```
Heart Rate: 150
SpO₂: 82
Temperature: 40
Blood Pressure: 200/120
```

Result:

```
HIGH severity alert
Email notification triggered
```

---

## Multiple Patients

The system successfully handles multiple patient streams:

```
P001
P002
P003
```

---

# Example Email Alert

```
Critical Health Anomaly Detected

Patient ID: P002
Anomaly Score: 0.082

Vitals
Heart Rate: 155
SpO₂: 78
Temperature: 40.2
Blood Pressure: 203/115

Explainability
• Heart Rate elevated
• Oxygen saturation decreased
• Body temperature elevated
```

---

# End Users

This system can assist:

* Doctors
* Healthcare staff
* Hospital monitoring teams

---

# Future Improvements

Possible enhancements:

* Mobile health monitoring application
* IoT wearable device integration
* Deep learning anomaly detection
* Real hospital data integration
* Cloud deployment

---

# License

This project is for **educational purposes**.

---