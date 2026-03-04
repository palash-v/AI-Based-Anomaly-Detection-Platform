from flask import Flask, jsonify, render_template, request
from flask import send_file 
import psycopg2
import os
import io
import csv

app = Flask(__name__)

# PostgreSQL connection
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="healthcare_db",
        user="admin",
        password="admin"
    )

@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/dashboard")
def analytics_dashboard():
    return render_template("dashboard.html")


@app.route("/monitor")
def live_monitor():
    return render_template("index.html")


# 🔹 Get Latest Record
@app.route("/latest")
def latest():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, patient_id, anomaly_score, severity,
               heart_rate, spo2, temperature,
               systolic_bp, diastolic_bp
        FROM anomaly_logs
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({
            "timestamp": row[0],
            "patient_id": row[1],
            "anomaly_score": row[2],
            "severity": row[3],
            "heart_rate": row[4],
            "spo2": row[5],
            "temperature": row[6],
            "systolic_bp": row[7],
            "diastolic_bp": row[8]
        })

    return jsonify({"message": "No data available"})


# 🔹 Get Recent Logs (for table)
@app.route("/logs")
def get_logs():
    conn = psycopg2.connect(
        host="localhost",
        database="healthcare_db",
        user="admin",
        password="admin"
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, patient_id, anomaly_score, severity,
               heart_rate, spo2, temperature,
               systolic_bp, diastolic_bp, explanation
        FROM anomaly_logs
        ORDER BY id DESC
        LIMIT 50
    """)

    rows = cursor.fetchall()

    logs = []
    for row in rows:
        logs.append({
            "timestamp": row[0],
            "patient_id": row[1],
            "score": float(row[2]),
            "severity": row[3],
            "heart_rate": row[4],
            "spo2": row[5],
            "temperature": row[6],
            "blood_pressure": f"{row[7]}/{row[8]}",
            "explanation": row[9]
        })

    return jsonify(logs)

#export
@app.route("/export")
def export_logs():
    conn = psycopg2.connect(
        host="localhost",
        database="healthcare_db",
        user="admin",
        password="admin"
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, patient_id, anomaly_score, severity, explanation
        FROM anomaly_logs
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Timestamp", "Patient ID", "Score", "Severity", "Explanation"])

    for row in rows:
        writer.writerow(row)

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="patient_logs.csv"
    )

#Dashboard route
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)