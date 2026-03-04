import json
import time
from datetime import datetime

import joblib
import pandas as pd
import psycopg2
from kafka import KafkaConsumer

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# =============================
# LOAD MODEL & SCALER
# =============================

model = joblib.load("model/anomaly_model.pkl")
scaler = joblib.load("model/scaler.pkl")


# =============================
# DATABASE CONNECTION
# =============================

conn = psycopg2.connect(
    host="localhost",
    database="healthcare_db",
    user="admin",
    password="admin"
)

cursor = conn.cursor()


# =============================
# EMAIL CONFIGURATION
# =============================

SENDER_EMAIL = "ai.health.monitor.alerts@gmail.com"
RECEIVER_EMAIL = "noobbeast16@gmail.com"
APP_PASSWORD = "kydilnedijyytoil"

EMAIL_COOLDOWN = 180
last_email_time = {}


def send_email_alert(patient_id, score, data, issues):

    subject = "🚨 Critical Health Anomaly Detected"

    html_body = f"""
    <html>
    <body style="font-family:Arial;background-color:#0f172a;color:white;padding:20px;">

    <h2 style="color:#ef4444;">🚨 Critical Health Anomaly Detected</h2>

    <p><b>Patient ID:</b> {patient_id}</p>
    <p><b>Anomaly Score:</b> {score:.3f}</p>

    <h3 style="color:#38bdf8;">Vital Signs</h3>

    <table style="border-collapse:collapse;width:400px;">
    <tr>
    <td style="border:1px solid #555;padding:8px;">Heart Rate</td>
    <td style="border:1px solid #555;padding:8px;">{data['heart_rate']}</td>
    </tr>

    <tr>
    <td style="border:1px solid #555;padding:8px;">SpO₂</td>
    <td style="border:1px solid #555;padding:8px;">{data['spo2']}</td>
    </tr>

    <tr>
    <td style="border:1px solid #555;padding:8px;">Temperature</td>
    <td style="border:1px solid #555;padding:8px;">{data['temperature']}</td>
    </tr>

    <tr>
    <td style="border:1px solid #555;padding:8px;">Blood Pressure</td>
    <td style="border:1px solid #555;padding:8px;">
    {data['systolic_bp']}/{data['diastolic_bp']}
    </td>
    </tr>
    </table>

    <h3 style="color:#f59e0b;">Explainability</h3>

    <ul>
    {''.join([f"<li>{issue}</li>" for issue in issues])}
    </ul>

    <p style="margin-top:20px;color:#94a3b8;">
    AI Healthcare Monitoring System
    </p>

    </body>
    </html>
    """

    msg = MIMEMultipart()   # ✅ CREATE MESSAGE FIRST
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(html_body, "html"))   # ✅ NOW ATTACH BODY

    try:

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)

        server.sendmail(
            SENDER_EMAIL,
            RECEIVER_EMAIL,
            msg.as_string()
        )

        server.quit()

        print("📩 Email Alert Sent Successfully")

    except Exception as e:
        print("❌ Email Sending Failed:", e)


# =============================
# KAFKA CONSUMER
# =============================

consumer = KafkaConsumer(
    'patient_vitals',
    bootstrap_servers='127.0.0.1:9092',
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='live-monitor-v3',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("🚀 AI Monitoring Started...\n")


# =============================
# MAIN LOOP
# =============================

for message in consumer:

    data = message.value
    patient_id = data["patient_id"]

    df = pd.DataFrame([{
        "heart_rate": data["heart_rate"],
        "spo2": data["spo2"],
        "temperature": data["temperature"],
        "systolic_bp": data["systolic_bp"],
        "diastolic_bp": data["diastolic_bp"]
    }])

    scaled = scaler.transform(df)

    score = float(-model.decision_function(scaled)[0])
    prediction = model.predict(scaled)[0]

    issues = []

    if prediction == -1:

        if data["heart_rate"] > 120:
            issues.append("Heart Rate elevated")

        if data["spo2"] < 92:
            issues.append("Oxygen saturation decreased")

        if data["temperature"] > 38:
            issues.append("Body temperature elevated")

        if data["systolic_bp"] > 150:
            issues.append("Systolic BP elevated")

        if data["diastolic_bp"] > 95:
            issues.append("Diastolic BP elevated")

        if score > 0.07:
            severity = "HIGH"
        elif score > 0.02:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        print(f"\n🚨 ALERT | {patient_id}")
        print(f"Score: {score:.3f} | Severity: {severity}")
        print("Explainability:")

        for issue in issues:
            print("•", issue)

    else:
        severity = "LOW"
        print(f"Normal | {patient_id} | Score: {score:.3f}")

    explanation_text = ", ".join(issues) if issues else "Normal"


    # =============================
    # DATABASE INSERT
    # =============================

    cursor.execute("""
        INSERT INTO anomaly_logs
        (timestamp, patient_id, anomaly_score, severity,
         heart_rate, spo2, temperature,
         systolic_bp, diastolic_bp, explanation)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        datetime.now(),
        patient_id,
        score,
        severity,
        data["heart_rate"],
        data["spo2"],
        data["temperature"],
        data["systolic_bp"],
        data["diastolic_bp"],
        explanation_text
    ))

    conn.commit()


    # =============================
    # EMAIL ALERT
    # =============================

    current_time = time.time()

    # Get last email time for this patient
    last_time = last_email_time.get(patient_id, 0)

    if severity == "HIGH" and current_time - last_time > EMAIL_COOLDOWN:

        send_email_alert(patient_id, score, data, issues)

        # update cooldown for this patient
        last_email_time[patient_id] = current_time